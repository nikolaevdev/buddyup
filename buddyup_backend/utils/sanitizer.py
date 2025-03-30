# buddyup/utils/sanitizer.py

import bleach
from fastapi import HTTPException

def sanitize_field(value: str) -> str:
    """
    Санитизирует строку с помощью bleach.
    Все HTML-теги удаляются (т.е. разрешается только чистый текст).
    Если очищённая строка отличается от исходной, выбрасывается HTTPException.
    """
    # Разрешаем только текст: никаких тегов, атрибутов или стилей.
    allowed_tags = []  # Никаких тегов не разрешаем
    allowed_attributes = {}
    allowed_styles = []

    sanitized = bleach.clean(value, tags=allowed_tags, attributes=allowed_attributes, strip=False)

    if sanitized != value:
        raise HTTPException(status_code=400, detail="Недопустимые HTML-теги или скрипты обнаружены")

    return sanitized.strip()
