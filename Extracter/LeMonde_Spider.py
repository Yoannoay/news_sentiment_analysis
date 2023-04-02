import scrapy 
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
import json 


sky_url = ["https://www.lemonde.fr/en/france/", "https://www.lemonde.fr/en/global-issues/"]



class LeMonde_Article_Spider(scrapy.Spider):
    name = "lemonde_article_scraper"
    data = []

    def __init__(self, *args, **kwargs):
        super(LeMonde_Article_Spider, self).__init__(*args, **kwargs)
        self.sky_news_data = pd.DataFrame(columns=['title', 'text'])

    def start_requests(self):
        
        yield scrapy.Request(url = "https://www.lemonde.fr/en/global-issues/", callback = self.parse)
        yield scrapy.Request(url = "https://www.lemonde.fr/en/france/", callback = self.parse)
        yield scrapy.Request(url = "https://www.lemonde.fr/en/united-states/", callback = self.parse)
        yield scrapy.Request(url = "https://www.lemonde.fr/en/united-kingdom/", callback = self.parse)
        yield scrapy.Request(url = "https://www.lemonde.fr/en/climate/", callback = self.parse)

    def parse(self, response):
        aod_link = Selector(response).css("a.article.article--nav::attr(href)").getall()
        for link in aod_link:
            yield response.follow(url = link, callback= self.standardise)

    def standardise(self, response):
        
        for item in response.css("html"):
            text_list = item.css("p.article__paragraph::text").getall()

            soup = BeautifulSoup(item.extract(), 'html.parser')

            #finding the first <script> tag with type application... 
            script_tag = soup.find('script', {'type': 'application/ld+json'})

            #extracting the content as a string and loading it as a dictionary
            json_data = json.loads(script_tag.string)

            topics = json_data['keywords']

            yield {
                'news_source': 'LeMonde News',
                'title' : item.css("title::text").get(),
                'article' : "".join(text_list),
                'topic' : topics
            }          
    


