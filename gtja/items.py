
from scrapy.item import Item, Field

class AbstractItem(Item):
    url = Field()
    title = Field()
    date = Field()
    abstract = Field()
    
class ReportItem(Item):
    file_urls = Field()
    files = Field()
