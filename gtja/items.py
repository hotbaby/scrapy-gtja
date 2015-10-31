
from scrapy.item import Item, Field

class ReportAbstractItem(Item):
    url = Field()
    title = Field()
    date = Field()
    abstract = Field()
    link = Field()
    
class ReportFileItem(Item):
    url = Field()
    date = Field()
    path = Field()
    link = Field()
