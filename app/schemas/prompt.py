from pydantic import BaseModel

class PromptRequest(BaseModel):
    topic: str  # тема для генерації промта, наприклад "Барселона на світанку"

class PromptResponse(BaseModel):
    prompt: str  # готовий промт для генерації відео
