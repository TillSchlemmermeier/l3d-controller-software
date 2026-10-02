import json
import os
import secrets
from pathlib import Path
from typing import Annotated, Literal, Union

from fastapi import APIRouter, Depends, File, Form, Header, HTTPException, Request, UploadFile
from fastapi import Path as PathParam
from fastapi.responses import FileResponse, JSONResponse
from pydantic import Field

router = APIRouter()


# --- types -------------------------------------------------------------------

FaderKey = Literal['brightness', 'fade']
ToggleKey = Literal['IO']
FaderValue = Annotated[float, PathParam(ge=0, le=1)]
ChannelIndex = Annotated[int, PathParam(ge=0, le=7)]

ChannelKey = Union[Annotated[int, Field(ge=0, le=7)], Literal['global']]
Section = Union[ChannelKey, Literal['panel']]
Slot = Union[Annotated[int, Field(ge=0)], Literal['generator', 's2l', 'dashboard']]


# --- admin token ---------------------------------------------------------------

ADMIN_TOKEN = os.environ.get("L3D_ADMIN_TOKEN", "")


def require_admin(x_admin_token: str = Header(default="")):
    if not ADMIN_TOKEN:
        raise HTTPException(status_code=503, detail="Admin operations disabled: L3D_ADMIN_TOKEN not set")
    if not secrets.compare_digest(x_admin_token, ADMIN_TOKEN):
        raise HTTPException(status_code=401, detail="Invalid or missing admin token")


# --- the shared objects --------------------------------------------------------------

db = None                   # DatabaseManager
state_manager = None        # StateManager
connection_manager = None   # ConnectionManager
state = None                # the UltraDict state
randomizer_queue = None


# --- elements and presets --------------------------------------------------------

# Preview GIFs live here
PREVIEW_DIR = (Path(__file__).resolve().parents[1] / "src/assets/previews").resolve()

# Resolve and traversal-check a preset's preview gif
def preview_path(type: str, element: str, preset: str) -> Path:
    prefix = type if type in ('channel', 'global') else element
    path = (PREVIEW_DIR / f"{prefix}_p_{preset}.gif").resolve()
    if path.parent != PREVIEW_DIR:
        raise HTTPException(status_code=400, detail="Invalid preset or element name")
    return path

# get a list with all the available generators or effects
@router.get('/api/get-element-names/{type}')
async def get_names(type: str):
    return db.get_element_names(type)

# get a list with all the active generators or effects
@router.get('/api/get-active-elements/{type}')
async def get_active_elements(type: str):
    return db.get_active_elements(type)

# get all the information available in the database for a generator or effect
@router.get('/api/get-element-info/{type}/{element_name}')
async def get_element_info(type: str, element_name: str):
    return db.get_element_info(type, element_name)

# get a list with all the preset names and types for an element
@router.get('/api/get-all-presets/{type}/{element_name}')
async def get_all_presets(type: str, element_name: str):
    return db.get_all_presets(type, element_name)

# get a list with all the preset names for a given generator or effect
@router.get('/api/get-presets/{type}/{element_name}')
async def get_presets(type: str, element_name: str):
    return db.get_preset_names(type, element_name)

# get all the information available in the database for a given preset
@router.get('/api/get-preset-info/{type}/{element}/{preset}')
async def get_preset_info(type: str, element: str, preset: str):
    return db.get_preset_info(type, element, preset)

# rename a given preset in the db and in the filesystem
@router.post('/api/rename-preset/{type}/{element}/{old_preset}/{new_preset}', dependencies=[Depends(require_admin)])
async def rename_preset(
    type: str,
    element: str,
    old_preset: str,
    new_preset: str,
):
    # build (and traversal-check) both paths before mutating the DB
    old_file_path = preview_path(type, element, old_preset)
    new_file_path = preview_path(type, element, new_preset)

    success = db.rename_preset(type, element, old_preset, new_preset)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to rename preset")
    # not every preset has a preview GIF
    if old_file_path.exists():
        old_file_path.rename(new_file_path)
    return {"message": "Preset renamed successfully"}

# delete preset
@router.delete('/api/delete-preset/{type}/{element}/{preset}', dependencies=[Depends(require_admin)])
async def delete_preset(type: str, element: str, preset: str):
    success = db.delete_preset(type, element, preset)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to delete preset")
    # remove the preview gif too (best-effort)
    preview_path(type, element, preset).unlink(missing_ok=True)
    return {"message": "Preset deleted successfully"}

# delete element
@router.delete('/api/delete-element/{type}/{element}', dependencies=[Depends(require_admin)])
async def delete_element(type: str, element: str):
    # capture preset names before the DB cascade removes them
    presets = db.get_preset_names(type, element)
    success = db.delete_element(type, element)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to delete element")
    # remove the preview gifs for all the presets too (best-effort)
    for preset in presets:
        preview_path(type, element, preset['name']).unlink(missing_ok=True)
    return {"message": "Element deleted successfully"}

# add new element
@router.post('/api/add-element/{type}/{element}', dependencies=[Depends(require_admin)])
async def add_element(type: str, element: str):
    success = db.add_element(type, element)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to add element")
    return {"message": "Element added successfully"}

# toggle the active state of a generator or effect
@router.post('/api/toggle-element-active/{type}/{element}', dependencies=[Depends(require_admin)])
async def toggle_element_active(type: str, element: str):
    success = db.toggle_element_active(type, element)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to toggle element active")
    return {"message": "Toggled element active successfully"}

# load a given preset in the state
@router.post('/api/load/{type}/{preset}/{channel}/{effectIndex}/{element}')
async def load(
    type: str,
    preset: str,
    channel: ChannelKey,
    effectIndex: int,
    element: str,
):
    preset_data = db.get_preset(type, element, preset)
    if type == 'generator':
        if channel not in state:
            this_channel = {
                "IO": False,
                "brightness": 1.0,
                "fade": 0.0,
                "numberOfEffects": 0
            }
            state_manager.load_generator(channel, preset_data, this_channel)
        else:
            state_manager.load_generator(channel, preset_data)
    elif type == 'effect':
        with state.lock:
            count = state[channel]['numberOfEffects']
        if effectIndex > count:
            raise HTTPException(status_code=422, detail=f'effect slot {effectIndex} is past the end ({count} effects)')
        state_manager.load_effect(channel, effectIndex, preset_data)
    elif type == 'channel':
        state_manager.load_channel(channel, preset_data)
    elif type == 'global':
        state_manager.load_global(preset_data)

    await connection_manager.update_state()
    return {'message': f'{type} loaded successfully'}

# save a new preset in the database
@router.post('/api/save/', dependencies=[Depends(require_admin)])
async def save(
    preset: str = Form(...),
    type: str = Form(...),
    channel: ChannelKey = Form(...),
    index: int = Form(...),
    preview: UploadFile = File(None),
    force: bool = Form(False),
):
    # Determine the correct element name based on type
    element = 'presets'  # default for channel and global
    if type == 'generator':
        element = state[channel]['generator']['name']
    elif type == 'effect':
        element = state[channel][index]['name']

    if not force and db.preset_exists(type, element, preset):
        return JSONResponse(
            status_code=409,  # Conflict
            content={"message": f"Preset '{preset}' already exists"}
        )

    if type == 'channel':
        data = dict(state[channel])
        data['IO'] = True
    elif type == 'global':
        data = dict(state)
    elif type == 'generator':
        data = dict(state[channel]['generator'])
    elif type == 'effect':
        data = dict(state[channel][index])

    db.save_preset(type, element, preset, data)

    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)

    if preview:
        file_path = preview_path(type, element, preset)
        with open(file_path, "wb") as buffer:
            buffer.write(await preview.read())

    return {"message": "Preset saved successfully"}


# --- live state ------------------------------------------------------------------

# update a global key
@router.post('/api/update-global-key/{key}/{value}')
async def update_global_key(
    key: FaderKey,
    value: FaderValue,
):
    state_manager.update_global_key(key, value)
    await connection_manager.update_key(key)
    return {'message': f'Global key {key} updated to {value}'}

# update a channel key
@router.post('/api/update-channel-key/{channelIndex}/{key}/{value}')
async def update_channel_key(
    channelIndex: ChannelIndex,
    key: FaderKey,
    value: FaderValue,
):
    state_manager.update_channel_key(channelIndex, key, value)
    await connection_manager.update_key(key, channelIndex)
    return {'message': f'Channel {channelIndex} key {key} updated to {value}'}

@router.post('/api/toggle-channel-key/{channelIndex}/{key}')
async def toggle_channel_key(
    channelIndex: ChannelIndex,
    key: ToggleKey,
):
    state_manager.toggle_channel_key(channelIndex, key)
    await connection_manager.update_key(key, channelIndex)
    return {'message': f'Channel {channelIndex} key {key} toggled'}

# remove an effect or a channel
@router.delete('/api/remove/{type}/{channelIndex}/{effectIndex}')
async def remove(
    type: str,
    channelIndex: ChannelKey,
    effectIndex: int,
):
    if type == 'channel':
        with state.lock:
            if state['numberOfChannels'] == 1:
                return {'message': 'Cannot delete the only channel'}
        state_manager.remove_channel(channelIndex)
    if type == 'effect':
        state_manager.remove_effect(channelIndex, effectIndex)
    await connection_manager.update_state()
    return {'message': type + ' deleted'}

# copy a channel
@router.post('/api/copychannel/{channel}')
async def copychannel(
    channel: int,
):
    state_manager.copy_channel(channel)
    await connection_manager.update_state()
    return {'message': 'Channel copied'}

# move a channel
@router.post('/api/movechannel/{from_index}/{to_index}')
async def movechannel(
    from_index: int,
    to_index: int,
):
    state_manager.move_channel(from_index, to_index)
    await connection_manager.update_state()
    return {'message': 'Channel moved'}

# move an effect
@router.post('/api/moveeffect/{channelIndex}/{fromIndex}/{toIndex}')
async def moveeffect(
    channelIndex: ChannelKey,
    fromIndex: int,
    toIndex: int,
):
    state_manager.move_effect(channelIndex, fromIndex, toIndex)
    await connection_manager.update_state()
    return {'message': 'Effect moved'}

# copy an effect
@router.post('/api/copyeffect/{from_channel}/{from_effectIndex}/{to_channel}/{to_effectIndex}')
async def copyeffect(
    from_channel: ChannelKey,
    from_effectIndex: int,
    to_channel: ChannelKey,
    to_effectIndex: int,
):
    state_manager.copy_effect(from_channel, from_effectIndex, to_channel, to_effectIndex)
    await connection_manager.update_state()
    return {'message': 'Effect copied'}

# toggle an effect
@router.post('/api/toggleeffect/{channelIndex}/{effectIndex}')
async def toggleeffect(
    channelIndex: ChannelKey,
    effectIndex: int,
):
    state_manager.toggle_effect(channelIndex, effectIndex)
    await connection_manager.update_element(channelIndex, effectIndex)
    return {'message': 'Effect toggled'}

# select a new context for the midi-controller
@router.post('/api/select/{contextIndex}/{channelIndex}/{elementIndex}')
async def select(
    contextIndex: int,
    channelIndex: Section,
    elementIndex: Slot,
):
    state_manager.update_context(contextIndex, channelIndex, elementIndex)
    await connection_manager.update_key('context')
    return {"message": "Selected"}

# toggle autopilot
@router.post('/api/toggle-autopilot')
async def toggle_autopilot():
    state_manager.toggle_autopilot()
    await connection_manager.update_key('autopilot')
    return {"message": "Autopilot toggled"}

# change autopilot mode
@router.post('/api/autopilot-mode/{mode}')
async def autopilot_mode(
    mode: str,
):
    state_manager.autopilot_mode(mode)
    await connection_manager.update_key('random')
    return {"message": "Autopilot mode changed"}

# trigger randomizer
@router.post('/api/trigger-randomizer/{mode}')
async def trigger_randomizer(
    mode: str,
):
    state_manager.save_state_for_undo()

    randomizer_queue.put(mode)
    return {"message": "Randomizer triggered"}

# randomize color for a channel
@router.post('/api/randomize-color/{channelIndex}')
async def randomize_color(
    channelIndex: ChannelKey,
):
    state_manager.save_state_for_undo()
    randomizer_queue.put(('color', channelIndex))
    return {"message": "Randomizer triggered"}

@router.post('/api/undo-random')
async def undo_random():
    state_manager.undo_last_change()
    await connection_manager.update_state()
    return {"message": "Last randomization undone"}

# toggle sending data to Arduino
@router.post('/api/toggle-cube')
async def toggle_cube():
    state_manager.toggle_cube()
    await connection_manager.update_key('IO')
    return {"message": "Sending to Arduino toggled"}

# normalize s2l
@router.post('/api/normalize-s2l')
async def normalize_s2l():
    state_manager.normalize_s2l()
    await connection_manager.update_key('s2l_normalize')
    return {"message": "s2l normalized"}

# turn the automatic rescaling on or off
@router.post('/api/toggle-auto-normalize')
async def toggle_auto_normalize():
    state_manager.toggle_auto_normalize()
    await connection_manager.update_key('s2l_auto_normalize')
    return {"message": "auto normalize toggled"}

# fire a oneshot in s2l
@router.post('/api/oneshot/{oneshotIndex}')
async def oneshot(
    oneshotIndex: int,
):
    state_manager.fire_oneshot(oneshotIndex)
    # the rendering engine will notify the frontend
    return {"message": "Oneshot fired"}


# --- gradients and the color manager ---------------------------------------------

# load a gradient from DB
@router.post('/api/load-gradient/{gradientId}/{channelIndex}')
async def load_gradient(gradientId: int, channelIndex: ChannelKey):
    gradient_data = db.get_gradient_by_id(gradientId)
    if gradient_data is None:
        raise HTTPException(status_code=404, detail=f'no gradient with id {gradientId}')
    color_data = ({
        'gradient': json.loads(gradient_data),
        'gradientType': 'linear',
        'speed': 0,
        'sectionStart': 0,
        'sectionWidth': 100,
        'rotateSpeedY': 0,
        'rotateSpeedZ': 0,
        'soundToLightOptions': []
    })
    return await update_color_manager(channelIndex, color_data)

# update color manager settings
@router.post('/api/color-manager/{channel}')
async def update_color_manager(channel: ChannelKey, color_data: dict):
    state_manager.update_color_manager(channel, color_data)
    await connection_manager.update_element(channel, 'color')

    return {"message": "Color manager updated successfully"}

# load all gradients in UI
@router.get('/api/get-gradient-presets')
async def get_gradient_presets():
    return db.get_all_gradients()

# save a custom gradient to DB
@router.post('/api/save-gradient', dependencies=[Depends(require_admin)])
async def save_gradient(request: Request):
    data = await request.json()
    subtype = data.get('subtype')
    gradient_data = data.get('gradientString')

    db.save_gradient('custom', gradient_data, subtype)
    return {"message": "Gradient saved successfully"}

# delete a gradient from DB
@router.delete('/api/delete-gradient/{id}', dependencies=[Depends(require_admin)])
async def delete_gradient(id: int):
    success = db.delete_gradient(id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to delete gradient")
    return {"message": "Gradient deleted successfully"}

# clear the gradient object from a channel
@router.post('/api/clear-gradient/{channelIndex}')
async def clear_gradient(channelIndex: ChannelKey):
    state_manager.clear_gradient(channelIndex)
    await connection_manager.update_state()
    return {"message": "Gradient cleared successfully"}


# --- system ------------------------------------------------------------------------

# serve the mobile application
@router.get("/mobile")
async def mobile_app():
    print("Serving mobile app")
    dist_path = os.path.join(os.path.dirname(__file__), "..", "mobile", "dist")
    return FileResponse(f"{dist_path}/index.html")


# update the full state in the frontend
@router.get("/api/get-state")
async def get_present_state():
    await connection_manager.update_state()
