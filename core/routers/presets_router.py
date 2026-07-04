from pathlib import Path

from fastapi import APIRouter, Request, Form, File, UploadFile, Depends, HTTPException
from fastapi.responses import JSONResponse

from routers.auth import require_admin

router = APIRouter()

# Preview GIFs live here
PREVIEW_DIR = (Path(__file__).resolve().parents[2] / "src/assets/previews").resolve()

# Resolve and traversal-check a preset's preview gif
def preview_path(type: str, element: str, preset: str) -> Path:
    prefix = type if type in ('channel', 'global') else element
    path = (PREVIEW_DIR / f"{prefix}_p_{preset}.gif").resolve()
    if path.parent != PREVIEW_DIR:
        raise HTTPException(status_code=400, detail="Invalid preset or element name")
    return path

# Dependency functions
def get_db(request: Request):
    return request.app.state.db

def get_state_manager(request: Request):
    return request.app.state.state_manager

def get_connection_manager(request: Request):
    return request.app.state.connection_manager

def get_cube_state(request: Request):
    return request.app.state.cube_state

# get a list with all the available generators or effects
@router.get('/api/get-element-names/{type}')
async def get_names(type: str, db = Depends(get_db)):
    element_names = db.get_element_names(type)
    return JSONResponse(content=element_names)

# get a list with all the active generators or effects
@router.get('/api/get-active-elements/{type}')
async def get_active_elements(type: str, db = Depends(get_db)):
    active_elements = db.get_active_elements(type)
    return JSONResponse(content=active_elements)

# get all the information available in the database for a generator or effect
@router.get('/api/get-element-info/{type}/{element_name}')
async def get_element_info(type: str, element_name: str, db = Depends(get_db)):
    element = db.get_element_info(type, element_name)
    return JSONResponse(content=element)

# get a list with all the preset names and types for an element
@router.get('/api/get-all-presets/{type}/{element_name}')
async def get_all_presets(type: str, element_name: str, db = Depends(get_db)):
    presets = db.get_all_presets(type, element_name)
    return JSONResponse(content=presets)

# get a list with all the preset names for a given generator or effect
@router.get('/api/get-presets/{type}/{element_name}')
async def get_presets(type: str, element_name: str, db = Depends(get_db)):
    presets = db.get_preset_names(type, element_name)
    return JSONResponse(content=presets)

# get all the information available in the database for a given preset
@router.get('/api/get-preset-info/{type}/{element}/{preset}')
async def get_preset_info(type: str, element: str, preset: str, db = Depends(get_db)):
    preset_data = db.get_preset_info(type, element, preset)
    return JSONResponse(content=preset_data)

# rename a given preset in the db and in the filesystem
@router.post('/api/rename-preset/{type}/{element}/{old_preset}/{new_preset}', dependencies=[Depends(require_admin)])
async def rename_preset(
    type: str, 
    element: str, 
    old_preset: str, 
    new_preset: str, 
    db = Depends(get_db)
):
    # build (and traversal-check) both paths before mutating the DB
    old_file_path = preview_path(type, element, old_preset)
    new_file_path = preview_path(type, element, new_preset)

    success = db.rename_preset(type, element, old_preset, new_preset)
    if not success:
        return JSONResponse(
            status_code=400,
            content={"message": "Failed to rename preset"}
        )
    if old_file_path.exists():
        old_file_path.rename(new_file_path)
        return JSONResponse(
            status_code=200,
            content={"message": "Preset renamed successfully"}
        )
    else:
        return JSONResponse(
            status_code=400,
            content={"message": "Failed to rename preset"}
        )

# delete preset
@router.delete('/api/delete-preset/{type}/{element}/{preset}', dependencies=[Depends(require_admin)])
async def delete_preset(type: str, element: str, preset: str, db = Depends(get_db)):
    success = db.delete_preset(type, element, preset)
    if not success:
        return JSONResponse(
            status_code=400,
            content={"message": "Failed to delete preset"}
        )
    # remove the preview gif too (best-effort)
    preview_path(type, element, preset).unlink(missing_ok=True)
    return JSONResponse(
        status_code=200,
        content={"message": "Preset deleted successfully"}
    )

# delete element
@router.delete('/api/delete-element/{type}/{element}', dependencies=[Depends(require_admin)])
async def delete_element(type: str, element: str, db = Depends(get_db)):
    # capture preset names before the DB cascade removes them
    presets = db.get_preset_names(type, element)
    success = db.delete_element(type, element)
    if not success:
        return JSONResponse(
            status_code=400,
            content={"message": "Failed to delete element"}
        )
    # remove the preview gifs for all the presets too (best-effort)
    for preset in presets:
        preview_path(type, element, preset['name']).unlink(missing_ok=True)
    return JSONResponse(
        status_code=200,
        content={"message": "Element deleted successfully"}
    )

# add new element
@router.post('/api/add-element/{type}/{element}', dependencies=[Depends(require_admin)])
async def add_element(type: str, element: str, db = Depends(get_db)):
    success = db.add_element(type, element)
    if success:
        return JSONResponse(
            status_code=200,
            content={"message": "Element added successfully"}
        )
    else:
        return JSONResponse(
            status_code=400,
            content={"message": "Failed to add element"}
        )
        
# toggle the active state of a generator or effect
@router.post('/api/toggle-element-active/{type}/{element}', dependencies=[Depends(require_admin)])
async def toggle_element_active(type: str, element: str, db = Depends(get_db)):
    success = db.toggle_element_active(type, element)
    if success:
        return JSONResponse(
            status_code=200,
            content={"message": "Toggled element active successfully"}
        )
    else:
        return JSONResponse(
            status_code=400,
            content={"message": "Failed to toggle element active"}
        )

# load a given preset in the state    
@router.post('/api/load/{type}/{preset}/{channel}/{effectIndex}/{element}')
async def load(
    type: str, 
    preset: str, 
    channel: int, 
    effectIndex: int, 
    element: str,
    db = Depends(get_db),
    state_manager = Depends(get_state_manager),
    connection_manager = Depends(get_connection_manager),
    state = Depends(get_cube_state)
):
    preset_data = db.get_preset(type, element, preset)
    if type == 'generator':
        if channel not in state:
            this_channel = {
                "IO": False,
                "brightness": 1.0,
                "fade": 0.0,
                "update": False,
                9: {"name": "blank"},
                "numberOfEffects": 0
            }
            state_manager.load_generator(channel, preset_data, this_channel)
        else:
            state_manager.load_generator(channel, preset_data)
    elif type == 'effect':
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
    channel: int = Form(...),
    index: int = Form(...),
    preview: UploadFile = File(None),
    force: bool = Form(False),
    db = Depends(get_db),
    state = Depends(get_cube_state)
):
    success = False

    # Determine the correct element name based on type
    element = 'presets'  # default for channel and global
    if type == 'generator':
        element = state[channel][9]['name']
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
        data = dict(state[channel][9])
    elif type == 'effect':
        data = dict(state[channel][index])

    success = db.save_preset(type, element, preset, data)

    if not success:
        return JSONResponse(
            status_code=400,
            content={"message": 'Error saving preset'}
        )

    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)

    if preview:
        file_path = preview_path(type, element, preset)
        with open(file_path, "wb") as buffer:
            buffer.write(await preview.read())

    return JSONResponse(
        status_code=200,
        content={"message": "Preset saved successfully"}
    )