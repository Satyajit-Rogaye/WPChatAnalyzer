import re
import pandas as pd
import sys
import numpy as np
import streamlit as st

def preprocessor(data):
    sys.stdout.reconfigure(encoding='utf-8')#solving unicodeencoderor

    pattern='\d{1,2}/\d{1,2}/\d{2}, \d{1,2}:\d{2}\s?[AP]M -'

    messages=re.split(pattern,data)[1:]

    dates=re.findall(pattern,data)

    df=pd.DataFrame({'Messages':messages,'Message_Date':dates})
    # Replace narrow no-break space with normal space

    df['Message_Date'] = df['Message_Date'].str.replace('\u202f', ' ', regex=False)

    df['Message_Date'] = pd.to_datetime(df['Message_Date'], format="%m/%d/%y, %I:%M %p -")

    df.rename(columns={'Message_Date':'Date'},inplace=True)

    #seperating users and messages

    users=[]
    Messages=[]
    for msg in df['Messages']:
        entry=re.split('([\w\W]+?):\s',msg)
        if entry[1:]:#user name
            users.append(entry[1])
            Messages.append(entry[2])
        else:
            users.append('Message notification')
            Messages.append(entry[0])

    df['User Name']=users
    df['User Messages']=Messages
    df.drop(columns=['Messages'],inplace=True)
    df['Year']=df['Date'].dt.year
    df['Month']=df['Date'].dt.month_name()
    df['Month_Num']=df['Date'].dt.month
    df['Day']=df['Date'].dt.day
    df['Hours']=df['Date'].dt.hour
    df['Minutes']=df['Date'].dt.minute 
    df['Only_Date']=df['Date'].dt.date
    df['Day_Name']=df['Date'].dt.day_name()

    period=[]
    for hour in df[['Day_Name','Hours']]['Hours']:
        if hour == 23:
            period.append(str(hour) + "-"+str('00'))
        elif hour == 0:
            period.append(str('00')+ "-"+str(hour + 1))
        else:
            period.append(str(hour)+ "-"+str(hour + 1))
    
    df['Period']=period
    return df
