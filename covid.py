#!/usr/bin/env python
import csv


def daily_report(day,keyfield):
  
    path = "COVID-19\\csse_covid_19_data\\csse_covid_19_daily_reports\\"
    file_name = (path+day+".csv")

    table = {}
    with open(file_name, "rt", newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='|')
        
    #with open("COVID-19\\csse_covid_19_data\\csse_covid_19_daily_reports\\03-13-2020.csv", newline='') as csvfile:
        #reader = csv.DictReader(csvfile, delimiter=',', quotechar='|')    
        
        for row in reader:
            table[row[keyfield]] = row
            print( table )
        return table

        
if __name__ == "__main__":
    daily_report("03-13-2020","Country/Region")    
               


