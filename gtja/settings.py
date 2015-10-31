
BOT_NAME = "gtja"
BOT_VERSION = "1.0"

SPIDER_MODULES = ["gtja.spiders"]
NEWSPIDER_MODULE = ["gtja.spiders"]
USER_AGENT = "%s/%s" % (BOT_NAME, BOT_VERSION)


ITEM_PIPELINES = {
    "gtja.pipelines.MongoDBStorage": 1,
}

FILES_STORE_PATH = r"G:/data/gtja/report/"


MONGODB_SERVER = "192.168.199.167"
MONGODB_PORT = 27017
MONGODB_DB = "gtja"
MONGODB_COLLECTION = "report"


COOKIE = {
    "nc":2,
    "loginncName":"49a49a49a95a116a111a104a0",
    "zbhLoginType":2,
    "loginUserName":"49a49a49a95a116a111a104a0",
    "JSESSIONID":"GLQHWvHSSj8qpQbLmHGtFvG1d4W6py8vgLB1zVwSpbT8pLn2cBf4!1451595514",
    "junhongLoginType":2,
    "count":-2,
    }

