# Чат бот для VK и Telegram с обучением через Dialogflow



## Окружение
### Требования
Для запуска требуется python версии 3.13. Или установленная утилита [uv](https://docs.astral.sh/uv/) 



### Установка зависимостей (если нет uv) 
```sh
pip install -r requirements.txt
```
### Переменные окружения


1. Создайте файл `.env` в папке проекта
2. Заполните файл `.env` следующим образом без кавычек:
```bash
TELEGRAM_BOT_TOKEN=token
TELEGRAM_CHAT_ID=id
TELEGRAM_DEBUG_BOT_TOKEN=token
GOOGLE_APPLICATION_CREDENTIALS=path
DIALOG_FLOW_PROJECT_ID=project_id
VK_API_KEY=vk_token
```
#### Как получить токены

*  Токен для телеграм бота TELEGRAM_BOT_TOKEN(бот который отправляет сообщения о проверке работ) и TELEGRAM_DEBUG_BOT_TOKEN(Бот для отладки, **Необязательный**, если не указан, логи идут в консоль) можно получить при создании бота [ссылке](https://telegram.me/BotFather)
* TELEGRAM_CHAT_ID - ваш айди в телеграме, можно получить у [бота](https://telegram.me/userinfobot) 
* GOOGLE_APPLICATION_CREDENTIALS - путь к credintals.json который позволяет общаться с DialogFlow. Нужен для развертывании на сервере,
при настройке как указано по [ссылке](https://cloud.google.com/dialogflow/es/docs/quick/setup#sdk) нужная переменная окружения создастся сама
* DIALOG_FLOW_PROJECT_ID [Создать проект](https://cloud.google.com/dialogflow/es/docs/quick/setup)\
* VK_API_KEY Api key группы в VK, требуется для запуска vk_bot


### Запустите скрипт 
```sh
python tg_bot.py 
```
для запуска бота в телеграме,
```sh
python vk_bot.py 
```
для запуска бота в vk,

```sh
python create_intents.py 
```
для Добавления интентов к проекту dialogFlow, интенты загружаются из question.json 

### При наличии uv
- Просто запустите скрипт с помощью uv 
```sh
uv run tg_bot.py 
```

### Примечание

  Напишите телеграм боту чтобы он мог отправлять вам сообщения
  
### Пример использования
[!test](https://github.com/user-attachments/assets/5ac4d113-ff0f-4c88-9a52-225ae07be685)

[vk](https://vk.com/club230569125)

[tg](https://t.me/game_of_verbs_dvmn2_bot)

