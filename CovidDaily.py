import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import locale


class CovidDaily():
    def __init__(self, day):
        self.day=day
        self.root="COVID-19\\csse_covid_19_data\\"
        self.dailyreports="csse_covid_19_daily_reports\\"
        self.file_name=(self.root+self.dailyreports+self.day+".csv")
        self.report = pd.read_csv(self.file_name)
        self.report['deathsRate%']=(self.report['Deaths']/self.report['Confirmed'])*100
        self.report['recoveredRate%']=(self.report['Recovered']/self.report['Confirmed'])*100
        self.country_pops=pd.read_csv("E:\\Programing\\covid\\CountryPops.csv")
        #self.country_pops=pd.read_csv(fdesantis2855\\covid\\CountryPops.csv")
        self.worldPop=7773630000
        #pd.set_option('display.max_rows', 500)
        pd.set_option('display.max_columns', 10)
        #pd.set_option('display.width', 1000)
        
    def report_all(self): 
         return self.report

    def country(self,country):
        #Test for new format the exception is the old format    
        try:
            country_region="Country_Region"
            province_state="Province_State"
            test=self.report[country_region][0] 
        except:
            country_region="Country/Region"
            province_state="Province/State" 
 
        cdf=pd.DataFrame(data=None, columns=self.report.columns) 
        for i in self.report.index:
            if self.report[country_region][i] == country:
                row=self.report.iloc[i,:]
                cdf.loc[i,:]=row
                
        country_report=(cdf[[country_region, province_state,'Confirmed','Deaths','Recovered','deathsRate%','recoveredRate%']])
        country_report.sort_values([province_state],ascending=True)
        #print("  cdf  ",cdf)
        #print("Country Report ", country_report)
        
        # Calculate Totals
        print("");print(country," TOTALS")
        confirmed=country_report['Confirmed'].sum();        print("Confirmed :{:,}".format(confirmed))
        deaths=country_report['Deaths'].sum();              print("Deaths    :{:,}".format(deaths))
        recovered=country_report['Recovered'].sum();        print("Recovered :{:,}".format(recovered))
        deaths_p=((deaths/confirmed)*100);                  print("Deaths%   :{}".format(deaths_p))
        recovered_p=((recovered/confirmed)*100);            print("Recovered%:{}".format(recovered_p))
        print("")
        #
        new_row={country_region:'---', province_state:'--SUMMARY--','Confirmed':confirmed,'Deaths':deaths,'Recovered':recovered, 'deathsRate%':deaths_p, 'recoveredRate%':recovered_p}
        bottom_row=pd.DataFrame(data=None, columns=country_report.columns)
        bottom_row.append(new_row, ignore_index=True)
       
        country_report.append(bottom_row)
        country_report.country=country
        return(country_report)
    
    def state(self,country,state):
        #Test for new format the exception is the old format    
        try:
            format_new=True
            country_region="Country_Region"
            province_state="Province_State"
            test=self.report[country_region][0] 
        except:
            country_region="Country/Region"
            province_state="Province/State" 
            format_new=False
            
        state_report=pd.DataFrame(data=None, columns=self.report.columns)
        
        if format_new:
            for i in self.report.index:
                if self.report[country_region][i] == country and self.report[province_state][i] == state:
                    row=self.report.iloc[i,:]
                    state_report.loc[i,:]=row
        else:
            print("OLD FORMAT DETECTED AND CANNOT BE PARSED ACURATELY BY STATE")
            return()
        
        
        # Calculate Totals
        print("");print(state," TOTALS")
        confirmed=state_report['Confirmed'].sum(); print("Confirmed :",confirmed)
        deaths=state_report['Deaths'].sum(); print("Deaths   :",deaths)
        recovered=state_report['Recovered'].sum(); print("Recovered :",recovered)
        deaths_p=((deaths/confirmed)*100); print("Deaths%  :",deaths_p)
        recovered_p=((recovered/confirmed)*100); print("Recovered%:",recovered_p)
        print("")
        #
                
        return(state_report)                   

    def country_world_ratio(self,report):
        country=report.country
        #test=report.iloc(report["Country_Region"]=report.country)
        #Test for new format the exception is the old format    
        try:
            format_new=True; country_region="Country_Region"; province_state="Province_State"; test=report[country_region]
        except:
            format_new=False; country_region="Country/Region"; province_state="Province/State"
        
        #Find the row of the country
        #
        cpopdf=pd.DataFrame(data=None, columns=self.country_pops.columns)
    
        print(self.country_pops)
        found=False
        for i in self.country_pops.index:
            if found: break
            value=self.country_pops["Country/Territory"][i]; value=value.strip()
            if country in value:
                row=self.country_pops.iloc[i,:]
                cpopdf.loc[0,:]=row
                found=True
              
        pop=cpopdf["Population"][0]; 
        pop=int(pop.replace(",",""))
        
        #Caculate totals
        worldPop=int(self.worldPop)
        deaths=country_report['Deaths'].sum()
        confirmed=country_report['Confirmed'].sum()
        recovered=country_report['Recovered'].sum()
        deaths_p=((deaths/confirmed)*100); 
        recovered_p=((recovered/confirmed)*100); 
      
        DeathsPerState=( deaths/pop)*100
        ConfirmedPerState=( confirmed/pop )*100
        RecoveredPerState=( recovered/pop )*100
        
        DeathsPerWorld=(report['Deaths']/self.worldPop)*100
        ConfirmedPerWorld=(report['Confirmed']/self.worldPop)*100
        RecoveredPerWorld=(report['Recovered']/self.worldPop)*100
       
        confirmed=report['Confirmed'].sum();              
        ConfirmedPerWorld=confirmed/self.worldPop*100;       
        
        deaths=report['Deaths'].sum();                    
        deaths_p=((deaths/confirmed)*100);                
        DeathsPerWorld=((deaths/self.worldPop)*100);      
        
        recovered=report['Recovered'].sum();              
        recovered_p=((recovered/confirmed)*100);          
        RecoverdPerWorld=((recovered/self.worldPop)*100); 
        # 
        print("")
        print("World Population: {:,}".format(self.worldPop))
        print(country," TOTALS")
        print("Confirmed           : {:,}".format(confirmed))
        print("Confirmed % of World: {:.5f}".format(ConfirmedPerWorld))
        print("Deaths              : {:,}".format(deaths))
        print("Deaths%             : {:3f}".format(deaths_p))
        print("Deaths % of World   : {:.5f}".format(DeathsPerWorld))
        print("Recovered           : {:,}".format(recovered))
        print("Recovered%          : {:3f}".format(recovered_p))
        print("Recovered % of World: {:.5f}".format(RecoverdPerWorld))
        print("")
        #
        return() 
    
    
if __name__ == "__main__":
        cvd=CovidDaily("04-16-2020")
        #all=cvd.report_all()
        #print(all)
        country_report=cvd.country("Iran")
        #print(country_report)
        state_report=cvd.state("US", "New York")
        #print(state_report)
        country_ratio=cvd.country_world_ratio(country_report)
        print(country_ratio)
    
        
    