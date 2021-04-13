import os
from time import sleep

from src import posts_utils
from src.telegrambot import PostsRedirector


TIMEOUT = 0.01
PUBLIC_URL = 'https://m.vk.com/detectit_spb'
LAST_SENDED_POST_NUM = -1

BOT_TOKEN = os.environ['detectit_bot_token']
CHAT_ID = os.environ['detectit_chat_id']
SLEEP_TIME = 3


posts_redirector = PostsRedirector(BOT_TOKEN)


def main():
    last_sended_post_num = -1
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
                posts_redirector.send_msg(CHAT_ID, message)
                last_sended_post_num = post_num
                
        sleep(SLEEP_TIME)
            

if __name__ == '__main__':
    main()
