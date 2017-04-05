#!/usr/bin/env python
# -*- coding: utf-8 -*-

import common.crawler_to_html
import common.common_movie_crawler
import common.file_common
import os
import json
from pprint import pprint


def compile_url(url):
    return 'http://www.dytt8.net' + url


def get_movie_list(url, decode_type='utf-8'):
    movie_link_list = common.crawler_to_html.get_links_from_html_keywords(url, ['/html/gndy/dyzz/2017',
                                                                                '/html/gndy/jddy/2017'], decode_type)
    movie_link_list = list(map(compile_url, movie_link_list))
    movie_link_set = set(movie_link_list)
    final_movie_link_list = list(movie_link_set)
    return final_movie_link_list


def get_movie_dict_json_str(index_url, decode_type='utf-8'):
    my_index_url = index_url
    my_real_movie_link_list = get_movie_list(my_index_url, decode_type)
    search_movie_download_list = common.common_movie_crawler.get_movie_download_list(my_real_movie_link_list,
                                                                                     decode_type,
                                                                                     True)
    movie_dict = common.common_movie_crawler.get_movie_download_dict(search_movie_download_list)
    movie_json_str = json.dumps(movie_dict)
    return movie_json_str


def main():
    my_index_url = 'http://www.dytt8.net/'
    movie_json_str = get_movie_dict_json_str(my_index_url, 'gbk')
    pprint(json.loads(movie_json_str))
    # my_index_url = 'http://www.dytt8.net/'
    # my_real_movie_link_list = get_movie_list(my_index_url, 'gbk')
    # if_add_title = True
    # if if_add_title:
    #     search_movie_download_list = common.common_movie_crawler.get_movie_download_list(my_real_movie_link_list, 'gbk',
    #                                                                                      True)
    #     movie_dict = common.common_movie_crawler.get_movie_download_dict(search_movie_download_list)
    #     movie_json = json.dumps(movie_dict)
    #     common.file_common.write_tuple_result_to_txt(search_movie_download_list, os.path.abspath('.') + '/top_movies',
    #                                                  'movies2017(title).txt')
    # else:
    #     search_movie_download_list = common.common_movie_crawler.get_movie_download_list(my_real_movie_link_list, 'gbk',
    #                                                                                      False)
    #     common.file_common.write_result_to_txt(search_movie_download_list, os.path.abspath('.') + '/top_movies',
    #                                            'movies2017.txt')


    # tv_url = 'http://www.ygdy8.com/html/tv/oumeitv/20151007/49245.html'
    # tv_list = get_tv_drama_program_list(tv_url, 'gbk')
    # write_result_to_txt(tv_list, os.path.abspath('.'), 'tv_drama_program_list.txt')


if __name__ == '__main__':
    main()
