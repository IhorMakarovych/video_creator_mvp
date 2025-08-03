import re

def clean_prompt(prompt: str, max_words: int = 50) -> str:
    if not prompt:
        return ""

    original_prompt = prompt  # на випадок, якщо очистимо все

    # 1. Прибираємо лапки на початку і в кінці
    prompt = prompt.strip().strip('"').strip("'")

    # 2. Видаляємо тільки службові слова на початку, але зберігаємо текст далі
    prompt = re.sub(r'^(Video Prompt|Scene \d*|Scene|Title|Setting|Description)\s*:\s*', '', prompt, flags=re.IGNORECASE)

    # 3. Прибираємо Markdown символи
    prompt = re.sub(r'[\*_#>`]+', '', prompt)

    # 4. Прибираємо подвійні пробіли та перенос рядків
    prompt = re.sub(r'\s+', ' ', prompt)

    # 5. Якщо все вирізалось — повертаємо оригінал
    if not prompt.strip():
        prompt = original_prompt.strip()

    # 6. Обрізаємо по кількості слів
    words = prompt.split()
    if len(words) > max_words:
        prompt = " ".join(words[:max_words])

    # 7. Прибираємо випадкові символи на кінці
    prompt = prompt.rstrip(".,;:-_ ")

    return prompt


