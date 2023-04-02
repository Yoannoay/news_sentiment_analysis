#Triggers the processes in order 
from Extracter.Spider_central import SpiderCentral


def run():
   #spider central has a function to determine if there has already been a csv created for today, if there has it wont run. 
    go_spiders = SpiderCentral()
    


if __name__ == '__main__':
    run()