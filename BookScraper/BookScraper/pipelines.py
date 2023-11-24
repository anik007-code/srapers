# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json

import redis
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscraperPipeline:

    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        name = adapter.get('Name')
        if name is not None:
            name.strip()
        self.store_in_redis(item)
        return item

    def store_in_redis(self, item):
        try:
            self.redis_client.delete('Books')
            item_json = json.dumps(item)
            self.redis_client.lpush('Books', item_json)
            print(f"Item pushed to Redis: {item}")
        except Exception as e:
            print(f"Error of redis client is - : {e}")
