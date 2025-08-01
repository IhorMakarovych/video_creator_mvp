from pydantic import BaseModel, Field, HttpUrl
from typing import Optional


class VideoRequest(BaseModel):
    script: str = Field(..., description="Текст сценарію відео")
    duration_seconds: Optional[int] = Field(60, description="Бажана тривалість відео в секундах")
    language: Optional[str] = Field("en", description="Мова озвучення (en, es, uk, etc.)")
    music_url: Optional[HttpUrl] = Field(None, description="Опціональний URL для фонової музики")
