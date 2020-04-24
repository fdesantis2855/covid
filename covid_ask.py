import os
import subprocess

os.system("cls")
os.system("color e")

#variable initialization
daily_instance=0; time_instance=0
countrysave = "US"; categorysave = "Confirmed"
startsave = "4/1/20"; endsave = "4/20/20"
localesave = "S"; statesave = "California"; countysave = "Orange"
dayreportsave="04-22-2020"; localereportsave= "S"; countryreportsave = "US"; statereportsave = "California"

session=True
while session == True:
    print("");print("COVID PANDEMIC INFORMATION");print("")
    print("");print("Select Type of Information");print("")
    branch=         input (' Covid Daily Reports (DR) or Time Range (TR) or (q) to quit  : ')
    print(branch)
    
    if branch=="q" or branch=="Q" or branch=="Quit": session = False
    
    if branch == "TR" or branch =="tr":
        os.system("color b")
        os.system("cls")
        #print("");print("Loading Johns Hopkins Covid Time Series Information...");print("")
        #os.system("cls")
        if time_instance==0: 
            print("");print("Loading Johns Hopkins Covid Time Range Information...");print("")
            from CovidTime import CovidTime
            os.system("cls")
        print("");   print('Covid Time Range Information');print("")
        country =    input (f'Country of Interest  (Press Enter for {countrysave})  : ') or countrysave
        category =   input (f'Desired category - "Confirmed", "Deaths", "Recovered"   (Press Enter for {categorysave}): ') or categorysave
        start_date = input (f'START DATE for the time window of interest     (Press Enter for {startsave})              : ') or startsave 
        end_date =   input (f'END DATE for the time window of interest      (Prese Enter for {endsave})              : ') or endsave 
        
        
        obj=CovidTime(category)
        
        countrysave=country
        categorysave=category
        startsave=start_date
        endsave=end_date
   
        if country == "US":  # For "US" process for National or State or County numbers
            print("...")
            locale = input(f'NATIONAL numbers OR Specific STATE OR Specific COUNTY numbers ? - (N) or (S) or (C)  (Press Enter for {localesave} ) : ') or localesave    
            #print("::",locale,localesave)
            if locale=="S" or locale=="s" or locale=="state" or locale=="State" or locale=="STATE":
                state =      input (f'STATE of Interest   (Press Enter for {statesave} ): ') or statesave
                #print(":::",state,"::",statesave)
                
                obj.us_state(state, start_date, end_date)
                
                statesave=state
           
            elif locale=="C" or locale == "c" or locale=="county" or locale=="County" or locale=="COUNTY": 
                state =      input (f'STATE of Interest     (Press Enter for {statesave}) : ') or statesave
                print(":::",state,"::",statesave)
                county =     input (f'COUNTY of Interest   (Press Enter for  {countysave}): ') or countysave
                #print(":::",county,"::",countysave)
                obj.us_county(county, state, start_date, end_date)
                
                statesave=state; countysave=county
        
            elif locale == "N" or locale=="n" or locale=="National" or country != "US":
                location=obj.location("US")
                totals = obj.totals(start_date,end_date)
                try:
                    obj.plot_totals()
                except:
                    print("Time window selected has no numbers for the country of interest. Try Again")
            
            localesave=locale
        
        elif country != "US":
            location=obj.location(country)
            totals = obj.totals(start_date,end_date)
            try:
                    obj.plot_totals()
            except:
                    print("Time window selected has no numbers for the country of interest. Try Again")
        
        time_instance+=1    
    
    elif branch == "DR" or branch == "dr" or branch =="Dr":
        os.system("color a")
        #print("");print("Loading Johns Hopkins Covid Daily Report Information");print("")
        #from CovidDaily import CovidDaily
        #os.system("cls")
        
        if daily_instance==0: 
            os.system("cls")
            print("");print("Loading Johns Hopkins Covid Daily Information...");print("")
            from CovidDaily import CovidDaily
            os.system("cls")
       
        print("");   print('Covid Daily Information');print("")
        dayreport =    input (f'Desired Day for Report  (Press Enter for {dayreportsave})  : ') or dayreportsave
        #Create Daily object
        daily=CovidDaily(dayreport)
        
        countryreport = input (f'Country of Interest  (Press Enter for {countryreportsave})  : ') or countryreportsave
        
        if countryreport != "US":
            daily.country(countryreport)
        
        elif countryreport == "US":
            localereport = input(f'NATIONAL OR STATE OR Report ? - (N) or (S)  (Press Enter for {localereportsave} ) : ') or localereportsave
            
            if localereport == "N" or localereport =="n" or localereport =="National" or countryreport != "US":
                daily.country("US")
                
                localereportsave=localereport
                
            elif localereport == "S" or localereport == "s" or localereport == "state" or localereport == "STATE" or localereport == "State":
                statereport =      input (f'Report for which STATE ? -  (Press Enter for {statereportsave} ): ') or statereportsave
                daily.state("US",statereport)
                
                localereportsave=localereport; statereportsave=statereport
        
        daily_instance+=1                                         
 
os.system("color 7")