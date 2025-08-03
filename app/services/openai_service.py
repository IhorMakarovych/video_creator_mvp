import os
from openai import OpenAI
from dotenv import load_dotenv
from app.utils.prompt_utils import clean_prompt

# Завантажуємо .env
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("❌ OPENAI_API_KEY not found in environment variables")

client = OpenAI(api_key=api_key)


def generate_video_prompt(topic: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an assistant that generates short, cinematic video prompts for AI video generation."},
            {"role": "user", "content": f"Generate a video prompt for: {topic}"}
        ],
        max_tokens=120,
        temperature=0.7,
        top_p=1.0,
        frequency_penalty=0.2,
        presence_penalty=0.2
    )

    raw_prompt = response.choices[0].message.content
    return clean_prompt(raw_prompt)
