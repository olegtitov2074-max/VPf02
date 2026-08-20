"""
Telegram-бот с интеграцией ProxyAPI (LLM).
Основные команды:
  /start — начать диалог
  /clear — очистить контекст
  /help — показать справку
"""

import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message

import config
import proxyapi_client
import context_manager

# --- Логирование ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

# --- Инициализация бота ---
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()


# --- Команды ---
@dp.message(Command("start"))
async def cmd_start(message: Message) -> None:
    """Команда /start — приветствие."""
    context_manager.clear_context(message.from_user.id)
    await message.answer(
        "Привет! Я бот на базе LLM. Задайте мне вопрос, и я постараюсь ответить.\n\n"
        "Команды:\n"
        "/clear — очистить историю диалога\n"
        "/help — показать справку"
    )
    logger.info("Пользователь %s (%s) выполнил /start", message.from_user.full_name, message.from_user.id)


@dp.message(Command("clear"))
async def cmd_clear(message: Message) -> None:
    """Команда /clear — очистить контекст пользователя."""
    cleared = context_manager.clear_context(message.from_user.id)
    if cleared:
        await message.answer("✅ Контекст очищен.")
    else:
        await message.answer("❌ Контекст уже пуст.")
    logger.info("Пользователь %s очистил контекст", message.from_user.id)


@dp.message(Command("help"))
async def cmd_help(message: Message) -> None:
    """Команда /help — показать справку."""
    await message.answer(
        "📖 Справка:\n\n"
        "Этот бот использует LLM (через ProxyAPI) для ответов на ваши вопросы.\n\n"
        "Как пользоваться:\n"
        "• Просто напишите сообщение — бот ответит как чат-бот.\n"
        "• Контекст диалога сохраняется — бот помнит историю.\n\n"
        "Команды:\n"
        "/start — начать новый диалог\n"
        "/clear — очистить историю диалога\n"
        "/help — показать эту справку"
    )


# --- Обработка обычных сообщений ---
@dp.message()
async def handle_message(message: Message) -> None:
    """Обработка обычного текстового сообщения."""
    user_id = message.from_user.id
    text = message.text.strip()

    if not text:
        return

    logger.info("Пользователь %s (%s): %s", message.from_user.full_name, user_id, text[:50])

    # Добавляем сообщение пользователя в контекст
    context_manager.add_message(user_id, "user", text)

    try:
        # Получаем контекст и отправляем запрос к ProxyAPI
        context = context_manager.get_context(user_id)
        reply = proxyapi_client.chat(context)

        # Добавляем ответ бота в контекст
        context_manager.add_message(user_id, "assistant", reply)

        await message.answer(reply)

    except requests.exceptions.HTTPError as e:
        logger.error("HTTP ошибка ProxyAPI: %s", e)
        await message.answer(
            "❌ Ошибка сервера. Попробуйте позже.\n"
            "Код ошибки: " + str(e.response.status_code if e.response else "N/A")
        )
    except requests.exceptions.Timeout:
        logger.error("Таймаут ProxyAPI")
        await message.answer("❌ Сервер не отвечает. Попробуйте позже.")
    except requests.exceptions.ConnectionError:
        logger.error("Ошибка подключения к ProxyAPI")
        await message.answer("❌ Нет подключения к API. Проверьте соединение.")
    except ValueError as e:
        logger.error("Ошибка обработки ответа API: %s", e)
        await message.answer("❌ Неверный ответ от сервера. Попробуйте позже.")
    except Exception as e:
        logger.error("Неожиданная ошибка: %s", e, exc_info=True)
        await message.answer("❌ Произошла ошибка. Попробуйте позже.")


# --- Запуск бота ---
async def main() -> None:
    """Проверка конфигурации и запуск бота."""
    if not config.BOT_TOKEN:
        logger.error("BOT_TOKEN не указан! Добавьте его в .env")
        return

    if not config.PROXYAPI_KEY:
        logger.error("PROXYAPI_KEY не указан! Добавьте его в .env")
        return

    logger.info("Бот запущен ✅")
    await dp.start_polling(bot)


if __name__ == "__main__":
    import requests  # noqa: E402 — для handle_message

    try:
        import asyncio
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
