
# -*- coding: UTF-8 -*-

import os
import datetime
import hashlib
from urllib import unquote

from scrapy import log
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request, FormRequest
from scrapy.conf import settings
from scrapy.utils.spider import iterate_spider_output
from scrapy.spiders import Spider

from gtja.items import ReportAbstractItem, ReportFileItem

class Rule(object):
    
    def __init__(self, link_extractor, callback=None, follow=None):
        self.link_extractor = link_extractor
        self.callback = callback
        self.follow = follow


class GtjaSpider(Spider):
    """ General configuration of the Crawl Spider """
    name = "gtja"
    allowed_domains = ["gtja.com"]
    start_urls = [
        #Strategy research
        #"http://www.gtja.com/fyInfo/uplusReportsListInner.jsp?catType=8&keyWord=",
        
        #Bond research
        #"http://www.gtja.com/fyInfo/uplusReportsListInner.jsp?catType=7&keyWord=",
        
        #Financial engineering
        #"http://www.gtja.com/fyInfo/uplusReportsListInner.jsp?catType=6&keyWord=",
        
        #Company research
        #"http://www.gtja.com/fyInfo/uplusReportsListInner.jsp?catType=5&keyWord=",

        #Industry research
        #"http://www.gtja.com/fyInfo/uplusReportsListInner.jsp?catType=4&keyWord=",
        
        #Macro research
        #"http://www.gtja.com/fyInfo/uplusReportsListInner.jsp?catType=3&keyWord=",
        
        #Latest report
        "http://www.gtja.com/fyInfo/uplusReportsListInner.jsp?catType=1&keyWord=",
    ]

    rules = [
        Rule(LinkExtractor(allow=[r"/fyInfo/contentForJunhong\.jsp"]), callback="parse_abstract", follow=True), #Report abstract
        Rule(LinkExtractor(allow=[r"/share/commons/ShowNotesDocumentFile\.jsp"]), callback="download_report"), #Report file
    ]
    
    suspend_request = []

    def __init__(self, *args, **kwargs):
        super(GtjaSpider, self).__init__(*args, **kwargs)
        self.compile_rules()
    
    def compile_rules(self):
        def get_method(method):
            if callable(method):
                return method
            elif isinstance(method, basestring):
                return getattr(self, method, None)
            else:
                assert(False)
        for rule in self.rules:
            rule.callback = get_method(rule.callback)
    
    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, cookies=settings["COOKIE"])
                
    def parse(self, response):
        return self.parse_response(response, callback=None, follow=True)
    
    def parse_response(self, response, callback=None, follow=False):
        
        if callback is not None:
            result = callback(response) or ()
            for requests_or_item in iterate_spider_output(result):
                yield requests_or_item
        
        if follow is True:
            for i, rule in enumerate(self.rules):
                for link in rule.link_extractor.extract_links(response): 
                    request = Request(url=link.url, callback=self.response_download)
                    request.meta.update(rule=i, link_text=link.text, link_url=link.url)
                    self.suspend_request.append(request)
        else:
            pass
                    
        self.add_next_operation(response)
        
        for request in self.suspend_request:
            yield request

    def response_download(self, response):
        rule = self.rules[response.meta["rule"]]
        return self.parse_response(response, callback=rule.callback, follow=rule.follow)
    
    def add_next_operation(self, response):
        """ Parse page info from html. """

        DOMAIN = "http://www.gtja.com"
        REPORT_LIST_URL = "/fyInfo/uplusReportsListInner.jsp" 
        if response.url.find(REPORT_LIST_URL) == -1:
            return
        
        hxs = HtmlXPathSelector(response)
        
        catType = 1
        keyWord = ""
        current_page = hxs.select("//td[@class='f12blue2 tdr']//span/text()").extract()[0]
        rows = hxs.select("//td[@class='f12blue2 tdr']//span/text()").extract()[3]
        pages = hxs.select("//td[@class='f12blue2 tdr']//span/text()").extract()[1]
        
        current_page = int(current_page)
        pages = int(pages)
        if current_page < pages:
            current_page = current_page + 1
            request = FormRequest(
                url=DOMAIN + REPORT_LIST_URL,
                formdata={"catType":str(catType), "keyWord":str(keyWord), "current_page":str(current_page+1), "rows":str(rows), "pages":str(pages)},
                callback=self.parse,
                )
            self.suspend_request.append(request)
        else:
            pass

    def parse_abstract(self, response):
        """ Extract data from html. """

        hxs = HtmlXPathSelector(response)
        item = ReportAbstractItem()

        url = response.url
        title = hxs.select("//td[@class='f20blue tdc']/text()").extract()[0]
        date = hxs.select("//div[@class='f_black f_14']/text()").extract()[0]
        abstract = hxs.select("//table[@class='f_black f_14']//td").extract()[0]
        link = hxs.select("//a[contains(@href,'ShowNotesDocumentFile')]/@href").extract()[0]
        link = "http://www.gtja.com" + link
        
        item["url"] = url
        item["title"] = title
        item["date"] = datetime.datetime.strptime(date, "%Y-%m-%d")
        item["abstract"] = abstract
        item["link"] = link
        return item

    def download_report(self, response):
        """ Download the report pdf. """
        def get_filename_from_url(url):
            #http://www.gtja.com/f//lotus/201510/20151023%20Company%20Report%2001816%20HK_addStamper_addEncrypt.pdf
            import re
            pattern = re.compile("http://www.gtja.com/f//lotus/(\d+)/(.*)")
            result = pattern.match(url)
            if result is None:
                return str(datetime.date.today()), hashlib.md5(url).hexdigest() + ".pdf"
            else:
                #return str(datetime.date.today()), hashlib.md5(url).hexdigest() + ".pdf"
                return result.group(1), unquote(result.group(2))
        
        date, name = get_filename_from_url(response.url) #TODO Create date directory.

        file_path = settings["FILES_STORE_PATH"] + date + "/"
        if os.path.exists(file_path) != True:
            os.mkdir(file_path)

        filename = file_path + name
        with open(filename.decode("utf-8"), "wb") as f: #TODO what is the diffenrence between "w+" and "wb"
            f.write(response.body)
            
        item = ReportFileItem()
        item["url"] = unquote(response.url)
        item["date"] =  date
        item["path"] =  "/" + date + "/" + name #Relative path
        item["link"] = response.meta["link_url"]
        return item

