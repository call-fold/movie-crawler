#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import schedule
import time
import redis
import ctypes
from common.file_common import check_folder
from crawl_the_whole_movie_site import crawl_index_page

check_folder('/var/log', 'movie_crawler')
logging.config.fileConfig('movie_crawler_logging.conf')
logger = logging.getLogger('slf')


def get_proc_id():
    return str(ctypes.CDLL('libc.so.6').syscall(186))


def crawler_job():
    strict_redis = redis.StrictRedis(host='127.0.0.1', port=6379, db=1, charset='GBK', decode_responses=True)
    host = "http://www.ygdy8.com"
    start_url = "http://www.ygdy8.com/index.html"
    logger.info('proc_id-' + get_proc_id() + ' begin to crawl from: ' + start_url)
    crawl_index_page(start_url, host, strict_redis)


schedule.every(1).days.do(crawler_job)

while True:
    schedule.run_pending()
    time.sleep(1)
