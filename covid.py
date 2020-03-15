#!/usr/bin/env python
import pandas as pd


def daily_report(day):
    
    root = "COVID-19\\csse_covid_19_data\\"
    dailyReports = "csse_covid_19_daily_reports\\"
    
    file_name = (root+dailyReports+day+".csv")
    
    #add rows for Death Ratio and Recovered Ratio    
    report = pd.read_csv(file_name)
    report['deathsRate%']=(report['Deaths']/report['Confirmed'])*100
    report['recoveredRate%']=(report['Recovered']/report['Confirmed'])*100
   
    return report    


def country_deathRate(report,country):
    cdf=pd.DataFrame(data=None, columns=report.columns)
    for i in report.index:
        if report["Country/Region"][i] == country:
            row=report.iloc[i,:]
            cdf.loc[i,:]=row
            
    country_deaths=(cdf[['Country/Region','Province/State','Confirmed','Deaths','deathsRate%']])
    country_deaths.sort_values(['Province/State'],ascending=True)
    sums = country_deaths.select_dtypes(pd.np.number).sum().rename('total')
    country_deaths.append(sums)
    return(country_deaths)
    
def country_recoveredRate(report,country):
    crf=pd.DataFrame(data=None, columns=report.columns)
    for i in report.index:
        if report["Country/Region"][i] == country:
            row=report.iloc[i,:]
            crf.loc[i,:]=row   
    
    country_recovered=(crf[['Country/Region','Province/State','Confirmed','Recovered','recoveredRate%']])
    country_recovered.sort_values(['Province/State'],ascending=True)
    sums = country_recovered.select_dtypes(pd.np.number).sum().rename('total')
    country_recovered.append(sums)
    return(country_recovered)
    
        
if __name__ == "__main__":
    day="03-14-2020"
    country="US"
    report=daily_report(day)    
    country_deaths=country_deathRate(report,country) 
    country_recovered=country_recoveredRate(report,country)
    print( country_deaths )
    #print( country_recovered )
           