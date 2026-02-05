import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from openapi.{{ cookiecutter.service_name }}.main import app
import services.{{ cookiecutter.service_name }}.api
from services.{{ cookiecutter.service_name }}.conf.settings import settings
from libs.mongodb.client import MongoManager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    MongoManager.connect(settings.mongodb_uri)
    yield
    # Shutdown
    MongoManager.close()


# Attach lifespan to the existing app
app.router.lifespan_context = lifespan

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
