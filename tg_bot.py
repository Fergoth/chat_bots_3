import logging
import os
import time

from dotenv import load_dotenv
from google.cloud import dialogflow
from telegram import Bot, Update
from telegram.ext import (
    CallbackContext,
    Filters,
    MessageHandler,
    Updater,
)

logger = logging.getLogger("telegram_debug")


def detect_intent_text(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    return response.query_result.fulfillment_text


class TelegramLogsHandler(logging.Handler):
    def __init__(self, chat_id, tg_token):
        super().__init__()
        self.chat_id = chat_id
        self.bot = Bot(token=tg_token)

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)


def reply(update: Update, context: CallbackContext):
    try:
        project_id = os.environ["DIALOG_FLOW_PROJECT_ID"]
        session_id = update.message.chat_id
        language_code = "RU"
        reply = detect_intent_text(
            project_id, session_id, update.message.text, language_code
        )
        update.message.reply_text(reply)
    except Exception as e:
        logger.error(f"Неизвестная ошибка:{e}")
        time.sleep(5)


def main():
    load_dotenv()
    tg_debug_token = os.environ.get("TELEGRAM_DEBUG_BOT_TOKEN")
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    if tg_debug_token:
        logger.addHandler(TelegramLogsHandler(chat_id, tg_debug_token))
    logger.setLevel(logging.INFO)
    logger.info("Телеграм Бот dialogflow запущен")
    tg_token = os.environ["TELEGRAM_BOT_TOKEN"]
    updater = Updater(token=tg_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, reply))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
