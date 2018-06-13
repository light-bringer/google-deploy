import re

import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log


class CleanPipeline(object):
    def process_item(self, item, spider):
        try:
            item['Room_Size'] = re.search(r'\d+[,.]?\d*', item['Room_Size']).group()
        except AttributeError:
            pass

        try:
            item['Rate'] = re.search(r'\d+[,.]?\d*', item['Rate']).group()
        except AttributeError:
            pass

        return item


class MongoDBPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        # valid = True
        # for data in item:
        #     if not data:
        #         valid = False
        #         raise DropItem("Missing {0}!".format(data))
        # if valid:

        self.collection.insert(dict(item))

        # key = {'Url': item['Url']}
        # data = {'key2': 'value2', 'key3': 'value3'};
        # self.collection.update(key, dict(item), upsert=True)

        log.msg("Question added to MongoDB database!",
                level=log.DEBUG, spider=spider)

        return item

