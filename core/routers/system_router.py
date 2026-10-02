from fastapi import APIRouter, Request
from fastapi.responses import FileResponse
import os

router = APIRouter()

# serve the mobile application
@router.get("/mobile")
async def mobile_app():
    print("Serving mobile app")
    dist_path = os.path.join(os.path.dirname(__file__), "..", "..", "mobile","dist")
    return FileResponse(f"{dist_path}/index.html")


# update the full state in the frontend
@router.get("/api/get-state")
async def get_present_state(request: Request):
    connection_manager = request.app.state.connection_manager

    await connection_manager.update_state()
