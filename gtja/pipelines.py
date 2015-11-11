
from pymongo import MongoClient

from scrapy.conf import settings
from scrapy.exceptions import DropItem

from gtja.items import ReportAbstractItem, ReportFileItem

class MongoDBAbstractStorage(object):

    def __init__(self, *args, **kwargs):
        connection = MongoClient(settings["MONGODB_SERVER"], settings["MONGODB_PORT"])
        db = connection[settings["MONGODB_DB"]]
        self.collection = db[settings["MONGODB_COLLECTION_REPORT_ABSTRACT"]]
   
    def process_item(self, item, spider):
        
        if isinstance(item, ReportAbstractItem):
            self.collection.insert(dict(item))
        return item
    
    
class MongoDBFileStorage(object):
    
    def __init__(self, *args, **kwargs):
        connection = MongoClient(settings["MONGODB_SERVER"], settings["MONGODB_PORT"])
        db = connection[settings["MONGODB_DB"]]
        self.collection = db[settings["MONGODB_COLLECTION_REPORT_FILE"]]
        
    def process_item(self, item, spider):
        
        if isinstance(item, ReportFileItem):
            self.collection.insert(dict(item))
        return item
    
    

