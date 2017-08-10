#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import threading
import os
import sys
import logging.config
import ctypes
import errno
import redis

from urllib import request
from time import sleep
from common.file_common import check_folder
from common.timeout import timeout
from lxml import etree

check_folder('/var/log', 'movie_crawler')
log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'conf/movie_crawler_logging.conf')
logging.config.fileConfig(log_file_path)
logger = logging.getLogger('slf')


def get_proc_id():
    return str(ctypes.CDLL('libc.so.6').syscall(186))


# 继承父类threading.Thread
class CrawlThread(threading.Thread):
    def __init__(self, url, crawled_urls, host, strict_redis, catalog):
        threading.Thread.__init__(self)
        self.url = url
        self.crawled_urls = crawled_urls
        self.host = host
        self.strict_redis = strict_redis
        self.catalog = catalog

    # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
    def run(self):
        logger.info('proc_id-' + get_proc_id() + " - " + self.catalog + " begin...")
        crawl_list_page(self.url, self.crawled_urls, self.host, self.strict_redis)


# 判断地址是否已经爬取
def is_exit(new_url, crawled_urls):
    for url in crawled_urls:
        if url == new_url:
            return True
    return False


# 获取页面资源
def get_page(url):
    try:
        f = request.urlopen(url)
        page = f.read()
    except Exception as e:
        logger.error('exception url: ' + url)
        logger.error('exception proc id: ' + get_proc_id())
        logger.exception(e)
    else:
        return page


# 处理资源名
def change_code_type(input_str, encode_type):
    real_input_str = input_str.encode(encode_type, 'ignore')
    return real_input_str


def change_search_str(byte_input):
    temp_str = str(byte_input).replace('\\x', '%')
    return re.findall(r'b\'(.+?)\'', temp_str)[0]


def make_search_url(search_url, add_str):
    return search_url + add_str


def change_movie_title(default_movie_title):
    search_str_byte = change_code_type(default_movie_title, 'gbk')
    real_movie_title = change_search_str(search_str_byte)
    # 处理电影名中间的空格
    movie_title = real_movie_title.replace(' ', '%20')
    return movie_title


# 处理资源页面 爬取资源地址
def crawl_source_page(url, movie_title, crawled_urls, strict_redis):
    page = get_page(url)
    if page == "error":
        return
    crawled_urls.append(url)
    page = page.decode('gbk', 'ignore')
    tree = etree.HTML(page)
    nodes = tree.xpath("//div[@align='left']//table//a")
    try:
        for node in nodes:
            source_url = node.xpath("@href")[0]
            # check 'ftp' in url
            if 'ftp' in source_url:
                logger.debug('proc_id-' + get_proc_id() + " " + source_url)
                # push to redis
                strict_redis.sadd(change_movie_title(movie_title), source_url)
    except Exception as e:
        logger.error('exception url: ' + url)
        logger.error('exception proc id: ' + get_proc_id())
        logger.exception(e)


def fix_movie_title(movie_title):
    return movie_title.replace("/", " ") \
        .replace("\\", " ") \
        .replace(":", " ") \
        .replace("*", " ") \
        .replace("?", " ") \
        .replace("\"", " ") \
        .replace("<", " ") \
        .replace(">", " ") \
        .replace("|", " ")


# 解析分类文件
def crawl_list_page(index_url, crawled_urls, host, strict_redis):
    page = get_page(index_url)
    if page == "error":
        return
    crawled_urls.append(index_url)
    page = page.decode('gbk', 'ignore')
    tree = etree.HTML(page)
    nodes = tree.xpath("//div[@class='co_content8']//a")
    for node in nodes:
        url = node.xpath("@href")[0]
        if re.match(r'/', url):
            # 非分页地址 可以从中解析出视频资源地址
            if is_exit(host + url, crawled_urls):
                pass
            else:
                try:
                    # 文件命名是不能出现以下特殊符号
                    if len(node.xpath('text()')) == 0:
                        movie_title = node.xpath('b/text()')[0]
                    else:
                        movie_title = node.xpath('text()')[0]
                    fix_movie_title(movie_title)
                    crawl_source_page(host + url, movie_title, crawled_urls, strict_redis)
                except Exception as e:
                    logger.error('exception index: ' + index_url)
                    logger.error('exception url: ' + host + url)
                    logger.error('exception proc id: ' + get_proc_id())
                    logger.exception(e)
            pass
        else:
            # 分页地址 从中嵌套再次解析
            index = index_url.rfind("/")
            base_url = index_url[0:index + 1]
            page_url = base_url + url
            if is_exit(page_url, crawled_urls):
                pass
            else:
                crawl_list_page(page_url, crawled_urls, host, strict_redis)
            pass
    pass


# 解析首页
def crawl_index_page(start_url, host, strict_redis):
    logger.info('proc_id-' + get_proc_id() + " begin to crawl from index page...")
    page = get_page(start_url)
    if page == "error":
        return
    page = page.decode('gbk', 'ignore')
    tree = etree.HTML(page)
    nodes = tree.xpath("//div[@id='menu']//a")
    logger.info('proc_id-' + get_proc_id() + " num of different type: " + str(len(nodes)))
    for node in nodes:
        crawled_urls = [start_url]
        url = node.xpath("@href")[0]
        if re.match(r'/html/[A-Za-z0-9_/]+/index.html', url):
            if is_exit(host + url, crawled_urls):
                pass
            else:
                try:
                    catalog = node.xpath("text()")[0]
                    thread = CrawlThread(host + url, crawled_urls, host, strict_redis, catalog)
                    thread.start()
                except Exception as e:
                    logger.error('exception url: ' + host + url)
                    logger.error('exception proc id: ' + get_proc_id())
                    logger.exception(e)


def main():
    strict_redis = redis.StrictRedis(host='127.0.0.1', port=6379, db=2, charset='GBK', decode_responses=True)
    host = "http://www.ygdy8.com"
    start_url = "http://www.ygdy8.com/index.html"
    logger.info('proc_id-' + get_proc_id() + ' begin to crawl from: ' + start_url)
    crawl_index_page(start_url, host, strict_redis)
    # 后面写入配置文件
    sleep(60 * 60)
    os._exit(0)


if __name__ == '__main__':
    main()
