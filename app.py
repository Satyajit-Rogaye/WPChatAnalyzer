import streamlit as st
import preprocessing ,helper
from urlextract import URLExtract
import matplotlib.pyplot as plt
import seaborn as sns
st.sidebar.title('Whatsapp Chat Analyzer') 
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    #convrting data into string
    data=bytes_data.decode("utf-8")
    #displaying the dataframe
    df=preprocessing.preprocessor(data)
    #fetching unique user
    userlist=df['User Name'].unique().tolist()
    userlist.remove('Message notification')
    userlist.sort()
    userlist.insert(0,"Overall")
    selected_user=st.sidebar.selectbox("Show analysis wrt ",userlist)
    

    if st.sidebar.button("Show Analysis"):

        #1 find stats
        st.title("Total Statistics")
        col1,col2,col3,col4=st.columns(4)
        no_msgs,words,media,links=helper.fetch_stats(selected_user,df)
        with col1:
            st.header("Total Messages")
            st.title(no_msgs)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Shared Media")
            st.title(media)
        with col4:
            st.header("Shared Links")
            st.title(links)

        #finfing the most active user in group level
        if selected_user =="Overall":
            st.title("Most Active User")

            x,newDF=helper.plot_active_user(df)
            fig,ax=plt.subplots()
            col1,col2=st.columns(2)

            with col1:
                ax.bar(x.index,x.values,color='red',label='Most Active User')
                plt.legend()
                plt.grid()
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(newDF)
            
        #Wordcloud
        st.title("WordCloud")
        df_wc=helper.develop_wordcluod(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)#showing image
        st.pyplot(fig)
        
        #Most common words
        st.title("20 Most Common Words")
        mostcommon=helper.most_common_words(selected_user,df)
        fig,ax=plt.subplots()
        col1,col2=st.columns(2)
        with col1:
            st.dataframe(mostcommon)
        with col2:
            ax.bar(mostcommon['Words'],mostcommon['Total Words'],label='Most Common Words')
            plt.legend()
            plt.grid()
            plt.xlabel("Words")
            plt.ylabel("Counts")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        
        commonemoji=helper.most_common_emoji(selected_user,df)
        st.title('Most Common Emoji')
        fig,ax=plt.subplots()
        col1,col2=st.columns(2)
        with col1:
            st.dataframe(commonemoji)
        with col2:
            ax.pie(commonemoji['count'].head(10),colors = ['skyblue','salmon','gold','mediumseagreen','plum','orange','deepskyblue','lightcoral','khaki','orchid'],autopct="%1.1f%%",labels=commonemoji['emoji'].head(10))
            st.pyplot(fig)
        
        timeanalysis=helper.time_analysis(selected_user,df)
        st.title('Monthly Time Analysis As Per Chats')
        fig,ax=plt.subplots()
        ax.plot(timeanalysis['Time'],timeanalysis['User Messages'],label='Total Chats/Month',marker='o',color='green')
        plt.xticks(rotation='vertical')
        plt.grid()
        plt.xlabel('Month-Year')
        plt.ylabel('Total Messages')
        plt.legend()
        st.pyplot(fig)

        dailyanalysis=helper.daily_analysis(selected_user,df)
        st.title('Daily Time Analysis As Per Chats')
        fig,ax=plt.subplots()
        ax.plot(dailyanalysis['Only_Date'],dailyanalysis['User Messages'],label='Total Chats/Day',color='black')
        plt.xticks(rotation='vertical')
        plt.grid()
        plt.xlabel('Year')
        plt.ylabel('Total Messages')
        plt.legend()
        st.pyplot(fig)
        
        col1,col2=st.columns(2)
        with col1:
            fig,ax=plt.subplots()
            most_busy_day=helper.most_active_day_in_week(selected_user,df)
            st.title('Most Active Day')
            ax.bar(most_busy_day.index,most_busy_day.values,color='magenta',label='Most Active Day')
            plt.grid()
            plt.xlabel("Day")
            plt.ylabel("Total Messgaes")
            plt.xticks(rotation='vertical')
            plt.legend()
            st.pyplot(fig)
        
        with col2:
            fig,ax=plt.subplots()
            most_busy_month=helper.most_active_day_in_month(selected_user,df)
            st.title('Most Active Month')
            ax.bar(most_busy_month.index,most_busy_month.values,color='magenta',label='Most Active Month')
            plt.xticks(rotation='vertical')
            plt.xlabel("Month")
            plt.ylabel("Total Messgaes")
            plt.grid()
            plt.legend()
            st.pyplot(fig)
        

        heatmap=helper.develop_heatmap(selected_user,df)
        plt.figure(figsize=(20,10))
        st.title("Weekly Activity Map")
        fig,ax=plt.subplots()
        ax=sns.heatmap(heatmap)
        st.pyplot(fig) 

        st.markdown("""
<div style='text-align: center; font-size: 20px; color: teal;'>
    <b>Chat Analyzer</b><br>
    <i>Designed & Created by</i><br>
    <span style='font-size:24px; color:orange;'>Satyajit Rogaye</span>
</div>
""", unsafe_allow_html=True)
