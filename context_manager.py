"""
Управление контекстом диалога.
Контекст хранится в памяти (dict). Ключ — user_id, значение — список сообщений.
"""

# { user_id: [ {"role": "system"/"user"/"assistant", "content": "..."}, ... ] }
_contexts: dict[int, list[dict]] = {}


def get_context(user_id: int) -> list[dict]:
    """Получить контекст пользователя. Если контекста нет — создать пустой."""
    if user_id not in _contexts:
        _contexts[user_id] = []
    return _contexts[user_id]


def add_message(user_id: int, role: str, content: str) -> None:
    """Добавить сообщение в контекст пользователя."""
    if user_id not in _contexts:
        _contexts[user_id] = []
    _contexts[user_id].append({"role": role, "content": content})


def clear_context(user_id: int) -> bool:
    """Очистить контекст пользователя. Возвращает True если контекст был."""
    if user_id in _contexts:
        del _contexts[user_id]
        return True
    return False


def has_context(user_id: int) -> bool:
    """Проверить, есть ли контекст у пользователя."""
    return user_id in _contexts
