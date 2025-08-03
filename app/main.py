from fastapi import FastAPI
from app.schemas.prompt import PromptRequest, PromptResponse
from app.services.openai_service import generate_video_prompt

app = FastAPI()

@app.post("/generate-prompt", response_model=PromptResponse)
def create_prompt(request: PromptRequest):
    prompt = generate_video_prompt(request.topic)
    return PromptResponse(prompt=prompt)

