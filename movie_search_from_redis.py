#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

import os
import redis
import logging.config

from common.file_common import check_folder
from crawl_the_whole_movie_site import crawl_list_page

check_folder('/var/log', 'movie_crawler')
log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'conf/movie_search_from_redis.conf')
logging.config.fileConfig(log_file_path)
logger = logging.getLogger('slf')

strict_redis = redis.StrictRedis(host='127.0.0.1', port=6379, db=2, charset='GBK', decode_responses=True)


def get_movie_list(pattern):
    pattern = ('*' + pattern + '*').encode('gbk')
    pattern = str(pattern).replace('\\x', '%')
    pattern = re.findall(r'b\'(.+?)\'', pattern)[0]
    list_title = strict_redis.keys(pattern)
    movie_list = []
    for title in list_title:
        movie_set = strict_redis.smembers(title)
        for movie in movie_set:
            movie_list.append(movie)
    return movie_list


def main():
    movie_title = '冰与火之歌'
    movie_list = get_movie_list(movie_title)
    for movie in movie_list:
        logger.info(movie)
        # crawl_list_page('http://www.ygdy8.com/html/tv/rihantv/list_8_24.html', [], 'http://www.ygdy8.com', strict_redis)


if __name__ == '__main__':
    main()
