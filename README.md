# Instagram & TikTok Downloader Bot

Telegram бот для скачивания видео из Instagram и TikTok.

## Возможности

- Скачивание видео из Instagram Reels
- Скачивание постов из Instagram (фото и видео)
- Скачивание видео из TikTok
- Потоковое воспроизведение видео
- Автоматическое удаление скачанных файлов после отправки
- Система безопасности с проверкой доступа
- Поддержка мультимедийных постов

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/alexohotnikov/insta_tiktok_download_bot.git
cd insta_tiktok_download_bot
```

2. Создайте виртуальное окружение и активируйте его:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
# или
venv\Scripts\activate  # для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл `.env` и добавьте необходимые переменные окружения:
```env
BOT_TOKEN=your_bot_token
BOT_LINK=your_bot_link
INSTAGRAM_SESSION_USERNAME=your_instagram_username
INSTAGRAM_SESSION_FILE=path_to_session_file
INSTAGRAM_COOKIES_FILE=path_to_cookies_file
NEED_PASSWORD_CHECK=true/false
BOT_VERSION=0.3.0
```

## Использование

1. Запустите бота:
```bash
python src/main.py
```

2. Отправьте боту ссылку на:
   - Instagram Reels
   - Instagram пост (фото/видео)
   - TikTok видео
3. Бот скачает контент и отправит его вам

## Зависимости

- aiogram>=3.0.0
- python-dotenv>=0.19.0
- requests>=2.26.0
- gallery-dl>=1.25.0
- tiktok-downloader>=0.2.0
- instaloader>=4.9.0
- yt-dlp

## Системные требования

- Python 3.8 или выше
- Доступ к интернету
- Достаточно места на диске для временных файлов

## Безопасность

- Встроенная система проверки доступа
- Автоматическая очистка временных файлов
- Безопасное хранение учетных данных через переменные окружения

## Версия

Текущая версия: 0.3.0

## Лицензия

MIT 