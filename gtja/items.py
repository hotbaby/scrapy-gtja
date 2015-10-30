
from scrapy.item import Item, Field

class AbstractItem(Item):
    url = Field()
    title = Field()
    date = Field()
    abstract = Field()
    
class ReportItem(Item):
    url = Field()
    date = Field()
    data = Field()
