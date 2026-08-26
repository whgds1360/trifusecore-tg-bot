# 🤖 Тг бот включающий в себя:

- 💬 Режим ответов на вопросы;
- 📸 Генерация изображений;
- 🔄 Пересылка из ВКонтакте в Telegram;
- 📧 Временная почта: Мгновенное создание одноразового почтового ящика.

# Быстрый старт
### Докер образ можно будет скачать по ссылке:

```
https://hub.docker.com/repository/docker/whgds1360/my-big-project-tg-bot/general
```
### До запуска создайте файл "config.env":
```
config.env

# Получем у BotFather
TG_TOKEN=8736...

# Строка для подключения к вашей бд
DB_URL=mysql+pymysql://root@host...

# Берем с официального сайта Groq
AI_API_KEY=gsk_RQbJy...

# Название модели тоже с сайта Groq
AI_MODEL=...
```

### Далее создаем контейнер с образом и передаем в него наш конфиг

```
docker run --env-file <Путь до конфига> whgds1360/my-big-project-tg-bot:latest
```

# Для форков:

### Установка зависимостей
```
pip install -r requirements.txt
```

## Структура проекта

<pre>
📦 trifusecore-tg-bot
│
├── 🚀 main.py                         # Точка входа
├── 📄 config.json                     # Текстовые настройки
│
├── 📂 core/                           
│   ├── database.py                    # Подключение к БД
│   ├── keyboard_creator.py            # Клавиатуры Telegram
│   ├── resources_manager.py           # Работа с секретами
│   ├── states_manager.py              # Состояния
│   ├── text_config_manager.py         # Загрузка конфига с текстами для сообщений
│   └── сore.py                        # Главный класс Core
│
├── 📂 features/                       
│   ├── ai_chat/                       # AI-чат
│   │   ├── ai_manager.py              # Работа с AI API
│   │   └── ai_router.py               # Обработка команд
│   │
│   ├── forwarding/                    # Пересылка из ВК в Telegram
│   │   ├── forward_manager.py         # Логика пересылки
│   │   └── forward_router.py          # Команды управления
│   │
│   ├── temp_mail/                     # Временная почта
│   │   ├── temp_mail_manager.py       # Генерация и проверка почты
│   │   └── temp_mail_router.py        # Команды почты
│   │
│   ├── main_menu/                     # Главное меню
│   │   └── main_menu_router.py
│   │
│   ├── start/                         # Команда /start
│   │   └── start_router.py
│   │
│   └── all_routers/                   # Сбор всех роутеров
│       └── all_routers.py
│
├── 📂 shared/                         # Общие утилиты (вспомогательные)
│   └── help_func_manager.py            
│
└── 📂 tests/                          # Тесты (pytest)
    ├── conftest.py                    # Настройки для pytest
    ├── core/                          # Тесты для core/
    │   ├── test_resources_config.py
    │   └── test_text_config.py
    ├── features/                      # Тесты для features/
    │   ├── test_ai.py
    │   └── test_temp_mail.py
    └── configs_for_tests/             # Тестовые конфиги для тестов
        └── 📄 test_config.env 
        └── 📄 test_config.json
</pre>

## Vertical slice 

<pre>
            ┌───────────────────────────────────────┐
            │                main.py                │
            │     ┌────────────────────────┐        │
            │     │Инициализация конфигов  │        |
            │     │(Resources + TextConfig)│        │
            │     └────────────────────────┘        │
            |                  │                    │
            |                  ▼                    │
            │ ┌───────────────────────────────────┐ │
            │ │Запуск Core.initialization_tg_bot()│ │
            │ └───────────────────────────────────┘ │
            └───────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐      ┌───────────────┐      ┌───────────────┐
│   AI CHAT     │      │  FORWARDING   │      │  TEMP MAIL    │
│  (фича)       │      │  (фича)       │      │  (фича)       │
├───────────────┤      ├───────────────┤      ├───────────────┤
│ ai_manager.py │      │ forward_mgr   │      │ temp_mail_mgr │
│ ai_router.py  │      │ forward_rt    │      │ temp_mail_rt  │
└───────────────┘      └───────────────┘      └───────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │       Core        │
                    │   - database.py   │
                    │   - keyboard_...  │
                    │   - resources_... │
                    └───────────────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │   Shared (utils)  │
                    │   help_func_...   │
                    └───────────────────┘
</pre>