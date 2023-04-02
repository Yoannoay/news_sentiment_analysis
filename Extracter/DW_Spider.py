import scrapy 
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import pandas as pd
from datetime import datetime




class DW_Article_Spider(scrapy.Spider):
    name = "dw_article_scraper"
    data = []

    def __init__(self, *args, **kwargs):    
        super(DW_Article_Spider, self).__init__(*args, **kwargs)
        

    def start_requests(self):
        
        yield scrapy.Request(url = "https://www.dw.com/en/germany/s-1432", callback = self.parse)
        yield scrapy.Request(url = "https://www.dw.com/en/europe/s-1433", callback = self.parse)
        yield scrapy.Request(url = "https://www.dw.com/en/north-america/s-58267502", callback = self.parse)
        yield scrapy.Request(url = "https://www.dw.com/en/middle-east/s-14207", callback = self.parse)
        yield scrapy.Request(url = "https://www.dw.com/en/business/s-1431", callback = self.parse)
        yield scrapy.Request(url = "https://www.dw.com/en/environment/s-11798", callback = self.parse)
        yield scrapy.Request(url = "https://www.dw.com/en/sports/s-8171", callback = self.parse)
        

    def parse(self, response):
        aod_link = Selector(response).css("a.sc-hKMtZM.jifRHn.link-in-teaser::attr(href)").getall()
        for link in aod_link:
            yield response.follow(url = link, callback= self.standardise)

    def standardise(self, response):
        
        for item in response.css("html"):
            text_list = item.css("p::text").getall()
            topics = item.css("div[data-tracking-name='content-detail-kicker'] a::text").get()

            yield {
                'news_source': 'DW News',
                'title' : item.css("title::text").get(),
                'article' : "".join(text_list),
                'topic' : topics
            }          
    




