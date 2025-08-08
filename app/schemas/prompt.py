from pydantic import BaseModel


class PromptRequest(BaseModel):
    topic: str


class PromptResponse(BaseModel):
    prompt: str
    video_url: str | None = None
