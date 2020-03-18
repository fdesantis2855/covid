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
    
def time_series(series_type):
    #series_type can be = Confirmed or Deaths or Recovered
    root = "COVID-19\\csse_covid_19_data\\"
    timeSeries = "csse_covid_19_time_series\\time_series_19-covid-"  
    series_name = (root+timeSeries+series_type+".csv")
    
    series_frame = pd.read_csv(series_name)
    return(series_frame)

def country_time_series(series_frame,country):
    country_series=pd.DataFrame(data=None, columns=series_frame.columns)
    for i in series_frame.index:
        if series_frame["Country/Region"][i] == country:
            row=series_frame.iloc[i,:]
            country_series.loc[i,:]=row      
    return(country_series)
       
def country_series_total(country_series,start_date,end_date):
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
    #print(country_totals)
    #print(  country_series.iloc[ind: , 4:]  )
    #Find the index of the start date and stop date called for 
    start_index=country_totals.columns.get_loc(start_date)
    #print("from ",start_index,start_date)
    end_index=country_totals.columns.get_loc(end_date)+1
    #print("to   ", end_index,end_date)
    #print(country_totals.iloc[-1:, start_index:end_index])
    country_totals_range=pd.DataFrame(data=None, columns=country_totals.columns)
    country_totals_range = country_totals.iloc[-1:, start_index:end_index]
    #print (  country_totals_range  )
    return (country_totals_range) 
  
def plot_country_totals(country_totals_range):
    #Extract country of interest
    country_of_interest=country_totals_range.index[0]  
    #Flip the table
    totals_transposed = country_totals_range.transpose()
  
    #Extract components  
    xticks=list(totals_transposed.index)
    values=(totals_transposed.values)
  
    
    print("");print(country_totals_range);print("")
    plt.plot(xticks,values)
    plt.ylabel('Deaths')
    plt.title(country_of_interest)
    plt.grid
    
    fig=plt.figure()
    ax=fig.add_subplot(111)
    for x,y in zip(xticks,values):
        point=y
        plt.annotate(point,(x,y),xytext=(0,10),ha='left')
    
    plt.show()
  
  
  
  
  
        
if __name__ == "__main__":
    #day="03-14-2020"
    #country="US"
    #report=daily_report(day)    
    #country_deaths=country_deathRate(report,country) 
    #country_recovered=country_recoveredRate(report,country)
    
    country="Italy"
    series_frame=time_series("Confirmed")
    country_series=country_time_series(series_frame,country)
    start_date="3/1/20"
    end_date="3/10/20"
    country_totals_range=country_series_total(country_series,start_date,end_date)
    plot_country_totals(country_totals_range)
    
    
           