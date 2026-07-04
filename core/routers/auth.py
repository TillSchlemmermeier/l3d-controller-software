"""Admin-token auth for destructive endpoints.

The operator UI sends a shared secret in the `X-Admin-Token` header. Guest
clients (mobile phones) never have it, so they can tweak visuals but cannot
delete / save / mutate the persistent store. The token is read from the
L3D_ADMIN_TOKEN environment variable, which the Electron app passes through
from its .env (see electron/main.ts).

Fails closed: if no token is configured, admin operations are refused rather
than left open.
"""
import os
import secrets

from fastapi import Header, HTTPException

ADMIN_TOKEN = os.environ.get("L3D_ADMIN_TOKEN", "")


def require_admin(x_admin_token: str = Header(default="")):
    if not ADMIN_TOKEN:
        raise HTTPException(status_code=503, detail="Admin operations disabled: L3D_ADMIN_TOKEN not set")
    if not secrets.compare_digest(x_admin_token, ADMIN_TOKEN):
        raise HTTPException(status_code=401, detail="Invalid or missing admin token")
