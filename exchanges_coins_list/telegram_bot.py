import os
import telegram
from logger import logger
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ.get("TOKEN1")
MY_ID = os.environ.get("TOKEN2")


class TelegramBot:
    def __init__(self):
        self.token = TOKEN
        self.chat_ids = [MY_ID]
        self.bot = telegram.Bot(token=self.token)
        self.logger = logger
        self.send_messages = False  # Add a switch to turn on/off message sending

    async def send_message(self, message):
        if self.send_messages:  # Check if message sending is enabled
            try:
                for chat_id in self.chat_ids:
                    await self.bot.send_message(chat_id=chat_id, text=message)
                    self.logger.logger.info(f"Message sent to {chat_id}")
            except telegram.error.TelegramError as e:
                self.logger.logger.error(f"Error sending message: {e}")