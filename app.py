import logging

logfile = '/home/pi/error.log'
logging.basicConfig(filename=logfile, level=logging.DEBUG)

import os
from urllib import request
from bs4 import BeautifulSoup as bs

from time import sleep
import secrets
from telebot import TeleBot
from threading import Thread

from src import posts_utils


try:
    TIMEOUT = 0.01
    PUBLIC_URL = 'https://m.vk.com/detectit_spb'

    BOT_TOKEN = os.environ['redirect_bot_token']
    CHAT_ID = os.environ['detectit_chat_id']
    OWNER_ID = os.environ['telegram_owner_id']
    SLEEP_TIME = 5

    posts_redirector = TeleBot(BOT_TOKEN)

    started = False
    last_sended_post_num = -1
    last_sended_post_url = -1


    def main():
        global started, last_sended_post_num, last_sended_post_url
        started = True
        while True:
            html = posts_utils.get_html(PUBLIC_URL)
            posts = posts_utils.get_wall_posts(html)
            posts_ids = [posts_utils.get_post_id(post) for post in posts]
            posts_nums = [int(post_id.split('_')[-1]) for post_id in posts_ids]
            zipped = zip(posts_nums, posts, posts_ids)
            sorted_posts_and_ids = []
            for post_num, post, post_id in sorted(zipped):
                if post_num > last_sended_post_num:
                    sorted_posts_and_ids.append((post, post_id, post_num))
                
            if sorted_posts_and_ids:
                for post, post_id, post_num in sorted_posts_and_ids:
                    message = posts_utils.create_msg(post, post_id)
                    posts_redirector.send_message(CHAT_ID, message)
                    post_url = posts_utils.get_post_url(post_id)
                    last_sended_post_url = post_url
                    last_sended_post_num = post_num
            sleep(SLEEP_TIME)


    @posts_redirector.message_handler(commands=['start'])
    def main_loop(message):
        global started
        if started:
            posts_redirector.reply_to(message, 'Already started!')
        else:
            posts_redirector.reply_to(message, 'Just started!')
            main()


    @posts_redirector.message_handler(commands=['status'])
    def send_status(message):
        global started, last_sended_post_url
        status_str = \
            f'started: {started}\nlast_post_url: {last_sended_post_url}'
        posts_redirector.reply_to(message, status_str)

                
    if __name__ == '__main__':
        posts_redirector.send_message(OWNER_ID, 'Waked up! =)')
        posts_redirector.polling(interval=3)
except Exception as e:
    logging.debug(e)