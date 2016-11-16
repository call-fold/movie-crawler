#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Common.CrawlerToHTML
import Common.CommonMovieCrawler
import Common.FileCommon
import os
import sys


def compile_url(url):
    return 'http://www.dytt8.net' + url


def get_movie_list(url, decode_type='utf-8'):
    movie_link_list = Common.CrawlerToHTML.get_links_from_html_separate(url, '/html/gndy/dyzz/2016', decode_type)
    movie_link_list = list(map(compile_url, movie_link_list))
    return movie_link_list


if __name__ == '__main__':
    my_index_url = 'http://www.dytt8.net/'
    my_real_movie_link_list = get_movie_list(my_index_url, 'gbk')
    search_movie_download_list = Common.CommonMovieCrawler.get_movie_download_list(my_real_movie_link_list, 'gbk',
                                                                                   False)
    Common.FileCommon.write_result_to_txt(search_movie_download_list, os.path.abspath('.'), 'movie2016.txt')
    # tv_url = 'http://www.ygdy8.com/html/tv/oumeitv/20151007/49245.html'
    # tv_list = get_tv_drama_program_list(tv_url, 'gbk')
    # write_result_to_txt(tv_list, os.path.abspath('.'), 'tv_drama_program_list.txt')
