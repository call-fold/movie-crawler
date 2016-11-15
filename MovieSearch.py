#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Common.CrawlerToHTML
import Common.CommonMovieCrawler
import Common.FileCommon
import os
import re


def change_code_type(input_str, encode_type):
    return input_str.encode(encode_type)


def change_search_str(byte_input):
    temp_str = str(byte_input).replace('\\x', '%')
    return re.findall(r'b\'(.+?)\'', temp_str)[0]


def make_search_url(search_url, add_str):
    return search_url + add_str


def get_search_url(default_search_url, search_str):
    search_str_byte = change_code_type(search_str, 'gbk')
    real_search_str = change_search_str(search_str_byte)
    real_search_url = make_search_url(default_search_url, real_search_str)
    return real_search_url


def compile_url(url):
    return 'http://www.ygdy8.com' + url


def get_movie_list(url, decode_type='utf-8'):
    movie_link_list1 = Common.CrawlerToHTML.get_links_from_html(url, '/html/gndy/dyzz/2', decode_type)
    movie_link_list2 = Common.CrawlerToHTML.get_links_from_html(url, '/html/gndy/jddy/2', decode_type)
    movie_link_list = movie_link_list1 + movie_link_list2
    real_movie_link_list = list(map(compile_url, movie_link_list))
    return real_movie_link_list


if __name__ == '__main__':
    input_name = input('movie to search: ')
    search_index_url = get_search_url('http://s.dydytt.net/plus/search.php?kwtype=0&searchtype=title&keyword=',
                                      input_name)
    my_real_movie_link_list = get_movie_list(search_index_url, 'gbk')
    search_movie_download_list = Common.CommonMovieCrawler.get_movie_download_list(my_real_movie_link_list, 'gbk',
                                                                                   False)
    Common.FileCommon.write_result_to_txt(search_movie_download_list, os.path.abspath('.'), input_name + '.txt')
