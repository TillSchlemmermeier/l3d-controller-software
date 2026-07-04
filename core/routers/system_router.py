from typing import Optional
from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
import os

from routers.auth import require_admin

router = APIRouter()

@router.get("/")
async def root():
  return {"message": "Hello World"}


# serve the mobile application
@router.get("/mobile", response_class=HTMLResponse)
async def mobile_app():
    print("Serving mobile app")
    dist_path = os.path.join(os.path.dirname(__file__), "..", "..", "mobile","dist")
    return FileResponse(f"{dist_path}/index.html")


# validate all presets
@router.get('/api/validate-presets', dependencies=[Depends(require_admin)])
async def validate_presets():
    try:
        from preset_validator import PresetValidator
        
        validator = PresetValidator()
        validation_results = validator.validate_all()
        
        return JSONResponse(
            status_code=200,
            content=validation_results
        )
        
    except Exception as e:
        print(f"Error validating presets: {e}")
        return JSONResponse(
            status_code=500,
            content={"message": f"Error validating presets: {str(e)}"}
        )


# update the cube data in the frontend with JSON (legacy function)
@router.get('/api/update_cube')
async def update_cube(request: Request):
    connection_manager = request.app.state.connection_manager

    await connection_manager.update_cube()
    return {"status": "ok"}


# update the full state in the frontend
@router.get("/api/get-state")
async def get_present_state(request: Request):
    connection_manager = request.app.state.connection_manager

    await connection_manager.update_state()


# update the value of a single element in the frontend
@router.get('/api/update_element/{channel}/{element}')
async def update_element(channel: int, element: int, request: Request):
    connection_manager = request.app.state.connection_manager

    await connection_manager.update_element(channel, element)
    return {"status": "ok"}


# update the value of a single key in the frontend
@router.get("/api/update_key/{key}")
async def update_key(key: str, request: Request, channel: Optional[int] = None):
    connection_manager = request.app.state.connection_manager

    await connection_manager.update_key(key, channel)
    return {"status": "ok"}
