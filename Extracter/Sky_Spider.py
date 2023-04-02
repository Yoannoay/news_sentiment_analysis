import scrapy 
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import pandas as pd
from datetime import datetime

#I DONT THINK THIS IS USED SO KICK IT WHEN READY
sky_url = ["https://news.sky.com/world", "https://news.sky.com/uk"]



class Sky_Article_Spider(scrapy.Spider):
    name = "sky_article_scraper"
    data = []

    def __init__(self, *args, **kwargs):
        super(Sky_Article_Spider, self).__init__(*args, **kwargs)
        

    def start_requests(self):
        
        yield scrapy.Request(url = "https://news.sky.com/world", callback = self.parse)
        yield scrapy.Request(url = "https://news.sky.com/uk", callback = self.parse)
        yield scrapy.Request(url = "https://news.sky.com/us", callback = self.parse)
        yield scrapy.Request(url = "https://news.sky.com/business", callback = self.parse)
        yield scrapy.Request(url = "https://news.sky.com/climate", callback = self.parse)

    def parse(self, response):
        aod_link = Selector(response).css("h3.sdc-site-tile__headline > a::attr(href)").getall()
        for link in aod_link:
            yield response.follow(url = link, callback= self.standardise)

    def standardise(self, response):
        
        for item in response.css("html"):
            text_list = item.css("p::text").getall()
            yield {
                'news_source': 'Sky News',
                'title' : item.css("title::text").get(),
                'article' : "".join(text_list)
            }          
    




