import os
from urllib import request
from bs4 import BeautifulSoup as bs

from time import sleep
import secrets
from telebot import TeleBot
from threading import Thread

from src import posts_utils


TIMEOUT = 0.01
PUBLIC_URL = 'https://m.vk.com/detectit_spb'
LAST_SENDED_POST_NUM = -1

BOT_TOKEN = os.environ['redirect_bot_token']
CHAT_ID = os.environ['detectit_chat_id']
SLEEP_TIME = 5

posts_redirector = TeleBot(BOT_TOKEN)


def main():
    last_sended_post_num = -1
    while True:
        html = posts_utils.get_html(PUBLIC_URL)
        posts = posts_utils.get_wall_posts(html)
        posts_ids = [posts_utils.get_post_id(post) for post in posts]
        posts_nums = [int(split('_')[-1]) for post_id in posts_ids]
        zipped = zip(posts_nums, posts, posts_ids)
        sorted_posts_and_ids = []
        for post_num, post, post_id in sorted(zipped):
            if post_num > last_sended_post_num:
                sorted_posts_and_ids.append((post, post_id, post_num))
            
        if sorted_posts_and_ids:
            for post, post_id, post_num in sorted_posts_and_ids:
                message = posts_utils.create_msg(post, post_id)
                posts_redirector.send_message(CHAT_ID, message)
                last_sended_post_num = post_num
        sleep(SLEEP_TIME)


@posts_redirector.message_handler(func=lambda x: x.text not in ['start', '/start'])
def echo(message):
    posts_redirector.reply_to(message, "I'm still alive!")


@posts_redirector.message_handler(commands=['start'])
def main_loop(message):
    posts_redirector.reply_to(message, 'Started!')
    main()

            
if __name__ == '__main__':
    posts_redirector.polling(interval=3)
