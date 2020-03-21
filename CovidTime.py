import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

class CovidTime():
    
    def __init__(self, category):
        #One of Three categories = Confirmed, Deaths or Recovered
        self.category = category
        self.root = "COVID-19\\csse_covid_19_data\\"
        self.timeSeries = "csse_covid_19_time_series\\time_series_19-covid-"  
        self.series_name = (self.root+self.timeSeries+self.category+".csv")
        self.series_frame =pd.read_csv(self.series_name)
        #print(self.series_frame)
        self.country_series=pd.DataFrame(data=None, columns=self.series_frame.columns)
        self.country_totals=pd.DataFrame(data=None, columns=self.country_series.columns)
        self.country='US'
        self.country_totals_range=pd.DataFrame(data=None, columns=self.country_totals.columns)
        pd.set_option('display.max_colwidth', 20)
        pd.set_option('display.max_columns', 12)
        pd.set_option('display.width', 200)
        
    def report_all(self):
        return(self.series_frame)

    def location(self,country):
        #Overwrite the initial value for the country
        self.country=country
        for i in self.series_frame.index:
            if self.series_frame["Country/Region"][i] == country:
                row=self.series_frame.iloc[i,:]
                self.country_series.loc[i,:]=row  
        return(self.country_series)

    def totals(self, start_date, end_date):
        #Extract Country Name
        country_of_interest=self.country
        
        #Form the totals row
        self.country_series.loc[country_of_interest] = self.country_series.sum()
        # Find the absolute index number of the last row which now is the totals row
        ind = (self.country_series.shape[0])-1
        
        #Note country_totals is initialized in init as a new dataframe for the totals using same column names as original
        #self.country_totals=pd.DataFrame(data=None, columns=country_series.columns)
        
        #Extract the total row into a the seperate data frame
        self.country_totals = self.country_series.iloc[ind: , 4:]

        
        #Find the index of the start date and stop date called for 
        start_index=self.country_totals.columns.get_loc(start_date)
        end_index=self.country_totals.columns.get_loc(end_date)+1
        
        #Note: country_total_range is initalized in init 
        #country_totals_range=pd.DataFrame(data=None, columns=country_totals.columns)
        self.country_totals_range = self.country_totals.iloc[-1:, start_index:end_index]
        print("");print(self.category)
        print(self.country_totals_range);print("")
        return (self.country_totals_range)             

    def plot_totals(self):
        #Extract country of interest
        country_of_interest=self.country_totals_range.index[0]  
        
        #Flip the table
        totals_transposed = self.country_totals_range.transpose()
        
        #Extract components  
        xticks=list(totals_transposed.index)
        values=list(totals_transposed.values)

        print("");print(country_totals_range);print("")
        plt.plot(xticks,values)

        i = 0
        for x,y in zip(xticks,values):
            xindex=xticks.index(x)
            yindex=values.index(y)
            print(xindex, yindex)
            plt.annotate(values[i],xy=(xindex,y),xytext=(1,1),textcoords="offset points",ha="left",va="bottom")
            i=i+1
         

        plt.ylabel(self.country)
        plt.title(country_of_interest)
        plt.grid 
        plt.show()
        
if __name__ == "__main__":     
        
    series=CovidTime("Confirmed")
    #series=time.report_all()
    
    country=series.location("US")
    #print(country)
    
    totals=series.totals("3/10/20","3/19/20")
    #print(totals)
     
    series.plot_totals
    
   
        