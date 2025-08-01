from fastapi import FastAPI, HTTPException
from app.schemas.video import VideoRequest
from app.services import openai_service, youtube_service
from app.utils.file_manager import save_video_to_disk

app = FastAPI()


@app.post("/generate/")
async def generate_video(data: VideoRequest):
    try:
        script_text = openai_service.generate_script(data.prompt)
        audio_path = openai_service.text_to_speech(script_text)
        images = youtube_service.fetch_images(data.prompt)
        video_path = save_video_to_disk(images, audio_path, data.title)
        return {"message": "Video generated successfully", "path": video_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
