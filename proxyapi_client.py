"""
Отправка запроса к LLM через ProxyAPI.
"""

import logging
import requests

from config import PROXYAPI_KEY, PROXYAPI_URL, MODEL, TEMPERATURE, MAX_TOKENS

logger = logging.getLogger(__name__)


def chat(messages: list[dict], system_message: str | None = None) -> str:
    """
    Отправить запрос к ProxyAPI и получить ответ.

    Args:
        messages: список сообщений диалога.
        system_message: системное сообщение. Если None — берётся из config.

    Returns:
        Текст ответа от модели.

    Raises:
        requests.exceptions.RequestException: при ошибке сети или HTTP.
        ValueError: при некорректном ответе от API.
    """
    import config

    system_msg = system_message or config.SYSTEM_MESSAGE

    # Добавляем системное сообщение в начало, если его ещё нет
    full_messages = messages.copy()
    if not any(m["role"] == "system" for m in full_messages):
        full_messages.insert(0, {"role": "system", "content": system_msg})

    payload = {
        "model": MODEL,
        "messages": full_messages,
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
    }

    headers = {
        "Authorization": f"Bearer {PROXYAPI_KEY}",
        "Content-Type": "application/json",
    }

    logger.info("Отправка запроса к ProxyAPI, сообщений в контексте: %d", len(messages))

    try:
        response = requests.post(
            PROXYAPI_URL,
            headers=headers,
            json=payload,
            timeout=120,
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logger.error("HTTP ошибка ProxyAPI: %s — %s", e, response.text)
        raise
    except requests.exceptions.Timeout:
        logger.error("Таймаут запроса к ProxyAPI (120 сек)")
        raise
    except requests.exceptions.ConnectionError:
        logger.error("Ошибка подключения к ProxyAPI")
        raise

    try:
        data = response.json()
        content = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, ValueError) as e:
        logger.error("Некорректный ответ от ProxyAPI: %s", e)
        logger.debug("Ответ API: %s", response.text)
        raise ValueError(f"Некорректный ответ от API: {response.text}") from e

    logger.info("Получен ответ от модели, длина: %d символов", len(content))
    return content
