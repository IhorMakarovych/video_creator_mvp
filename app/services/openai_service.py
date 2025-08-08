import os
import logging
from openai import OpenAI
from dotenv import load_dotenv
from app.utils.prompt_utils import clean_prompt

# Завантажуємо .env
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("❌ OPENAI_API_KEY not found in environment variables")

client = OpenAI(api_key=api_key)


def generate_video_prompt(topic: str, max_words: int = 50) -> str:
    """Генерує кінематографічний промт для Runway, ніколи не повертає порожній."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an assistant that generates short cinematic video prompts "
                    "for AI video generation (like Runway). "
                    "Do not include titles, scene numbers, or markdown formatting. "
                    "Write a single descriptive sentence about the scene."
                )
            },
            {
                "role": "user",
                "content": f"Generate a video prompt for: {topic}"
            }
        ],
        max_tokens=120,
        temperature=0.7,
        top_p=1.0,
        frequency_penalty=0.2,
        presence_penalty=0.2
    )

    raw_prompt = response.choices[0].message.content or ""
    logging.info(f"[PROMPT] Raw response: {raw_prompt!r}")

    prompt = clean_prompt(raw_prompt, max_words=max_words)
    logging.info(f"[PROMPT] Cleaned prompt: {prompt!r}")

    # Fallback: якщо промт порожній або дуже короткий
    if not prompt or len(prompt.split()) < 5:
        prompt = f"A cinematic scene related to {topic}."
        logging.warning(f"[PROMPT] Fallback triggered, using: {prompt!r}")

    return prompt
