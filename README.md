# Telegram Gif Bot

### 🔹 Описание
2 часть пет-проекта — полностью асинхронный Telegram bot на aiogram, взаимодействующий с [API](https://github.com/EgorBP/API) 
> Вы можете протестировать уже развернутое [API](https://api-production-8e0b.up.railway.app/docs) и [Бота](https://t.me/GifRepositoryBot).

### ✨ Основные возможности
- Быстрый запуск через [Docker](#-запуск-через-docker) или локально с [Python](#-запуск-через-python)  
- Тестирование с помощью pytest  
- Взаимодействие с [API](https://github.com/EgorBP/API)
> ⚠️ Перед запуском убедитесь, что API работает, иначе бот не сможет обрабатывать запросы.
  
### 📦 Структура проекта

- **`bot/`** — основной код бота
- **`tests/`** — модульные тесты
- **`.env.example`** — пример конфигурационного файла для локального запуска
- **`.env.docker.example`** — пример конфигурационного файла для Docker
- **`Dockerfile`** — инструкции для создания Docker-образа
- **`docker-compose.yml`** — конфигурация контейнеров для развёртывания
- **`requirements.txt`** — зависимости проекта

## ⚙️ Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/EgorBP/TgGifBot.git
cd TgGifBot
```
2. Настройте переменные среды:
```bash
cp .env.docker.example .env.docker
cp .env.example .env
```
3. Измените *`BOT_TOKEN`* в `.env` и `.env.docker` на ваш реальный токен бота.
> Токен можно получить у [BotFather](https://telegram.me/BotFather).

### 🐳 Запуск через Docker
1. Соберите и запустите контейнеры:
```bash
docker compose up --build
```
2. Бот будет доступен в Telegram по имени, которое вы указали при его создании у [BotFather](https://telegram.me/BotFather).

### 🐍 Запуск через Python
1. Создайте виртуальное окружение и активируйте его:
```python
python -m venv .venv
```
##### Для Windows
```bash
.venv\Scripts\activate
```
##### Для Linux/macOS
```bash
source .venv/bin/activate
```
2. Установите зависимости:
```bash
pip install -r requirements.txt
```
3. Запустите бота:
```bash
python app/main.py
```
4. Бот будет доступен в Telegram по имени, которое вы указали при его создании у [BotFather](https://telegram.me/BotFather).

