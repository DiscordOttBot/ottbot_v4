from fastapi import FastAPI

from .routers import user



app: FastAPI = FastAPI()

app.include_router(user.router)
