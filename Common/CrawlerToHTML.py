#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Common.FileCommon
import urllib.request
from bs4 import BeautifulSoup
import re


def get_html(url, decode_type='utf-8'):
    f = urllib.request.urlopen(url)
    html_content = f.read().decode(decode_type, 'ignore')
    return html_content


def get_soup(url, decode_type='utf-8'):
    f = urllib.request.urlopen(url)
    html_content = f.read().decode(decode_type, 'ignore')
    soup = BeautifulSoup(html_content, 'lxml')
    return soup


def get_title_from_html(url, decode_type='utf-8'):
    soup = get_soup(url, decode_type)
    movie_title = soup.title.string
    return movie_title


def get_content_from_html(url, decode_type='utf-8'):
    soup = get_soup(url, decode_type)
    text = soup.get_text()
    return text


def get_links_from_html(url, separate='', decode_type='utf-8'):
    soup = get_soup(url, decode_type)
    link_list = []
    for link in soup.find_all('a'):
        real_link = link.get('href')
        if real_link == None:
            continue
        if real_link == 'None':
            continue
        if separate == '':
            link_list.append(real_link)
        else:
            if separate in real_link:
                link_list.append(real_link)
    return link_list


def images_crawler(url, reg):
    html = get_html(url)
    image_re = re.compile(reg)
    image_list = re.findall(image_re, html)
    return image_list


def save_images(image_list, target_path, target_dir):
    dir_path = Common.FileCommon.check_folder(target_path, target_dir)
    i = 0
    for image_url in image_list:
        image_path = dir_path + '/' + '%d.jpg' % i
        urllib.request.urlretrieve(image_url, image_path)
        i += 1
    return dir_path


if __name__ == '__main__':
    pass
