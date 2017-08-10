#!/usr/bin/env bash

# source http://stackoverflow.com/questions/23222616/copy-all-keys-from-one-db-to-another-in-redis
#set connection data accordingly
source_host=localhost
source_port=6379
source_db=2
target_host=localhost
target_port=6379
target_db=4

#copy all keys without preserving ttl!
/home/slf/dev/redis-3.2.5/src/redis-cli -h $source_host -p $source_port -n $source_db keys \* | while read key;
do
    /bin/touch /var/log/movie_crawler/copy_redis.log
    /bin/echo "Copying $key" >> /var/log/movie_crawler/copy_redis.log
    /home/slf/dev/redis-3.2.5/src/redis-cli --raw -h $source_host -p $source_port -n $source_db DUMP "$key" | head -c -1 | /home/slf/dev/redis-3.2.5/src/redis-cli -x -h $target_host -p $target_port -n $target_db RESTORE "$key" 0
done