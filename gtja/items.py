
from scrapy.item import Item, Field

class ReportAbstractItem(Item):
    url = Field()
    title = Field()
    date = Field()
    create_date = Field()
    abstract = Field()
    link = Field()
    
class ReportFileItem(Item):
    url = Field()
    date = Field()
    create_date = Field()
    path = Field()
    link = Field()
