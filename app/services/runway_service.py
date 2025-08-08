import os
import time
import requests
import logging
from dotenv import load_dotenv

# Завантаження змінних середовища
load_dotenv()

RUNWAY_API_KEY = os.getenv("RUNWAY_API_KEY")
# RUNWAY_API_KEY = 'key_541ccb0d60d11fc723a9a9e7b8831dc36a535b634ed8a0e7ec09be3b09e68509878f5cb14dd853bb4ff982cafe6f47e71cd7732b67ebb00355b8f67a93216ee8'
if not RUNWAY_API_KEY:
    raise RuntimeError("❌ RUNWAY_API_KEY not found in environment variables")

RUNWAY_API_URL = "https://api.dev.runwayml.com/v1/video/generations"

HEADERS = {
    "Authorization": f"Bearer {RUNWAY_API_KEY}",
    "Content-Type": "application/json"
}


def send_to_runway(prompt: str, aspect_ratio: str = "16:9", duration: int = 5) -> str:
    """Відправляє промт на Runway і повертає ID задачі."""
    logging.info(f"[RUNWAY] Sending prompt: {prompt!r}")
    payload = {
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "duration": duration
    }
    response = requests.post(RUNWAY_API_URL, headers=HEADERS, json=payload)
    response.raise_for_status()
    data = response.json()

    task_id = data.get("id")
    logging.info(f"[RUNWAY] Task created with ID: {task_id}")
    return task_id


def check_runway_status(task_id: str, poll_interval: int = 5) -> dict:
    """Перевіряє статус задачі на Runway до завершення."""
    url = f"https://api.runwayml.com/v1/tasks/{task_id}"

    while True:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()

        status = data.get("status")
        logging.info(f"[RUNWAY] Task {task_id} status: {status}")

        if status == "completed":
            logging.info(f"[RUNWAY] Task {task_id} completed successfully")
            return data
        elif status in ("failed", "canceled"):
            logging.error(f"[RUNWAY] Task {task_id} failed with status: {status}")
            raise RuntimeError(f"Runway generation failed: {status}")

        time.sleep(poll_interval)
