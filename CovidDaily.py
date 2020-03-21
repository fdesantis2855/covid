import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

class CovidDaily():
    def __init__(self, day):
        self.day=day
        self.root="COVID-19\\csse_covid_19_data\\"
        self.dailyreports="csse_covid_19_daily_reports\\"
        self.file_name=(self.root+self.dailyreports+self.day+".csv")
        self.report = pd.read_csv(self.file_name)
        self.report['deathsRate%']=(self.report['Deaths']/self.report['Confirmed'])*100
        self.report['recoveredRate%']=(self.report['Recovered']/self.report['Confirmed'])*100
        #pd.set_option('display.max_rows', 500)
        #pd.set_option('display.max_columns', 500)
        #pd.set_option('display.width', 1000)
        
    def report_all(self): 
         return self.report

    def country(self,country):
        cdf=pd.DataFrame(data=None, columns=self.report.columns)
        
        for i in self.report.index:
            if self.report["Country/Region"][i] == country:
                row=self.report.iloc[i,:]
                cdf.loc[i,:]=row
                
        country_report=(cdf[['Country/Region','Province/State','Confirmed','Deaths','Recovered','deathsRate%','recoveredRate%']])
        country_report.sort_values(['Province/State'],ascending=True)
        #print("  cdf  ",cdf)
        #print("Country Report ", country_report)
        
        # Calculate Totals
        print("");print(country," TOTALS")
        confirmed=country_report['Confirmed'].sum(); print("Confirmed :",confirmed)
        deaths=country_report['Deaths'].sum(); print("Deaths   :",deaths)
        recovered=country_report['Recovered'].sum(); print("Recovered :",recovered)
        deaths_p=((deaths/confirmed)*100); print("Deaths%  :",deaths_p)
        recovered_p=((recovered/confirmed)*100); print("Recovered%:",recovered_p)
        print("")
        #
        new_row={'Country/Region':'---','Province/State':'--SUMMARY--','Confirmed':confirmed,'Deaths':deaths,'Recovered':recovered, 'deathsRate%':deaths_p, 'recoveredRate%':recovered_p}
        bottom_row=pd.DataFrame(data=None, columns=country_report.columns)
        bottom_row.append(new_row, ignore_index=True)
       
        country_report.append(bottom_row)
        return(country_report)

    
if __name__ == "__main__":
        cvd=CovidDaily("03-19-2020")
        #report=cvd.report_all()
        #print(report)
        country_report=cvd.country("US")
        #print(country_report)
        
    
        
    