from fastapi import FastAPI
from app.schemas.prompt import PromptRequest, PromptResponse
from app.services.openai_service import generate_video_prompt
from app.services.runway_service import send_to_runway, check_runway_status
from app.utils.prompt_utils import clean_prompt
import logging

app = FastAPI()


@app.post("/generate-video", response_model=PromptResponse)
def create_video(request: PromptRequest):
    # 1. Генеруємо промт
    raw_prompt = generate_video_prompt(request.topic)
    cleaned_prompt = clean_prompt(raw_prompt, max_words=60)

    # 2. Відправляємо до Runway
    task_id = send_to_runway(cleaned_prompt)

    # 3. Чекаємо завершення
    result = check_runway_status(task_id)

    # 4. Повертаємо промт і посилання на відео
    return PromptResponse(prompt=cleaned_prompt, video_url=result.get("output_url"))
