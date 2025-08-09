import os
import time
import requests
import logging
from dotenv import load_dotenv
from runwayml import RunwayML

# Завантаження змінних середовища
load_dotenv()
# client = RunwayML()

RUNWAY_API_KEY = os.getenv("RUNWAY_API_KEY")
# RUNWAY_API_KEY = 'key_541ccb0d60d11fc723a9a9e7b8831dc36a535b634ed8a0e7ec09be3b09e68509878f5cb14dd853bb4ff982cafe6f47e71cd7732b67ebb00355b8f67a93216ee8'
if not RUNWAY_API_KEY:
    raise RuntimeError("❌ RUNWAY_API_KEY not found in environment variables")

RUNWAY_API_URL = "https://api.dev.runwayml.com/v1/text_to_image"

POST_HEADERS = {
    "Authorization": f"Bearer {RUNWAY_API_KEY}",
    "Content-Type": "application/json",
    "X-Runway-Version": "2024-11-06"
}

GET_HEADERS = {
    "Authorization": f"Bearer {RUNWAY_API_KEY}",
    "Content-Type": "application/json",
    "X-Runway-Version": "2024-11-06"
}


def send_to_runway(prompt: str, ratio: str = "720:1280", model: str = "gen4_image") -> str:
    print('!!!!!', prompt)
    logging.info(f"[RUNWAY] Sending prompt: {prompt!r}")
    payload = {
        "model": model,
        "promptText": prompt,
        "ratio": ratio

    }
    response = requests.post(RUNWAY_API_URL, headers=POST_HEADERS, json=payload)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logging.error(f"[RUNWAY] HTTP error occurred: {e}")
        logging.error(f"[RUNWAY] Response status code: {response.status_code}")
        logging.error(f"[RUNWAY] Response body: {response.text}")
        raise

    data = response.json()
    task_id = data.get("id")
    logging.info(f"[RUNWAY] Task created with ID: {task_id}")
    print(f"https://api.dev.runwayml.com/v1/tasks/{task_id}")
    return task_id


def check_runway_status(task_id: str, poll_interval: int = 5) -> dict:
    """Перевіряє статус задачі на Runway до завершення."""
    url = f"https://api.dev.runwayml.com/v1/tasks/{task_id}"

    while True:
        response = requests.get(url, headers=GET_HEADERS)

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logging.error(f"[RUNWAY] HTTP error occurred: {e}")
            logging.error(f"[RUNWAY] Response status code: {response.status_code}")
            logging.error(f"[RUNWAY] Response body: {response.text}")
            raise

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
