from fastapi import FastAPI, Request

from routers import bedrock_router
import logging
import os

## Global Variables
__current_dir__ = os.path.dirname(os.path.realpath(__file__))

## fastapi app
app = FastAPI(
    title="Bedrock Client", description="Test Bedrock Client", version="0.1.0"
)

# Import routers
app.include_router(bedrock_router)