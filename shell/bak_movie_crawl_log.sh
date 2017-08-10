#!/usr/bin/env bash

/bin/mv /var/log/movie_crawler/movie_crawler.log /var/log/movie_crawler/movie_crawler.$(/bin/date +"\%Y\%m\%d\%H\%M").log
/bin/touch /var/log/movie_crawler/movie_crawler.log