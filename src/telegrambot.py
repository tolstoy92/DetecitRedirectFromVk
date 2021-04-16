from src import posts_utils
from telebot import TeleBot




class PostsRedirector:
    def __init__(self, token):
        self.__bot = TeleBot(token)

    def send_msg(self, chat_id, msg):
        self.__bot.send_message(chat_id=chat_id, text=msg)
