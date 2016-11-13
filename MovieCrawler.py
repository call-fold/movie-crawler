#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Common.CrawlerToHTML


def compile_url(url):
    return 'http://www.dytt8.net' + url


def get_movie_list(url, decode_type='utf-8'):
    movie_link_list = Common.CrawlerToHTML.get_links_from_html(url, '/html/gndy/dyzz/2016', decode_type)
    movie_link_list = list(map(compile_url, movie_link_list))
    return movie_link_list


def get_movie_download_tuple(url, decode_type='utf-8'):
    movie_title = Common.CrawlerToHTML.get_title_from_html(url, decode_type)
    download_link = Common.CrawlerToHTML.get_links_from_html(url, 'ftp', decode_type)
    return movie_title, download_link[0]


def get_movie_download_list(url, decode_type='utf-8'):
    movie_download_list = []
    movie_url_list = get_movie_list(url, decode_type)
    for movie_url in movie_url_list:
        movie_download = get_movie_download_tuple(movie_url, decode_type)
        print(movie_download)
        movie_download_list.append(movie_download)
    return movie_download_list


if __name__ == '__main__':
    my_url = 'http://www.dytt8.net/'
    # movie_url = 'http://www.ygdy8.net/html/gndy/dyzz/'
    get_movie_download_list(my_url, 'gbk')
