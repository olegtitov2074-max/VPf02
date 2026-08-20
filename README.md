# Telegram-бот с ProxyAPI (LLM)

Telegram-бот на Python (aiogram) с интеграцией LLM через ProxyAPI.

## 📁 Структура проекта

| Файл | Описание |
|---|---|
| `bot.py` | Основной файл — обработчики сообщений и команд |
| `config.py` | Токены и настройки (читает из `.env`) |
| `proxyapi_client.py` | Функция отправки запроса к ProxyAPI |
| `context_manager.py` | Хранение контекста диалога в памяти |
| `.env` | Переменные окружения (токены) |
| `requirements.txt` | Зависимости |

## 🚀 Установка

```powershell
pip install -r requirements.txt
```

## ⚙️ Настройка

1. Получите токен бота у **@BotFather** в Telegram
2. Получите ключ API в [proxyapi.ru](https://proxyapi.ru/)
3. Заполните `.env`:

```env
BOT_TOKEN=ваш_тг_токен
PROXYAPI_KEY=ваш_proxyapi_ключ
```

## ▶️ Запуск

```powershell
python bot.py
```

## 📋 Команды

| Команда | Описание |
|---|---|
| `/start` | Начать новый диалог |
| `/clear` | Очистить историю диалога |
| `/help` | Показать справку |

## 🧪 Тестирование параметров LLM

### Результаты прогонов

Данные из логов ProxyAPI (скриншот на скриншоте ниже):

| № | Модель | Temperature | Max Tokens | Эффект (сжатость/креатив) | Использовано токенов | Ориент. стоимость |
|---|---|---|---|---|---|---|
| 1 | gpt-3.5-turbo | — | — | Развёрнутый ответ | prompt: 27 → completion: 126 | 0.0522 ₽ |
| 2 | gpt-3.5-turbo | — | — | Развёрнутый ответ | prompt: 29 → completion: 132 | 0.0548 ₽ |
| 3 | gpt-3.5-turbo | — | — | Максимально сжатый ответ | prompt: 30 → completion: 22 | 0.0124 ₽ |
| 4 | gpt-3.5-turbo | — | — | Средний ответ | prompt: 28 → completion: 86 | 0.0369 ₽ |
| 5 | gpt-3.5-turbo | — | — | Максимально развёрнутый ответ | prompt: 28 → completion: 256 | 0.1027 ₽ |

> **Примечание:** На скриншоте логов ProxyAPI не отображаются temperature и max_tokens — они не попадают в логи провайдера. Задержки ответа: от 1.47 с до 3.73 с.

![Логи ProxyAPI](screenshots/logs.png)

### Как запустить тесты

```powershell
# Прогон 1 — минимальная температура
python proxyapi_request.py "Твой запрос" 0.0 256

# Прогон 2 — низкая температура
python proxyapi_request.py "Твой запрос" 0.3 256

# Прогон 3 — средняя температура
python proxyapi_request.py "Твой запрос" 0.7 1024

# Прогон 4 — высокая температура
python proxyapi_request.py "Твой запрос" 1.0 1024

# Прогон 5 — максимальная температура
python proxyapi_request.py "Твой запрос" 1.5 2048
```

## 📝 Лицензия

MIT
