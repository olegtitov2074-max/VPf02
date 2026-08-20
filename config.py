"""
Конфигурация бота: токены, настройки, параметры API.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Token (получить у @BotFather)
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# ProxyAPI Key (получить в личном кабинете proxyapi.ru)
PROXYAPI_KEY = os.getenv("PROXYAPI_KEY", "")

# Настройки LLM
MODEL = "gpt-3.5-turbo"
TEMPERATURE = 0.7
MAX_TOKENS = 1024

# ProxyAPI URL
PROXYAPI_URL = "https://api.proxyapi.ru/openai/v1/chat/completions"

# Системное сообщение по умолчанию
SYSTEM_MESSAGE = "Ты — полезный Telegram-бот. Отвечай кратко и по делу на русском языке."
