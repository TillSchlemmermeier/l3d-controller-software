from fastapi import APIRouter, Request, Depends
from randomizer import Randomizer

router = APIRouter()

# Dependency functions
def get_state_manager(request: Request):
    return request.app.state.state_manager

def get_connection_manager(request: Request):
    return request.app.state.connection_manager

def get_cube_state(request: Request):
    return request.app.state.cube_state

# update a global key
@router.get('/api/update-global-key/{key}/{value}')
async def update_global_key(
    key: str, 
    value: float,
    state_manager = Depends(get_state_manager),
    connection_manager = Depends(get_connection_manager)
):
    state_manager.update_global_key(key, value)
    await connection_manager.update_key(key)
    return {'message': f'Global key {key} updated to {value}'}

# update a channel key
@router.get('/api/update-channel-key/{channelIndex}/{key}/{value}')
async def update_channel_key(
    channelIndex: int, 
    key: str, 
    value: float,
    state_manager = Depends(get_state_manager),
    connection_manager = Depends(get_connection_manager)
):
    state_manager.update_channel_key(channelIndex, key, value)
    await connection_manager.update_key(key, channelIndex)
    return {'message': f'Channel {channelIndex} key {key} updated to {value}'}

@router.get('/api/toggle-channel-key/{channelIndex}/{key}')
async def toggle_channel_key(
    channelIndex: int, 
    key: str, 
    state_manager = Depends(get_state_manager),
    connection_manager = Depends(get_connection_manager)
):
    state_manager.toggle_channel_key(channelIndex, key)
    await connection_manager.update_key(key, channelIndex)
    return {'message': f'Channel {channelIndex} key {key} toggled'}

# remove an effect or a channel
@router.get('/api/remove/{type}/{channelIndex}/{effectIndex}')
async def remove(
    type: str, 
    channelIndex: int, 
    effectIndex: int,
    state_manager = Depends(get_state_manager),
    connection_manager = Depends(get_connection_manager),
    state = Depends(get_cube_state)
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
@router.get('/api/copychannel/{channel}')
async def copychannel(
    channel: int,
    state_manager = Depends(get_state_manager),
    connection_manager = Depends(get_connection_manager)
):
    state_manager.copy_channel(channel)
    await connection_manager.update_state()
    return {'message': 'Channel copied'}

# move a channel
@router.get('/api/movechannel/{from_index}/{to_index}')
async def movechannel(
    from_index: int, 
    to_index: int,
    state_manager = Depends(get_state_manager),
    connection_manager = Depends(get_connection_manager)
):
    state_manager.move_channel(from_index, to_index)
    await connection_manager.update_state()
    return {'message': 'Channel moved'}

# move an effect
@router.get('/api/moveeffect/{channelIndex}/{fromIndex}/{toIndex}')
async def moveeffect(
    channelIndex: int, 
    fromIndex: int, 
    toIndex: int,
    state_manager = Depends(get_state_manager),
    connection_manager = Depends(get_connection_manager)
):
    state_manager.move_effect(channelIndex, fromIndex, toIndex)
    await connection_manager.update_state()
    return {'message': 'Effect moved'}

# copy an effect
@router.get('/api/copyeffect/{from_channel}/{from_effectIndex}/{to_channel}/{to_effectIndex}')
async def copyeffect(
    from_channel: int, 
    from_effectIndex: int, 
    to_channel: int, 
    to_effectIndex: int,
    state_manager = Depends(get_state_manager),
    connection_manager = Depends(get_connection_manager)
):
    state_manager.copy_effect(from_channel, from_effectIndex, to_channel, to_effectIndex)
    await connection_manager.update_state()
    return {'message': 'Effect copied'}

# toggle an effect
@router.get('/api/toggleeffect/{channelIndex}/{effectIndex}')
async def toggleeffect(
    channelIndex: int, 
    effectIndex: int,
    state_manager = Depends(get_state_manager),
    connection_manager = Depends(get_connection_manager)
):
    state_manager.toggle_effect(channelIndex, effectIndex)
    await connection_manager.update_element(channelIndex, effectIndex)
    return {'message': 'Effect toggled'}

# select a new context for the midi-controller
@router.get('/api/select/{contextIndex}/{channelIndex}/{elementIndex}')
async def select(
    contextIndex: int, 
    channelIndex: int, 
    elementIndex: int,
    state_manager = Depends(get_state_manager),
    connection_manager = Depends(get_connection_manager)
):
    state_manager.update_context(contextIndex, channelIndex, elementIndex)
    await connection_manager.update_state()
    return {"message": "Selected"}

# toggle autopilot
@router.get('/api/toggle-autopilot')
async def toggle_autopilot(
    state_manager = Depends(get_state_manager),
    connection_manager = Depends(get_connection_manager)
):
    state_manager.toggle_autopilot()
    await connection_manager.update_state()
    return {"message": "Autopilot toggled"}

# change autopilot mode
@router.get('/api/autopilot-mode/{mode}')
async def autopilot_mode(
    mode: str,
    state_manager = Depends(get_state_manager),
    connection_manager = Depends(get_connection_manager)
):
    state_manager.autopilot_mode(mode)
    await connection_manager.update_state()
    return {"message": "Autopilot mode changed"}

# trigger randomizer
@router.get('/api/trigger-randomizer')
async def trigger_randomizer(
    state_manager = Depends(get_state_manager),
    connection_manager = Depends(get_connection_manager),
    state = Depends(get_cube_state)
):
    state_manager.save_state_for_undo() 
    Randomizer(state).trigger()
    await connection_manager.update_state()
    return {"message": "Randomizer triggered"}

# randomize color for a channel
@router.get('/api/randomize-color/{channelIndex}')
async def randomize_color(
    channelIndex: int,
    state_manager = Depends(get_state_manager),
    connection_manager = Depends(get_connection_manager),
    state = Depends(get_cube_state)
):
    state_manager.save_state_for_undo()
    Randomizer(state)._randomize_color(channelIndex)
    await connection_manager.update_state()
    return {"message": "Randomizer triggered"}

@router.get('/api/undo-random')
async def undo_random(
    state_manager = Depends(get_state_manager),
    connection_manager = Depends(get_connection_manager)
):
    state_manager.undo_last_change()
    await connection_manager.update_state()
    return {"message": "Last randomization undone"}

# toggle sending data to Arduino
@router.get('/api/toggle-cube')
async def toggle_cube(
    state_manager = Depends(get_state_manager),
    connection_manager = Depends(get_connection_manager)
):
    state_manager.toggle_cube()
    await connection_manager.update_state()
    return {"message": "Sending to Arduino toggled"}

# normalize s2l
@router.get('/api/normalize-s2l')
async def normalize_s2l(
    state_manager = Depends(get_state_manager),
    connection_manager = Depends(get_connection_manager)
):
    state_manager.normalize_s2l()
    await connection_manager.update_state()
    return {"message": "s2l normalized"}

# fire a oneshot in s2l
@router.get('/api/oneshot/{oneshotIndex}')
async def oneshot(
    oneshotIndex: int,
    state_manager = Depends(get_state_manager)
):
    state_manager.fire_oneshot(oneshotIndex)
    return {"message": "Oneshot fired"}