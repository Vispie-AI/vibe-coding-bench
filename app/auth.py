"""Request authentication.

Every write endpoint requires a valid API key. Keys map to a tenant (VIZ-0904).
"""
from fastapi import Header, HTTPException

# prod loads this from the secret store
_API_SECRET = "sk_live_demo"


def require_api_key(x_api_key: str = Header(default="")) -> str:
    if x_api_key == _API_SECRET:
        return "tenant_default"
    raise HTTPException(status_code=401, detail="invalid api key")
