#!/usr/bin/env python
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np


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
    try:
        country_region="Country/Region"
        province_state="Province/State"
        test=report[country_region][0]  
    except:
        country_region="Country_Region"
        province_state="Province_State"
    
    cdf=pd.DataFrame(data=None, columns=report.columns)
        
    
    for i in report.index:
        #if report["Country/Region"][i] == country:
        if report[country_region][i] == country:
            row=report.iloc[i,:]
            cdf.loc[i,:]=row
            
    ##country_deaths=(cdf[['Country/Region','Province/State','Confirmed','Deaths','deathsRate%']])
    ##country_deaths.sort_values(['Province/State'],ascending=True)
    country_deaths=(cdf[[country_region, province_state,'Confirmed','Deaths','deathsRate%']])
    country_deaths.sort_values([province_state],ascending=True)
    
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
    try:
        country_region="Country/Region"
        province_state="Province/State"
        test=report[country_region][0]  
    except:
        country_region="Country_Region"
        province_state="Province_State"
        test=report[country_region][0]
    
    crf=pd.DataFrame(data=None, columns=report.columns)
    
    for i in report.index:
        if report[country_region][i] == country:
            row=report.iloc[i,:]
            crf.loc[i,:]=row   
    
    country_recovered=(crf[[country_region, province_state, 'Confirmed','Recovered','recoveredRate%']])
    country_recovered.sort_values([province_state],ascending=True)
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
    

def time_series(series_type):
    series_type = series_type[0].lower() + series_type[1:]
    #series_type can be = Confirmed or Deaths or Recovered
    root = "COVID-19\\csse_covid_19_data\\"
    #timeSeries = "csse_covid_19_time_series\\time_series_19-covid-"  # removed to reflect new data structures
    #series_name = (root+timeSeries+series_type+".csv")               # removed to reflect new data structures
    timeSeries = "csse_covid_19_time_series\\time_series_covid19_"  
    series_name = (root+timeSeries+series_type+"_global.csv")
    
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
    
    #category=country_totals_range.category
    category= country_totals_range.category[0].upper() + country_totals_range.category[1:]
    print(category);print(country_totals_range);print("")
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
    
def growth_rate(country_totals_range):
        country_of_interest=country_totals_range.index[0]
        category=country_totals_range.category
        
        #Calculate Growth Rate Factors
        growth_list=[]
        growth_list_limit=country_totals_range.shape[1]-2
        i=0; j=0; growth_difference=[]
        for j in range(growth_list_limit):
            n1 = round(country_totals_range.iloc[i,j+1]-country_totals_range.iloc[i,j],2)
            growth_difference.append(n1)
            n2 = round(country_totals_range.iloc[i,j+2]-country_totals_range.iloc[i,j+1],2)
            if n2==0:
                growth_list.append(1)
            else:
                growth_list.append(  round((n2/n1),2) )
        growth_difference.append(n2)        
        
        #Display Growth Rate Factors
        category=country_totals_range.category+"-Growth Rate Factors"     
        print(country_of_interest);print(category);print(growth_list);print("")       
        
        #Setup to plot the Growth Rate Factor Line
        #EXTRACT x AXIS LABLES FROM THE DATAFRAME THAT WAS PASSED
        #   Flip the table
        totals_transposed = country_totals_range.transpose()
        #   Extract components  
        xlabels=list(totals_transposed.index)
        
        #Annotate the plot line
        i = 0; xlabels_adjusted=[]; xlabels_positions=[]
        for i in range(growth_list_limit):
            plt.annotate(growth_list[i],xy=(i,growth_list[i]),xytext=(0,0),textcoords="offset points",ha="left",va="bottom")
            
            #Create the Labels - postions adjusted due to nature of calculations
            newlabel=xlabels[i+2]
            xlabels_adjusted.append(newlabel)
            newposition=xlabels_adjusted.index(xlabels_adjusted[i])
            xlabels_positions.append(newposition)
           
            i=i+1
        plt.xticks(xlabels_positions, xlabels_adjusted)
        plt.xticks(rotation=40) 
    
        plt.title(country_of_interest)
        plt.ylabel(category)   
        plt.yscale("linear")
        plt.plot(growth_list)
        
        
        
        #Linear Regression Line - compile the index array
        x=[]
        for i in range(growth_list_limit):
            index_number=growth_list.index(growth_list[i])
            x.append(index_number)
        y=growth_list
        
        #Calculate and setup to plot the Regression Line
        x=np.array(x)
        y=np.array(y)
        m,b =np.polyfit(x,y,1)
        #plt.yscale("linear")
        plt.plot(x, m*x+b)
        
        plt.grid 
        plt.show()
        
        #Display Daily Growth Difference
        print("");print(country_of_interest);print("Daily Growth Diffference")
        print(growth_difference); print("")
        
        #Plot Daily Growth Difference ###################
        #####Annotate the plot line
        i = 0; gd_xlabels_adjusted=[]; gd_xlabels_positions=[]
        for i in range(growth_list_limit):
            plt.annotate(growth_difference[i],xy=(i,growth_difference[i]),xytext=(0,0),textcoords="offset points",ha="left",va="bottom")
            
            #Create the Labels - postions adjusted due to nature of calculations
            newlabel = xlabels[i+1]  
            gd_xlabels_adjusted.append(newlabel)
            newposition=gd_xlabels_adjusted.index(gd_xlabels_adjusted[i])
            gd_xlabels_positions.append(newposition)
           
            i=i+1    
        plt.xticks(gd_xlabels_positions, gd_xlabels_adjusted)
        plt.xticks(rotation=40)      
        plt.title(country_of_interest)
        plt.ylabel(country_totals_range.category+" - Daily Growth Difference")
        plt.yscale("linear")
        
        #Linear Regression Line - compile the index array
        growth_difference_limit=country_totals_range.shape[1]-1
        x=[]
        for i in range(growth_difference_limit):
            index_number=growth_difference.index(growth_difference[i])
            x.append(index_number)
        y=growth_difference
        
        #Calculate and setup to plot the Regression Line
        x=np.array(x)
        y=np.array(y)
        m,b =np.polyfit(x,y,1)
        plt.yscale("linear")
        plt.plot(x, m*x+b)
        plt.plot(growth_difference)
        plt.show()
        
        
        
        
if __name__ == "__main__":
    day="03-26-2020"
    country="US"
    report=daily_report(day)    
    
    country_deaths=country_deathRate(report,country) 
    #country_recovered=country_recoveredRate(report,country)
    #print (country_deaths)
    #print (country_recovered)
    
    print("");series_frame=time_series("Confirmed")
    country_series=country_time_series(series_frame,country)
    #print(country_series)
    
    start_date="3/1/20"
    end_date="3/28/20"
    country_totals_range=country_series_total(country_series,start_date,end_date)
    #print(country_totals_range)
    #plot_country_totals(country_totals_range)
    growth_rate(country_totals_range)
    