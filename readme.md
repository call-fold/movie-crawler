## MovieCrawler
## 电影爬虫

----

### 环境需求:
* python3.X
* redis

### pip list:
* lxml: 3.6.4
* beautifulsoup4: 4.5.1
* redis: 2.10.5

### 使用指南:
1.安装python3.x+环境, 推荐使用[pyenv](https://github.com/yyuu/pyenv)搭建纯净python环境, 自用python3.4.3
<br></br>
2.通过pip安装包:
```bash
sudo apt-get install libxml2-dev libxslt1-dev
pip install -r requirements.txt
```
3.取首页热门电影:
```bash
python movie_crawler_from_home_page.py
```
输出结果在top_movies目录下
<br></br>
4.搜索电影, 输入电影名:
```bash
python movie_search.py
```
输出结果在search_movies目录下
<br></br>
5.安装[redis](http://redis.io/), 默认:
```bash
host='127.0.0.1', port=6379, db=0
```
6.取豆瓣Top250电影, 存入redis:
```bash
python store_topN_movies_from_douban.py
```
7.从redis中取TopN电影(最大250):
```bash
python get_topN_movies_from_douban.py
```
输出结果在top_n_from_douban目录下
8.从电影天堂爬取全站数据, 存入redis中:
```bash
host='127.0.0.1', port=6379, db=1
```
```bash
python crawl_the_whole_movie_site.py
```
9.从redis中查询电影:
```
python movie_search_from_redis.py
```

<br></br>

### 集成到Django Blog中
#### 传送门: [电影搜索器](http://slfweb.com/movie_search/)
![movie_search](https://cloud.githubusercontent.com/assets/12811161/20725873/490df944-b6ae-11e6-884e-f6bf11142226.png)

### 更新列表:
* 2017-02-12: 将电影数据存入Redis中, [电影搜索器](http://slfweb.com/movie_search/)从Redis中取数据
* 2016-11-30: 完成与Django博客的集成, [电影搜索器](http://slfweb.com/movie_search/), 位于[博客-实验室](http://slfweb.com/laboratory/)下
* 2016-11-29: 一页多ftp链接问题
* 2016-11-24: 处理输入空格BUG, 完善翻页功能
* 2016-11-23: 取豆瓣Top250电影的下载地址
* 2016-11-18: 完善安装使用指南, 热门电影去重
* 2016-11-17: 完成翻页功能, 完善正则匹配
* 2016-11-16: 输入电影, 搜索对应电影, 并输出下载地址
* 2016-11-14: 从电影天堂网站, 获取热门电影(2016年)下载地址

### 待完成:
* 增加定时任务调度, 更新Redis电影数据库
* ~~翻页功能~~
* 搜索结果, 电影和电视剧未做区分
* 下载功能

### 注:
* 没有找到链接的电影不会生成*.txt

### BUG List:
* ~~处理电影名中间的空格~~

----