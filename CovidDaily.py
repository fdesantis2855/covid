import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

class CovidDaily():
    def __init__(self, day, country):
        self.day=day
        self.country=country
        self.root="COVID-19\\csse_covid_19_data\\"
        self.dailyreports="COVID-19\\csse_covid_19_data\\"
        self.file_name=(self.root+self.dailyreports,self.day+".csv")
        print(self.file_name)
    def report(self):
        #add rows for Death Ratio and Recovered Ratio    
        report = pd.read_csv(self.file_name)
        report['deathsRate%']=(report['Deaths']/report['Confirmed'])*100
        report['recoveredRate%']=(report['Recovered']/report['Confirmed'])*100
        return report

    def country_deathRate(self,report):
        cdf=pd.DataFrame(data=None, columns=report.columns)
        for i in report.index:
            if report["Country/Region"][i] == self.country:
                row=report.iloc[i,:]
                cdf.loc[i,:]=row

        country_deaths=(cdf[['Country/Region','Province/State','Confirmed','Deaths','deathsRate%']])
        country_deaths.sort_values(['Province/State'],ascending=True)
        sums = country_deaths.select_dtypes(pd.np.number).sum().rename('total')
        country_deaths.append(sums)
        return(country_deaths)

    def country_recoveredRate(self,report):
        crf=pd.DataFrame(data=None, columns=report.columns)
        for i in report.index:
            if report["Country/Region"][i] == self.country:
                row=report.iloc[i,:]
                crf.loc[i,:]=row   

        country_recovered=(crf[['Country/Region','Province/State','Confirmed','Recovered','recoveredRate%']])
        country_recovered.sort_values(['Province/State'],ascending=True)
        sums = country_recovered.select_dtypes(pd.np.number).sum().rename('total')
        country_recovered.append(sums)
        return(country_recovered)
    
    
if __name__ == "__main__":
        cvd=CovidDaily("3-13-2020","US")
        daily=cvd.report() 
    
        
    