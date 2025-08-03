from fastapi import FastAPI
from app.schemas.prompt import PromptRequest, PromptResponse
from app.services.openai_service import generate_video_prompt
from app.utils.prompt_utils import clean_prompt

app = FastAPI()


@app.post("/generate-prompt", response_model=PromptResponse)
def create_prompt(request: PromptRequest):
    raw_prompt = generate_video_prompt(request.topic)
    cleaned_prompt = clean_prompt(raw_prompt, max_words=60)
    return PromptResponse(prompt=cleaned_prompt)
