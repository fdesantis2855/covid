from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandasql import sqldf


class CovidTime():
    
    def __init__(self, category):
        #One of Three categories = Confirmed, Deaths, Recovered 
        self.category = category[0].lower() + category[1:]
        #self.country_pops=pd.read_csv("E:\\Programing\\covid\\CountryPops.csv")
        #self.country_pops=pd.read_csv(CountryPops.csv)
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
    
    def us_state(self,state, start_date, end_date):
        # Read in the US data frame
        self.timeSeries = "csse_covid_19_time_series\\time_series_covid19_" 
        us_frame_name = (self.root+self.timeSeries+self.category+"_US.csv")
        us_frame =pd.read_csv(us_frame_name)
        
        #Create the State dataframe
        state_frame=pd.DataFrame(data=None, columns=us_frame.columns) 
        
        #Sort for out all state records into the State dataframe
        state_frame=us_frame.loc[us_frame['Province_State']==state]
        
        #Drop the columns that are not needed to display
        state_series_display=state_frame
        state_series_display=state_series_display.drop(['UID','iso2','iso3','code3','FIPS','Lat','Long_','Combined_Key'],axis=1)
        
        #Sum up all the State numbers
        state_sum = state_series_display.sum(skipna=True, numeric_only=True)
        state_sum.state=state
        
        #Sub divide based on time
        state_sum_time=state_sum[start_date: end_date]
        
        #Output the State Sums per date
        Category=self.category[0].upper() + self.category[1:]
        print("");print(state+" "+"State "+Category+" Daily Totals - "+start_date+" - "+end_date)
        print(state_sum_time)
        print("END "+state+" "+"State "+Category+" Daily Totals - "+start_date+" - "+end_date) ;print("")
        
        #PLOT STATE CURVE
        #Configure Plot Window Title and Size
        fig=plt.figure(figsize=(12,5))
        fig.canvas.set_window_title(state+" "+Category+" Cases - "+start_date+" - "+end_date)
        
        # Annotate the plot with values
        i = 0; values_array=state_sum_time.values
        for y in (values_array):
            value="{:,.0f}".format(values_array[i])
            text=plt.annotate(value,xy=(i,y),xytext=(-5,5),textcoords="offset points",ha="left",va="bottom",rotation=80)
            text.set_fontsize(10)
            i=i+1 
            
        #Configure the Plot
        plt.title(state,fontsize=20)
        plt.ylabel(self.category[0].upper() + self.category[1:],fontsize=16)
        plt.tick_params(labelsize=9)
        plt.xticks(rotation=25) 
        plt.yscale("log")
        plt.plot(state_sum_time, self.line_color())
        plt.show()
        
        #Return the State dataframe        
        return(state_frame)
    
    def us_county(self,county, state, start_date, end_date):
        
        # Read in the US data frame
        self.timeSeries = "csse_covid_19_time_series\\time_series_covid19_" 
        us_frame_name = (self.root+self.timeSeries+self.category+"_US.csv")
        us_frame =pd.read_csv(us_frame_name)
        
        #Create the State dataframe
        county_frame=pd.DataFrame(data=None, columns=us_frame.columns) 
        
        #Sort for out all state records into the State dataframe
        county_frame=us_frame.loc[(us_frame['Province_State']==state) & (us_frame["Admin2"]==county)]
        
        #Drop the columns that are not needed to display
        county_series_display=county_frame
        county_series_display=county_series_display.drop(['UID','iso2','iso3','code3','FIPS','Lat','Long_','Combined_Key'],axis=1)
        
        #Sum up all the State numbers
        county_sum = county_series_display.sum(skipna=True, numeric_only=True)
        county_sum.state=county
        
        #Sub divide based on time
        county_sum_time=county_sum[start_date: end_date]
        
        #Output the State Sums per date
        Category=self.category[0].upper() + self.category[1:]
        print("");print(county+" County, "+state+" State "+Category+" Daily Totals - "+start_date+" - "+end_date)
        print(county_sum_time)
        print("END "+county+" County, "+state+" State "+Category+" Daily Totals - "+start_date+" - "+end_date) ;print("")
        
        #PLOT county CURVE
        #Configure Plot Window Title and Size
        fig=plt.figure(figsize=(12,5))
        fig.canvas.set_window_title(county+" County, "+state+" State "+Category+" Daily Totals - "+start_date+" - "+end_date)
        
        # Annotate the plot with values
        i = 0; values_array=county_sum_time.values
        for y in (values_array):
            value="{:,.0f}".format(values_array[i])
            text=plt.annotate(value,xy=(i,y),xytext=(-5,5),textcoords="offset points",ha="left",va="bottom",rotation=80)
            text.set_fontsize(10)
            i=i+1 
            
        #Configure the Plot
        plt.title((county+' County, '+state),fontsize=20)
        plt.ylabel(self.category[0].upper() + self.category[1:],fontsize=16)
        plt.tick_params(labelsize=9)
        plt.xticks(rotation=25) 
        plt.yscale("log")
        plt.plot(county_sum_time, self.line_color())
        plt.show()
        
        #Return the State dataframe        
        return(county_frame)
    
    

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
        plt.yscale("log")
        plt.title(country_of_interest,fontsize=20)
        
        # Annotate the plot with values 
        i = 0
        for y in (values):
            value=values[i]; value=''.join(map(str,value)); value=int(value)
            value="{:,.0f}".format(value)
            text=plt.annotate(value,xy=(i,y),xytext=(-5,5),textcoords="offset points",ha="left",va="bottom",rotation=75)
            text.set_fontsize(9)
            i=i+1 
        
        plt.grid(True, which='major',axis='x',color='y',linewidth=.25,animated=True)
       
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
            growth_list.append(  round(((n2/n1)),2)  )
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
        
        plt.yscale("log")
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
        #plt.title(country_of_interest)
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
          
        plt.grid(True, which='major',axis='x',color='y',linewidth=.25,animated=True)
        plt.show()
    
        return(self.country_pops)
    
    
    def logistics_plot(self, country, start_date, end_date):    
       
        category1="Confirmed"
        category2="Deaths"
        
        confirmed=CovidTime(category1)
        confirmed_country=confirmed.location(country)
        confirmed_time=confirmed.totals(start_date,end_date)

        deaths=CovidTime(category2)
        deaths_country=deaths.location(country)
        deaths_time=deaths.totals(start_date,end_date)
        
        #logitics curve  1-new cases/pop
        #country=self.country_totals_range.index[0]
        country_spaced=" "+country
        
        Category1=category1[0].upper()+category1[1:]  
        Category2=category2[0].upper()+category2[1:] 
        cpop=self.country_pops
        
        #index=cpop.loc[cpop['Country/Territory']==country].index
        #pop=cpop.iloc[index]['Population']
        pop=cpop.iloc[ cpop.loc[cpop['Country/Territory']==country_spaced].index ]['Population']
      
        #Extract the value from the Series pop    
        #print("pop.values[0] ",pop.values[0])
        pop_string=(pop.values[0])     
        population=int(pop_string.replace(",",""))
         
        growth_list=[]
        growth_list_limit=deaths_time.shape[1]-1
        
        logistics=pd.DataFrame(data=None, index=confirmed_time.index, columns=confirmed_time.columns) 

        #Calculate diff data frames
        i=0;  j=0; k=0; countlist=[]; growth_difference=[]; 
        for j in range(growth_list_limit):
            deaths_diff = deaths_time.iloc[i,j+1]-deaths_time.iloc[i,j]
            confirmed_diff = confirmed_time.iloc[i,j+1]-deaths_time.iloc[i,j]
            l=((1-(confirmed_diff/population)) * confirmed_time.iloc[i,j])
            logistics[logistics.columns[j+1]]=l
         
        #Flip the Dataframe on its side
        logistics_table=logistics.iloc[0]
        #Trim off 1st row with NAN for the value
        logistics_table=logistics_table[1:]
        
        #PLOT LINE CONFIGURATION
        fig=plt.figure(figsize=(12,6))
        fig.canvas.set_window_title(country+" Logistics Curve - "+start_date+" - "+end_date) 
        color=self.line_color() 
        plt.xticks(rotation=70)
        plt.tick_params(labelsize=9)
        plt.ylabel("Deaths / Confirmed Ratio")
        plt.yscale("log")
        plt.title(country,fontsize=20)
        
        #  Annotate the plot with values 
        for index in range(deaths_time.shape[1]-1):
            value="{:.03f}".format(logistics_table[index])
            y=float(value)
            #print(value,logistics_table[index])
            text = plt.annotate(value,xy=(index, y),xytext=(0,0),textcoords="offset pixels",ha="left",va="bottom",rotation=75)
            text.set_fontsize(7)
            #index=index+1   
        
        plt.plot(logistics_table)
        plt.grid(True, which='major',axis='x',color='y',linewidth=.25,animated=True)
        plt.show()
        
        
        print(population) 
       
        
            
            
            
            
            
if __name__ == "__main__":      
   
    start="2/1/20"; end="4/20/20"
    country="US"
    category1="Confirmed"
    category2="Deaths"
    category3="Recovered"    
    
    #confirmed=CovidTime(category1)
    #deaths=CovidTime(category2)
    recovered=CovidTime(category3)
    
    #US_confirmed=confirmed.location(country)
    #US_deaths=deaths.location(country)
    #US_recovered=recovered.location(country)
    
    #US_confirmed_totals=confirmed.totals(start,end)
    #confirmed.plot_totals()
    #US_deaths_totals=deaths.totals(start,end)
    #deaths.plot_totals()
    #US_recovered_totals=recovered.totals(start,end)
    #recovered.plot_totals()
    recovered.growth_rate()
