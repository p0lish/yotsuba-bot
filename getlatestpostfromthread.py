#!/usr/bin/python
import random
import socket

import requests
from bs4 import BeautifulSoup
from requests import HTTPError

POSSIBLE_ERRORS = (HTTPError,
                   socket.error,
                   requests.exceptions.InvalidSchema,
                   requests.exceptions.ConnectionError)

ROOT_URL = "http://boards.4chan.org"

USERAGENTS = [
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201"
]


def random_user_agent():
    return random.choice(USERAGENTS)

USER_AGENT = random_user_agent()


def get_content(url):
    try:
        req = requests.get(url, headers={'User-Agent': USER_AGENT}, verify=False, timeout=20)
        if req.status_code == 200:
            return req.content
    except POSSIBLE_ERRORS as error:
        print(url)
        print("This url causes the following error:", error)
        return ""
    except requests.exceptions.Timeout:
        return "timeout"


def get_all_posts_from_thread(thread, num_of_pages):
    i = 1
    allPosts = []
    while i <= num_of_pages:
        str_i = str(i) if i > 1 else ""
        current_url = "/".join((ROOT_URL, thread, str_i))
        root_url = "/".join((ROOT_URL, thread, ""))
        content = get_content(current_url)
        soup_content = BeautifulSoup(content, 'html.parser')
        info = soup_content.findAll('div', {"class": "thread"})
        info = list(set(info))
        for inf in info:
            soup_data = BeautifulSoup(str(inf), 'html.parser')
            # print(soup_data)
            timestamp = soup_data.find('span', {"class": "dateTime"})['data-utc']
            thumbnail = soup_data.find('a', {"class": "fileThumb"}).find('img')['src']
            image = soup_data.find('a', {"class": "fileThumb"})['href']
            link = soup_data.find('a', {"class": "replylink"})['href']
            quote = soup_data.find('blockquote', {"class": "postMessage"}).getText()
            allPosts.append({
                "timestamp": timestamp,
                "thumbnail": 'http:' + thumbnail,
                "image": 'http:' + image,
                "link": root_url + '/' + link,
                "description": quote
             })
        i += 1
    sorted_posts = sorted(allPosts, key=lambda k: k['timestamp'], reverse=True)
    return sorted_posts