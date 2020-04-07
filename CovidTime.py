import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

class CovidTime():
    
    def __init__(self, category):
        #One of Three categories = Confirmed, Deaths, Recovered 
        self.category = category[0].lower() + category[1:]
        self.country_pops=pd.read_csv("E:\\Programing\\covid\\CountryPops.csv")
        self.worldPop=7773630000
        self.root = "COVID-19\\csse_covid_19_data\\"
        #self.timeSeries = "csse_covid_19_time_series\\time_series_19-covid-"  # removed to reflect new data structures
        #self.series_name = (self.root+self.timeSeries+self.category+".csv")   # removed to reflect new data structures
        self.timeSeries = "csse_covid_19_time_series\\time_series_covid19_" 
        self.series_name = (self.root+self.timeSeries+self.category+"_global.csv")
        self.series_frame =pd.read_csv(self.series_name)
        #print(self.series_frame)
        self.country_series=pd.DataFrame(data=None, columns=self.series_frame.columns)
        self.country_totals=pd.DataFrame(data=None, columns=self.country_series.columns)
        self.country='US'
        self.country_totals_range=pd.DataFrame(data=None, columns=self.country_totals.columns)
        pd.set_option('display.max_rows', 500)
        pd.set_option('display.max_colwidth', 25)
        pd.set_option('display.max_columns', 12)
        pd.set_option('display.width', 200)
        
    
    def line_color(self):
        color={"confirmed":"blue", "deaths":"red", "recovered":"green"}
        plot_line=color.get(self.category)
        return(plot_line)
        
    def report_all(self):
        return(self.series_frame)
        
    def world(self, start_date, end_date):
        wtdf=pd.DataFrame(data=None, columns=self.series_frame.columns);    
        wtdf2=pd.DataFrame(data=None, columns=self.series_frame.columns); 
        wtdf=self.series_frame.sum(numeric_only=True); 
        wtdf2 = wtdf[0:][2:]; 
        
        wtdf3=wtdf2.loc[start_date : end_date]
        labels_array=wtdf3.index
        values_array=wtdf3.values
        
        #Plot the world data
        category = self.category[0].upper() + self.category[1:]
        fig=plt.figure(figsize=(12,5))
        fig.canvas.set_window_title("World"+ " "+category+" Cases"+" "+start_date+" "+end_date)
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)

        plt.title("World",fontsize=20)
        plt.ylabel(self.category)
        plt.tick_params(labelsize=9)
        plt.xticks(rotation=30) 
        color=self.line_color()
        plt.plot(wtdf3,color)
        plt.yscale("linear")
        
        # Annotate the plot with values
        i = 0
        for y in (values_array):
            value="{:,.0f}".format(values_array[i])
            text=plt.annotate(value,xy=(i,y),xytext=(-5,5),textcoords="offset points",ha="left",va="bottom",rotation=80)
            text.set_fontsize(8)
            i=i+1  
             
        plt.show()
        return()    
        
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
        xticks=totals_transposed.index
        values=totals_transposed.values

        category = self.category[0].upper() + self.category[1:]
        fig=plt.figure(figsize=(12,5))
        fig.canvas.set_window_title(country_of_interest+" "+ category +" Cases") 
        color=self.line_color()
        plt.plot( xticks,values,color=color )
        plt.xticks(rotation=30)
        plt.tick_params(labelsize=9)
        plt.ylabel(self.category)
        plt.yscale("linear")
        plt.title(country_of_interest,fontsize=20)
        
        # Annotate the plot with values 
        i = 0
        for y in (values):
            value=values[i]; value=''.join(map(str,value)); value=int(value)
            value="{:,.0f}".format(value)
            text=plt.annotate(value,xy=(i,y),xytext=(-5,5),textcoords="offset points",ha="left",va="bottom",rotation=75)
            text.set_fontsize(9)
            i=i+1 
        
        plt.grid 
       
        plt.show()
        
        
    def growth_rate(self):
        country_of_interest=self.country_totals_range.index[0]
        category=self.category[0].upper()+self.category[1:]
        growth_list=[]
        growth_list_limit=self.country_totals_range.shape[1]-2
        
        #Calculate growth factors
        i=0; j=0; countlist=[]; growth_difference=[]
        for j in range(growth_list_limit):
            n1 = self.country_totals_range.iloc[i,j+1]-self.country_totals_range.iloc[i,j]
            n2 = self.country_totals_range.iloc[i,j+2]-self.country_totals_range.iloc[i,j+1]
            growth_difference.append(n1)
            if n1==0: n1=1
            #n2 = self.country_totals_range.iloc[i,j+1]
            growth_list.append(  round(((n1/n2)),2)  )
        growth_difference.append(n2)
        
        print(category);print(growth_list)          
        
        #SETUP TO PLOT
        #Setup Window
        category = self.category[0].upper() + self.category[1:]
        fig=plt.figure(figsize=(12,8))
        fig.canvas.set_window_title(country_of_interest+ " "+category+" Cases Growth")

        
        #1st subplot
        plt.subplot(2,1,1)
        #EXTRACT x AXIS LABLES FROM THE DATAFRAME THAT WAS PASSED
        #   Flip the table
        totals_transposed = self.country_totals_range.transpose()
        #   Extract components  
        xlabels=list(totals_transposed.index)
        
        plt.yscale("linear")
        color=self.line_color()
        plt.plot(growth_list,color)    
        plt.ylabel(self.category+" - Growth Factors")
        plt.title(country_of_interest, fontsize=20)
        #  Annotate the 1st subplot with values
        i = 0; xlabels_adjusted=[]; xlabels_positions=[]
        for i in range(growth_list_limit):
            text = plt.annotate(growth_list[i],xy=(i,growth_list[i]),xytext=(-5,5),textcoords="offset points",ha="left",va="bottom",rotation=75)
            text.set_fontsize(8)
            
            #Create the Labels - postions adjusted due to nature of calculations
            newlabel=xlabels[i+2]
            xlabels_adjusted.append(newlabel)
            newposition=xlabels_adjusted.index(xlabels_adjusted[i])
            xlabels_positions.append(newposition)
            
            i=i+1
            
        plt.xticks(xlabels_positions, xlabels_adjusted)
        plt.xticks(rotation=35)         
        plt.tick_params(labelsize=8)
        
        #  1st subplot - Linear Regression Line - compile the index array
        x=[]
        for i in range(growth_list_limit):
            index_number=growth_list.index(growth_list[i])
            x.append(index_number)
        y=growth_list
        #  Calculate and setup to plot the Regression Line
        x=np.array(x)
        y=np.array(y)
        m,b =np.polyfit(x,y,1)
        plt.yscale("linear")
        plt.plot(x, m*x+b)
        ####### 1st suplot End ######
        
        #Plot 2nd subplot- Growth Difference
        plt.subplot(2,1,2)
        #  Annotate the plot 2nd subplot line
        i = 0; gd_xlabels_adjusted=[]; gd_xlabels_positions=[]
        for i in range(growth_list_limit):
            difference="{:,.0f}".format(growth_difference[i])
            text = plt.annotate(difference,xy=(i,growth_difference[i]),xytext=(0,0),textcoords="offset pixels",ha="left",va="bottom",rotation=75)
            text.set_fontsize(8)
            
            #Create the Labels - postions adjusted due to nature of calculations
            newlabel = xlabels[i+1]  
            gd_xlabels_adjusted.append(newlabel)
            newposition=gd_xlabels_adjusted.index(gd_xlabels_adjusted[i])
            gd_xlabels_positions.append(newposition)
           
            i=i+1   
             
        plt.xticks(gd_xlabels_positions, gd_xlabels_adjusted)
        plt.xticks(rotation=35) 
        plt.tick_params(labelsize=8)     
        plt.title(country_of_interest)
        plt.ylabel(self.category+" - Growth Difference")
        plt.yscale("linear")
        
        #  2nd subpot -  Linear Regression Line
        #    compile the index array
        growth_difference_limit=self.country_totals_range.shape[1]-1
        x=[]
        for i in range(growth_difference_limit):
            index_number=growth_difference.index(growth_difference[i])
            x.append(index_number)
        y=growth_difference
        
        #  2nd subplot - Calculate and setup to plot the Regression Line
        x=np.array(x)
        print(x)
        y=np.array(y)
        print(y)
        plt.yscale("linear")
        m,b =np.polyfit(x,y,1)
        plt.plot(x, m*x+b)
        color=self.line_color
        plt.plot(growth_difference)
        plt.tick_params(labelsize=9)
        #plt.xticks(rotation=35) 
          
        plt.show()
    
        return(self.country_pops)
            
if __name__ == "__main__":     
        
    series=CovidTime("Deaths")
    world=series.world("3/5/20","4/5/20")
   
    
    #series=time.report_all()
    
    country=series.location("US")
    #print(country)
    
    totals=series.totals("3/5/20","4/5/20")
    #print(totals)
     
    series.plot_totals()
    
    series.growth_rate()
    
        