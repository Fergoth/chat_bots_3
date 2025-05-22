import logging
import os
import random
import time

import vk_api as vk
from dotenv import load_dotenv
from google.cloud import dialogflow
from telegram import Bot
from vk_api.longpoll import VkEventType, VkLongPoll

logger = logging.getLogger("telegram_debug")


def detect_intent_text(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    if response.query_result.intent.is_fallback:
        return None
    return response.query_result.fulfillment_text


class TelegramLogsHandler(logging.Handler):
    def __init__(self, chat_id, tg_token):
        super().__init__()
        self.chat_id = chat_id
        self.bot = Bot(token=tg_token)

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)


def reply(event, vk_api):
    try:
        project_id = os.environ["DIALOG_FLOW_PROJECT_ID"]
        session_id = event.user_id
        language_code = "RU"
        reply = detect_intent_text(project_id, session_id, event.text, language_code)
        if reply:
            vk_api.messages.send(
                user_id=event.user_id, message=reply, random_id=random.randint(1, 1000)
            )
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
    logger.info("VK Бот dialogflow запущен")

    vk_token = os.environ["VK_API_KEY"]
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            reply(event, vk_api)


if __name__ == "__main__":
    main()
