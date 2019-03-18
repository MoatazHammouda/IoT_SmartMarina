import json
import pandas as pd
import numpy as np
import seaborn as sns

#beautiful plots
sns.set(rc={'figure.figsize':(11, 4)})


def getWeather(year):
  
    #its a json file
    with open('weatherYear.txt') as f:
        data = json.load(f)
        
    #temporal arrays, pd works with np.datetime64 (really convenient time operations possible)
    time = np.array([], dtype=np.datetime64)
    temp = np.array([])
    
    #json file has entry almanac_summaries, subentry almanac_dt is date, subentry mean_temp is temperature
    for x in data["almanac_summaries"]:
        
        monthDay = x["almanac_dt"]
        month =  monthDay[:2]
        day = monthDay[2:]
        try:
            time = np.append(time, pd.to_datetime(year + "-"+month + "-" + day))
            temp = np.append(temp, x["mean_temp"])
            
        #pd.to_datetime throughs error because of leap year 
        except ValueError as e: 
            if str(e) != "day is out of range for month":
                raise
                
    data = pd.Series(temp, index=time)
    

    
    return data

def getData():
    
    
    sdata = pd.read_csv("smartMarinaAg.csv", sep=",", names=["id", "time", "value"],
                        skiprows=2, thousands=',')
    
    #drop nans
    sdata = sdata.dropna(axis=0)
    
    sdata["time"] = pd.to_datetime(sdata["time"])
    sdata = sdata.set_index("time")
    
    #cool time operations for later
    
    #sdata["Weekday Name"] = sdata.index.weekday_name
    #sdata["hour"] = sdata.index.hour
    #sdata["month"] = sdata.index.month
    
    #split data into plugs
    ids = sdata["id"].unique()
    data = list() #list of plugs
    dataNan = list() #second versions with NaN entries, I need this later...
    
    for id_value in ids:
        data.append(sdata.loc[ sdata["id"] == id_value])
    
    
    for i in range(len(data)):
        #average current over one day
        data[i] = data[i].resample("D").agg({'value':'mean','id':'last'})
        #resample("D") creates NaN entries because it creates a continiuous
        #flow of time but not at every day is current recorded
        dataNan.append(data[i].copy()) #save NaN version
        #thus deelete NaN
        data[i] = data[i].dropna(axis=0)
    
    for d in data:
        
    
        #inserting weather data into dataframe in correct position
        weather = getWeather("2018") #year is arbitrary (useless)
        temp = np.array([])
    
        for t in d.index:
    
            for tw in weather.index:
                 if t.day == tw.day and t.month == tw.month:
                     temp = np.append(temp, weather[tw])
                     
                     break
      
        #add temp column with temperature
        d["temp"] = temp
        
        
    return data, dataNan
    
     




