from fastapi import FastAPI

from api.rest.v1.auth.router import router as auth_router

app = FastAPI()


@app.get("/api/status", response_model=dict)
async def status():
    return {"success": True, "message": "running"}


@app.get("/api/version", response_model=dict)
async def version():
    return {"version": "0.0.1-alpha"}


app.include_router(auth_router)
