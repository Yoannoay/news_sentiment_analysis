import scrapy 
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import pandas as pd
from datetime import datetime





#I DONT THINK THIS IS USED SO KICK IT WHEN READY
sky_url = ["https://www.cbsnews.com/world/", "https://www.cbsnews.com/us/"]



class CBS_Article_Spider(scrapy.Spider):
    name = "cbs_article_scraper"
    data = []

    def __init__(self, *args, **kwargs):
        super(CBS_Article_Spider, self).__init__(*args, **kwargs)
        
        

    def start_requests(self):
        
        yield scrapy.Request(url = "https://www.cbsnews.com/world/", callback = self.parse) 
        yield scrapy.Request(url = "https://www.cbsnews.com/us/", callback = self.parse)
        yield scrapy.Request(url = "https://www.cbsnews.com/politics/", callback = self.parse)
        yield scrapy.Request(url = "https://www.cbsnews.com/science/", callback = self.parse)
        yield scrapy.Request(url = "https://www.cbsnews.com/moneywatch/", callback = self.parse)
        yield scrapy.Request(url = "https://www.cbsnews.com/crime/", callback = self.parse)


    def parse(self, response):
        aod_link = Selector(response).css("a.item__anchor::attr(href)").getall()
        for link in aod_link:
            yield response.follow(url = link, callback= self.standardise)

    def standardise(self, response):
        
        for item in response.css("html"):
            text_list = item.css("p::text").getall()
            print(text_list)
            yield {
                'news_source': 'CBS News',
                'title' : item.css("h1.content__title ::text").get(),
                'article' : "".join(text_list),
                'topic' : response.css("meta[name='news_keywords']::attr(content)").get()
            }     
          
    
