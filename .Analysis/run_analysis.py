from Analyser import Analyser
def run():
    #trying to just control what analysis is done by using inpu, but input isnt called and so the call to the analyser class fails due to no arguement
    analysis_trigger = input("Would you like any visualisation: Y/N? \n ")
    if analysis_trigger == "Y":
        analysis_option = input("Choose from the following options: \n 1. Topic_sentiment (Stacked Bar Chart) \n")
        execute_analysis = Analyser(analysis_option)


if __name__ == '__main__':
    run()