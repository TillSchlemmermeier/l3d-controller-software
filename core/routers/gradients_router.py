from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
import json

from routers.auth import require_admin

router = APIRouter()

# load a gradient from DB
@router.post('/api/load-gradient/{gradientId}/{channelIndex}')
async def load_gradient(gradientId: int, channelIndex: int, request: Request):
    db = request.app.state.db

    gradient_data = db.get_gradient_by_id(gradientId)
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
    return await update_color_manager(channelIndex, color_data, request)

# update color manager settings
@router.post('/api/color-manager/{channel}')
async def update_color_manager(channel: int, color_data: dict, request: Request):
    state_manager = request.app.state.state_manager
    connection_manager = request.app.state.connection_manager

    state_manager.update_color_manager(channel, color_data)
    await connection_manager.update_element(channel, 8)

    return JSONResponse(
        status_code=200,
        content={"message": "Color manager updated successfully"}
    )

# load all gradients in UI
@router.get('/api/get-gradient-presets')
async def get_gradient_presets(request: Request):
    db = request.app.state.db

    gradients = db.get_all_gradients()
    return JSONResponse(content=gradients)

# save a custom gradient to DB
@router.post('/api/save-gradient', dependencies=[Depends(require_admin)])
async def save_gradient(request: Request):
    db = request.app.state.db

    data = await request.json()
    subtype = data.get('subtype')
    gradient_data = data.get('gradientString')

    success = db.save_gradient('custom', gradient_data, subtype)
    if success:
        return JSONResponse(status_code=200, content={"message": "Gradient saved successfully"})
    else:
        return JSONResponse(status_code=400, content={"message": "Failed to save gradient"})

# delete a gradient from DB
@router.delete('/api/delete-gradient/{id}', dependencies=[Depends(require_admin)])
async def delete_gradient(id: int, request: Request):
    db = request.app.state.db

    success = db.delete_gradient(id)
    if success:
        return JSONResponse(status_code=200, content={"message": "Gradient deleted successfully"})
    else:
        return JSONResponse(status_code=400, content={"message": "Failed to delete gradient"})

# clear the gradient object from a channel
@router.post('/api/clear-gradient/{channelIndex}')
async def clear_gradient(channelIndex: int, request: Request):
    state_manager = request.app.state.state_manager
    connection_manager = request.app.state.connection_manager

    state_manager.clear_gradient(channelIndex)
    await connection_manager.update_state()
    return JSONResponse(status_code=200, content={"message": "Gradient cleared successfully"})