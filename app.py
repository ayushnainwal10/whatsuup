import streamlit as st
import matplotlib.pyplot as plt
import preprocessor , helper
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    # st.text(data)

    df = preprocessor.preprocess(data)
    # st.dataframe(df)  # function to dispaly dataframe in streamlit

    #fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'Overall')

    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)


    # Stats Area
    if st.sidebar.button("Show Analysis"):
        num_messages,words,num_media_messages,num_links = helper.fetch_stats(selected_user,df)

        st.title("Top Statistics")
        col1,col2,col3,col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)
    
        # fetching busiest users in the group
        if selected_user == 'Overall':
            st.title("Most Busy Users")
            x,new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1,col2 = st.columns(2)

            with col1:
                ax.bar(x.index,x.values,color='#ffa94d')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # monthly timeline
        st.title("Monthly Timeline")
        monthly_timeline = helper.monthly_time_line(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(monthly_timeline['time'],monthly_timeline['message'],color='#51cf66')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_time_line(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'],daily_timeline['message'],color='#5c7cfa')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        st.title("Weekly Acticity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = helper.weekly_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='#ff6b6b')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header("Most Busy Month")
            busy_month = helper.monthly_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_month.index,busy_month.values , color='#ff6b6b')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            
        # activity heatmap
        st.title("Weekly Activity Heatmap")
        activity_map = helper.activity_heat_map(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(activity_map)
        st.pyplot(fig)

        # wordcloud
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig, ax = plt.subplots()
        plt.axis('off')
        ax.imshow(df_wc)
        st.pyplot(fig)
                
        # Most Common words
        st.title("Most Common Words")

        most_common_df = helper.most_common_words(selected_user,df)

        fig,ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1],color='#66d9e8')
        st.pyplot(fig)


        # Emoji analysis
        emoji_df = helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")

        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(), autopct='%0.2f')
            st.pyplot(fig)
        

st.sidebar.text("Copyright \u00A9 2024 Vishal Verma")