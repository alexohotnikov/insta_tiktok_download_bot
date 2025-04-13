# Instagram & TikTok Downloader Bot

Telegram бот для скачивания видео из Instagram Reels и TikTok.

## Возможности

- Скачивание видео из Instagram Reels
- Скачивание видео из TikTok
- Автоматическое удаление скачанных файлов после отправки

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/insta_tiktok_download_bot.git
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
INSTAGRAM_SESSION_USERNAME=your_instagram_username
INSTAGRAM_SESSION_FILE=path_to_session_file
INSTAGRAM_COOKIES_FILE=path_to_cookies_file
```

## Использование

1. Запустите бота:
```bash
python src/main.py
```

2. Отправьте боту ссылку на видео из Instagram Reels или TikTok
3. Бот скачает видео и отправит его вам

## Зависимости

- aiogram>=3.0.0
- python-dotenv>=0.19.0
- requests>=2.26.0
- gallery-dl>=1.25.0
- tiktok-downloader>=0.2.0

## Лицензия

MIT 