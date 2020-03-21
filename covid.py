#!/usr/bin/env python
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

def daily_report(day):
    
    root = "COVID-19\\csse_covid_19_data\\"
    dailyReports = "csse_covid_19_daily_reports\\"
    timeSeries = "csse_covid_19_time_series"
    
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
    #
    category="Deaths"
    print(country," TOTALS")
    confirmed=country_deaths['Confirmed'].sum(); print("Confirmed :",confirmed)
    deaths=country_deaths['Deaths'].sum(); print("Death     :",deaths)
    death_p=(deaths/confirmed)*100; print("Deaths%   :",death_p)
    #new_row={'Country/Region':'','Province/State':'--SUMMARY--','Confirmed':confirmed,'Deaths':deaths,'deathsRate%':death_p}
    #country_deaths.append(new_row, ignore_index=True)
    #
    country_deaths.category=category
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
    #
    category="Recovered"
    print(country," TOTALS")
    confirmed=country_recovered['Confirmed'].sum(); print("Confirmed :",confirmed)
    recovered=country_recovered['Recovered'].sum(); print("Recovered :",recovered)
    recovered_p=(recovered/confirmed)*100; print("Recovered%:",recovered_p)
    #new_row={'Country/Region':'---','Province/State':'--SUMMARY--','Confirmed':confirmed,'Recovered':recovered,'recoveredRate%':recovered_p}
    #bottom_row=pd.DataFrame(data=None, columns=country_recovered.columns)
    #country_recovered.append(bottom_row,ignore_index=True)
    #
    country_deaths.category=category
    sums = country_recovered.select_dtypes(pd.np.number).sum().rename('total')
    country_recovered.append(sums)
    return(country_recovered)
    
def time_series(series_type):
    #series_type can be = Confirmed or Deaths or Recovered
    root = "COVID-19\\csse_covid_19_data\\"
    timeSeries = "csse_covid_19_time_series\\time_series_19-covid-"  
    series_name = (root+timeSeries+series_type+".csv")
    
    series_frame = pd.read_csv(series_name)
    series_frame.category=series_type
    return(series_frame)

def country_time_series(series_frame,country):
    country_series=pd.DataFrame(data=None, columns=series_frame.columns)
    country_series.category=series_frame.category
    for i in series_frame.index:
        if series_frame["Country/Region"][i] == country:
            row=series_frame.iloc[i,:]
            country_series.loc[i,:]=row      
    return(country_series)
       
def country_series_total(country_series,start_date,end_date):
    country_series_total.category=country_series.category
    origin_date="1/22/20"
    #Extract Country Name
    country_of_interest=country_series.iloc[0]["Country/Region"]
    #Form the totals row
    country_series.loc[country_of_interest] = country_series.sum()
    # Find the index of the totals row 
    ind = (country_series.shape[0])-1
    #Initialize a new dataframe for the totals using same column names as original
    country_totals=pd.DataFrame(data=None, columns=country_series.columns)
    #Extract the total row into a the seperate data frame
    country_totals = country_series.iloc[ind: , 4:]
    
    #Find the index of the start date and stop date called for 
    start_index=country_totals.columns.get_loc(start_date)
    end_index=country_totals.columns.get_loc(end_date)+1
    
    country_totals_range=pd.DataFrame(data=None, columns=country_totals.columns)
    country_totals_range = country_totals.iloc[-1:, start_index:end_index]
    country_totals_range.category = country_series.category
    
    return (country_totals_range) 
  
def plot_country_totals(country_totals_range):
    #Extract country of interest
    country_of_interest=country_totals_range.index[0]  
    #Flip the table
    totals_transposed = country_totals_range.transpose()
  
    #Extract components  
    xticks=list(totals_transposed.index)
    plt.xticks(rotation=30)
    values=list(totals_transposed.values)
    
    print(country_totals_range.category)
    print("");print(country_totals_range);print("")
    plt.plot(xticks,values)
    
    i = 0
    for x,y in zip(xticks,values):
        xindex=xticks.index(x)
        yindex=values.index(y)
        #plt.annotate(values[i],xy=(xindex,yindex),textcoords="offset points",ha="left",va="top")
        plt.annotate(values[i],xy=(xindex,int(y)),xytext=(0,0),textcoords="offset points",ha="left",va="bottom")
        i=i+1
    
    plt.ylabel(country_totals_range.category)
    plt.title(country_of_interest)
    plt.grid 
    plt.show()
  
        
if __name__ == "__main__":
    day="03-17-2020"
    country="US"
    report=daily_report(day)    
    
    #country_deaths=country_deathRate(report,country) 
    #country_recovered=country_recoveredRate(report,country)
    #print (country_deaths)
    #print (country_recovered)
    
    country="US"
    print("");series_frame=time_series("Recovered")
    country_series=country_time_series(series_frame,country)
    #print(country_series)
    
    start_date="3/10/20"
    end_date="3/20/20"
    country_totals_range=country_series_total(country_series,start_date,end_date)
    #print(country_totals_range)
    plot_country_totals(country_totals_range)
    
    
           