import psycopg2 
from datetime import datetime, timedelta



class Chooser:

    def __init__(self):
        self.choose_news_source()
        self.choose_date()
        

    def choose_news_source(self):

        #The dictionary which contains the choices to make it easier to link a choice to a value. Rather than multiple if x then y

        source_dict = {"1": "sky_news", "2" : "cbs_news", "3" : "lemonde_news", "4" : "dw_news"}

        print("""Hello welcome to the News Analysis Application! \nThe following are the available news sources: \n 
              1. Sky News (England)\n 
              2. CBS News (America)\n 
              3. Le Monde News (France) \n 
              4. DW News Germany \n """)
              
        one_or_multiple = input("""Would you like to use one or multiple news sources (Type in the relevant number and press enter): 
                                \n  1. One \n or \n 2. Multiple \n""")
        
        if one_or_multiple == "1":
            news_source = input("Please enter the number of the news source you would like to look into: \n ")

            self.news_choice = str(source_dict.get(news_source))
            print(self.news_choice)
            return self.news_choice
            

        
        elif one_or_multiple == "2":

            self.choices = []
        # asking for the news sources.
            news_choices = input("Please enter the numbers corresponding to the news sources you are interested in: \n")
        # only use text which is an integer and therefore meant as a key (this is to hopefully side step any variations in input)
            text = news_choices.strip(" ")
            
            for element in text:
                if element.isdigit():
                    self.choices.append(str(source_dict.get(element)))

            print(self.choices)
            return self.choices 
                    





    def choose_date(self):


        conn = psycopg2.connect(host='localhost', database='world_news',
                                user='postgres', password ='supremeoverlordYC7')
        cur = conn.cursor()
        # getting both the earliest and latest dates available
        cur.execute("SELECT MIN(date) FROM sky_news")
        min_date = cur.fetchone()[0]

        cur.execute("SELECT MAX(date) FROM sky_news")
        max_date = cur.fetchone()[0]

        # execute code depending on option chosen.
        options = {"1": self.istoday, "2": self.lastndays(7), "3": self.lastndays(30)}

        choice = input("""Please pick from the below what period of time you would like to analyse:\n 1. Today\n 2. These last 7 days (Week)\n 3. These past 30 days (Month)\n 4. A specific day/ range of days\n """)

        text = choice.strip()

        if text.isdigit() and text != "4":
            options.get(text)()

        elif text == "4":
            start_date = input(f"Please enter the start date with the following format 'YYYY-MM-DD' (MUST BE BETWEEN THESE DATES: {min_date} - {max_date}): \n ")
            end_date = input(f"Please enter the end date with the following format 'YYYY-MM-DD'(MUST BE BETWEEN THESE DATES: {min_date} - {max_date}): \n ")
            self.range_of_days(start_date, end_date)

    def istoday(self):
        now = datetime.now()
        self.day_choice = f"{now.year}-{now.month}-{now.day}"
        return self.day_choice

    def lastndays(self, n):
        def inner():
            self.day_choice = []
            n_days_ago = datetime.now() - timedelta(days=n)

            while n_days_ago < datetime.now():
                self.day_choice.append(n_days_ago.strftime('%Y-%m-%d'))
                n_days_ago += timedelta(days=1)

            return self.day_choice
        return inner

    def range_of_days(self, start, end):
        # start date
        start_date = datetime.strptime(start, "%Y-%m-%d")

        # end date
        end_date = datetime.strptime(end, "%Y-%m-%d")

        # timedelta object representing the time between two dates
        delta = end_date - start_date
        self.day_choice = []
        for i in range(delta.days + 1):
            day = start_date + timedelta(days=i)
            self.day_choice.append(day.strftime("%Y-%m-%d"))

        return self.day_choice



test = Chooser()
