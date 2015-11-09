
BOT_NAME = "gtja"
BOT_VERSION = "1.0"

SPIDER_MODULES = ["gtja.spiders"]
NEWSPIDER_MODULE = ["gtja.spiders"]
USER_AGENT = "%s/%s" % (BOT_NAME, BOT_VERSION)


ITEM_PIPELINES = {
    "gtja.pipelines.MongoDBAbstractStorage": 1,
    "gtja.pipelines.MongoDBFileStorage": 2,
}

FILES_STORE_PATH = r"G:/data/gtja/report/"


MONGODB_SERVER = "192.168.1.9"
MONGODB_PORT = 27017
MONGODB_DB = "gtja"
MONGODB_COLLECTION_REPORT_ABSTRACT = "report_abstract"
MONGODB_COLLECTION_REPORT_FILE = "report_file"
MONGODB_COLLECTION_REPORT_VISITED = "report_visited"

EXPIRE_DAYS = 2

COOKIE = {
    "nc":2,
    "loginncName":"49a49a49a95a116a111a104a0",
    "zbhLoginType":2,
    "loginUserName":"49a49a49a95a116a111a104a0",
    "JSESSIONID":"GLQHWvHSSj8qpQbLmHGtFvG1d4W6py8vgLB1zVwSpbT8pLn2cBf4!1451595514",
    "junhongLoginType":2,
    "count":-2,
    }

