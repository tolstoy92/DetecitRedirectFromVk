from urllib import request
from bs4 import BeautifulSoup as bs


def get_html(url):
    response = request.urlopen(url)
    html = response.read()
    return html.decode()


def get_wall_posts(html):
    soup = bs(html, features='html.parser')
    posts = soup.find_all('div', {'class': 'wall_item'})
    return posts


def get_post_id(post_html):
    a_tag = post_html.find('a', {'class': 'pi_author'})
    if a_tag:
        id_info = a_tag['data-post-id']
        return id_info


def get_last_post(posts):
    last_post_num = -1
    last_post = None

    for post in posts:
        post_id = get_post_id(post)
        post_num = int(post_id.split('_')[-1])
        if post_num > last_post_num:
            last_post_num = post_num
            last_post = post
    return last_post


def get_post_url(post_id):
    return f'http://m.vk.com/wall{post_id}'


def create_msg(post, post_id):
    post_content = get_post_content(post)
    for i in post_content.select('br'):
        i.replace_with('\n')
    post_text = post_content.text
    post_url = get_post_url(post_id)
    message = f'{post_text}\n\nСсылка на пост:\n\t{post_url}'
    return message


def get_post_content(post):
    content = post.find('div', {'class': 'pi_text'})
    return content
