#Where all the spiders are called to run.
from scrapy.crawler import CrawlerProcess
from Cleaning.Cleaner import Cleaner
from Cleaning.Logger import Logger
from Extracter.Sky_Spider import Sky_Article_Spider
from Extracter.CBS_Spider import CBS_Article_Spider
from Extracter.LeMonde_Spider import LeMonde_Article_Spider
from Extracter.DW_Spider import DW_Article_Spider
import scrapy
from scrapy import signals

import datetime
import os 
import pandas as pd 

class SpiderCentral():

    spiders = ["CBS_News_Articles", "Sky_News_Articles", "LeMonde_News_Articles", "DW_News_Articles" ]


    def __init__(self):
        self.to_run()
        

    
     
    def to_run(self):
        
        
       
        self.spiders_2_go = []
        for spider in self.spiders:
                source = spider.split("_")[0]
                name = f"{source}_Article_Spider"
                self.spiders_2_go.append(name)

                

        process = CrawlerProcess()
        for spider in self.spiders_2_go:
            channel = spider.split("_")[0]
            news_store = f"{channel}_news_articles.csv"
            process = CrawlerProcess(settings = {
            'FEED_URI': news_store,
            'FEED_FORMAT': 'csv'
            })
            process.crawl(globals()[spider])
        
        # start all spiders present in the list
        process.start() 

        for spiders in self.spiders_2_go:
            source = spiders.split("_")[0].lower()
            func_name = f"run_{source}_spider"
            class_name = f"{source}_Spider"
            getattr(self, func_name)()   

    


    #running the relevant functions for each spider
    def run_sky_spider(self):

        process = CrawlerProcess(settings = {
            'FEED_URI': 'Sky_news_articles.csv',
            'FEED_FORMAT': 'csv'
        })

        
        
        sky = Cleaner("Sky_news_articles.csv")
        sky.sky_create_topic_col()
        log = Logger("Sky_News", "Sky_News_Articles", "Sky_news_articles.csv")
        

    
    def run_cbs_spider(self):
        
        process = CrawlerProcess(settings = {
        'FEED_URI': 'CBS_news_articles.csv',
        'FEED_FORMAT': 'csv'
        })
        cbs = Cleaner("CBS_news_articles.csv")
        cbs.cbs_cleaner()
        
        log = Logger("CBS_News", "CBS_News_Articles","CBS_news_articles.csv")
        # log.reset()



    def run_lemonde_spider(self):

        process = CrawlerProcess(settings = {
        'FEED_URI': 'LeMonde_news_articles.csv',
        'FEED_FORMAT': 'csv'
        })


        
        
        log = Logger("LeMonde_News", "LeMonde_News_Articles","LeMonde_news_articles.csv")



    def run_dw_spider(self):

        process = CrawlerProcess(settings = {
            'FEED_URI': 'DW_news_articles.csv',
            'FEED_FORMAT': 'csv'
        })

        dw = Cleaner("DW_news_articles.csv")
        dw.dw_cleaner()
        log = Logger("DW_News", "DW_News_Articles","DW_news_articles.csv")
        
