import re

def clean_prompt(prompt: str, max_words: int = 50) -> str:
    if not prompt:
        return ""

    # 1. Прибираємо лапки на початку і в кінці
    prompt = prompt.strip().strip('"').strip("'")

    # 2. Прибираємо Markdown-форматування
    prompt = re.sub(r'[\*_#>`]+', '', prompt)

    # 3. Замінюємо багато пробілів і переносів рядків на один пробіл
    prompt = re.sub(r'\s+', ' ', prompt)

    # 4. Опціонально обмежуємо кількість слів
    words = prompt.split()
    if len(words) > max_words:
        prompt = " ".join(words[:max_words])

    return prompt