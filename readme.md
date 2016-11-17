## MovieCrawler
## 电影爬虫

----

#### pip list:
* lxml: 3.6.4
* beautifulsoup4: 4.5.1

#### 使用指南:
1.安装python3.x+环境, 推荐使用pyenv搭建纯净python环境, [pyenv](https://github.com/yyuu/pyenv), 自用python3.4.3
<br></br>
2.通过pip安装包:
```bash
sudo apt-get install libxml2-dev libxslt1-dev
pip install -r requirements.txt
```
<br></br>
3.取首页热门电影:
```bash
python MovieCrawlerFromHomePage.py
```
输出结果在top_movies目录下
<br></br>
4.搜索电影, 输入电影名:
```bash
python MovieSearch.py
```
输出结果在search_movies目录下

#### 功能列表:
* 2016-11-18: 完善安装使用指南, 热门电影去重
* 2016-11-17: 完成翻页功能, 完善正则匹配
* 2016-11-16: 输入电影, 搜索对应电影, 并输出下载地址
* 2016-11-14: 从电影天堂网站, 获取热门电影(2016年)下载地址

#### 待完成:
* ~~翻页功能~~
* 下载功能

----