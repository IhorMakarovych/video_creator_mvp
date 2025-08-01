# Video Creator MVP

Простий веб-додаток на Python з FastAPI для генерації відео за допомогою AI.

## Опис

Проєкт дозволяє:
- Створювати текстові промти через інтеграцію з ChatGPT;
- Генерувати відео на основі промтів через Runway API;
- Зберігати відео локально;
- (Планується) викладати відео на YouTube.

## Технології

- Python 3.11+
- FastAPI
- SQLAlchemy (або інша ORM)
- Pydantic для валідації даних
- Runway API
- OpenAI API

## Запуск проєкту локально

1. Клонувати репозиторій:
   ```bash
   git clone https://github.com/IhorMakarovych/video_creator_mvp.git
   cd video_creator_mvp
   
2. Встановити віртуальне середовище і залежності:
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   pip install -r requirements.txt

3. Створити файл .env на основі .env.example і додати ключі API.

4. Запустити додаток:
   uvicorn app.main:app --reload

5. Відкрити у браузері:
   http://localhost:8000
