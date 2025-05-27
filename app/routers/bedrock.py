from fastapi import APIRouter
from pydantic import BaseModel, Field
from starlette import status

import os
from client import BedrockClient, ChatRequest

router = APIRouter()

# Create a Bedrock Runtime client in the AWS Region you want to use.
client = BedrockClient(
    region_name=os.getenv("AWS_REGION", "eu-central-1"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

@router.get("/chat/models", status_code=status.HTTP_200_OK)
async def get_models():
    return client.list_foundation_models()

@router.post("/chat/completions", status_code=status.HTTP_200_OK)
async def create_chat_completion(request: ChatRequest, streaming: bool = False):
    model_Id = "anthropic.claude-3-5-sonnet-20240620-v1:0"
    if streaming:
        return client.invoke_model_with_streaming(model_id=model_Id, request=request)
    return client.invoke_model(model_id=model_Id, request=request)