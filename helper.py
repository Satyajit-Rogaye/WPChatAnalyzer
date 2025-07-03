from urlextract import URLExtract
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
import seaborn as sns


def fetch_stats(selected_user,df):

    if selected_user =="Overall":
        #fetching 1 no of messages
        num_msg=df.shape[0]
        #fetching 2 no of words 
        words=[]
        media=[]
        links=[]
        extractor=URLExtract()
        for msg in df['User Messages']:
            words.extend(msg.split())
            links.extend(extractor.find_urls(msg))
            if msg =="<Media omitted>\n":
                media.append(msg)
        return num_msg,len(words),len(media),len(links)

    else:
        newDF=df[df['User Name']==selected_user]
        num_msg = newDF.shape[0]
        words=[]
        media=[]
        links=[]
        extractor=URLExtract()
        for msg in newDF['User Messages']:
            words.extend(msg.split())
            links.extend(extractor.find_urls(msg))
            if msg =="<Media omitted>\n":
                media.append(msg)
        return num_msg,len(words),len(media),len(links)
      

def plot_active_user(df):
    x=df['User Name'].value_counts().head()
    newDF=round(df['User Name'].value_counts()/df.shape[0]*100,2).reset_index().rename(columns={'index':'Percent','User Name':'Name'})
    return x,newDF

def develop_wordcluod(selected_user,df):
    if selected_user =="Overall":
        #masking
        temp=df[df['User Name']!='Message notification']
        temp=temp[temp['User Messages']!="<Media omitted>\n"]
        wc=WordCloud(height=300,width=300,max_font_size=40,background_color='white')
        df_wc=wc.generate(temp['User Messages'].str.cat(sep=" "))
        return df_wc
    
    else:
        #masking
        temp=df[df['User Name']!='Message notification']
        temp=temp[temp['User Messages']!="<Media omitted>\n"]
        wc=WordCloud(height=300,width=300,max_font_size=40,background_color='white')
        df_wc=wc.generate(temp['User Messages'].str.cat(sep=" "))
        return df_wc

def most_common_words(selected_user,df):
    if selected_user =="Overall":
        temp=df[df['User Name']!='Message notification']
        temp=temp[temp['User Messages']!="<Media omitted>\n"]
        words=[]
        for msg in temp['User Messages']:
            words.extend(msg.split())
            word_count=Counter(words).most_common(20)
    
        mostcommon=pd.DataFrame(word_count,index=[i for i in range(1,21)])
        mostcommon=mostcommon.rename(columns={0:"Words",1:'Total Words'})
        return mostcommon

    else:
        newDF=df[df['User Name']==selected_user]
        temp=newDF[newDF['User Name']!='Message notification']
        temp=temp[temp['User Messages']!="<Media omitted>\n"]
        words=[]
        for msg in temp['User Messages']:
            words.extend(msg.split())
            word_count=Counter(words).most_common(20)
    
        mostcommon=pd.DataFrame(word_count,index=[i for i in range(1,21)])
        mostcommon=mostcommon.rename(columns={0:"Words",1:'Total Words'})
        return mostcommon
        

def most_common_emoji(selected_user,df):
    if selected_user =='Overall':
        emj = []

        for text in df['User Messages']:
            if isinstance(text, str):  # ensure it's not NaN
                emj.extend([c for c in text if emoji.is_emoji(c)])

        emjpd = pd.DataFrame(Counter(emj).most_common(), columns=['emoji', 'count'])
        return emjpd
    else:
        newDF=df[df['User Name']==selected_user]
        emj = []
        for text in newDF['User Messages']:
            if isinstance(text, str):  # ensure it's not NaN
                emj.extend([c for c in text if emoji.is_emoji(c)])

        emjpd = pd.DataFrame(Counter(emj).most_common(), columns=['emoji', 'count'])
        return emjpd
    
def time_analysis(selected_user,df):
    if selected_user=='Overall':
        time_line=df.groupby(['Year','Month_Num','Month']).count()['User Messages'].reset_index()
        time=[]
        for i in range(time_line.shape[0]):
            time.append(time_line['Month'][i]+ "-"+str(time_line['Year'][i]))
        time_line['Time']=time
        return time_line
    else:
        newDF=df[df['User Name']==selected_user]
        time_line=newDF.groupby(['Year','Month_Num','Month']).count()['User Messages'].reset_index()
        time=[]
        for i in range(time_line.shape[0]):
            time.append(time_line['Month'][i]+ "-"+str(time_line['Year'][i]))
        time_line['Time']=time
        return time_line
    
def daily_analysis(selected_user,df):
    if selected_user=="Overall":
        daily_time=df.groupby('Only_Date').count()['User Messages'].reset_index()
        return daily_time
    else:
        newDF=df[df['User Name']==selected_user]
        daily_time=newDF.groupby('Only_Date').count()['User Messages'].reset_index()
        return daily_time
    
def most_active_day_in_week(selected_user,df):
    if selected_user=="Overall":
        day_name_count=df['Day_Name'].value_counts()
        return day_name_count
    else:
        newDF=df[df['User Name']==selected_user]
        day_name_count=newDF['Day_Name'].value_counts()
        return day_name_count

def most_active_day_in_month(selected_user,df):
    if selected_user=="Overall":
        Month_name_count=df['Month'].value_counts()
        return Month_name_count
    else:
        newDF=df[df['User Name']==selected_user]
        Month_name_count=newDF['Month'].value_counts()
        return Month_name_count

def develop_heatmap(selected_user,df):
    if selected_user == 'Overall':
        plt.figure(figsize=(20,10))
        heatmap=df.pivot_table(index='Day_Name',columns='Period',values='User Messages',aggfunc='count').fillna(0)
        return heatmap
    else:
        newDF=df[df['User Name']==selected_user]
        plt.figure(figsize=(20,10))
        heatmap=newDF.pivot_table(index='Day_Name',columns='Period',values='User Messages',aggfunc='count').fillna(0)
        return heatmap
