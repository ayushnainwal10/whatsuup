import streamlit as st
import matplotlib.pyplot as plt
import preprocessor
import helper
import seaborn as sns

# Set page title and favicon
st.set_page_config(page_title="WhatsApp Chat Analyzer", page_icon=":iphone:")

# Define color scheme
primary_color = "#3498db"
secondary_color = "#2ecc71"
background_color = "#f9f9f9"
text_color = "#333333"

# Set overall page style with a background image
st.markdown(
    f"""
    <style>
        body {{
            background-image: url('https://source.unsplash.com/random');
            background-size: cover;
        }}
        .reportview-container .main .block-container{{
            max-width: 1200px;
            padding-top: 2rem;
            padding-right: 2rem;
            padding-left: 2rem;
            padding-bottom: 3rem;
            border-radius: 15px;
            box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.1);
            background-color: rgba(255, 255, 255, 0.9);
        }}
        .reportview-container .main {{
            color: {text_color};
        }}
        .stButton>button {{
            border-radius: 10px;
            box-shadow: 0px 5px 10px rgba(0, 0, 0, 0.1);
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar with a sleek design
st.sidebar.title("📱 WhatsApp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")

time_format = st.sidebar.radio("Select Time Format", ("12-hour", "24-hour"))

# Button to show instructions with a subtle animation
show_instructions = st.sidebar.button("ℹ️ Instructions")

# Session state to keep track of instructions visibility
if "show_instructions" not in st.session_state:
    st.session_state.show_instructions = False

if show_instructions:
    st.session_state.show_instructions = not st.session_state.show_instructions

if st.session_state.show_instructions:
    st.markdown(
        """
        **Instructions to Extract WhatsApp Chat without Media:**

        1. Open WhatsApp.
        2. Open the chat you want to analyze.
        3. Tap on the three dots in the top-right corner.
        4. Select 'More' > 'Export chat'.
        5. Choose 'Without Media'.
        6. Upload the exported text file using the file uploader on the left sidebar.
        7. Select the desired time format.
        8. Click on 'Show Analysis' to generate insights.
        """
    )

if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')

    df = preprocessor.preprocess(data, time_format)

    # Fetch unique users with a cool dropdown animation
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, 'Overall')

    selected_user = st.sidebar.selectbox("👤 Show analysis wrt", user_list)

    # Stats Area with a modern card design
    if st.sidebar.button("📊 Show Analysis"):
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)


        st.title("📈 Top Statistics")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Messages", num_messages, delta=num_messages - df.shape[0])
        with col2:
            st.metric("Total Words", words, delta=words - len(" ".join(df['message'])))
        with col3:
            st.metric("Media Shared", num_media_messages, delta=num_media_messages - df[df['message'] == '<Media omitted>\n'].shape[0])
        with col4:
            st.metric("Links Shared", num_links, delta=num_links - len(df[df['message'].str.contains("http[s]?://")]))


        # Fetching busiest users in the group with a sleek bar chart
        if selected_user == 'Overall':
            st.title('👥 Most Active Users')
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots(figsize=(10, 6))

            ax.bar(x.index, x.values, color=primary_color)
            plt.xticks(rotation='vertical')
            plt.xlabel("User")
            plt.ylabel("Number of Messages")
            plt.title("Most Active Users")
            plt.tight_layout()

            st.pyplot(fig)
            st.dataframe(new_df, height=400)

        # WordCloud with a fancy background
        st.title("💬 Wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        ax.axis('off')  # Hide axis
        st.pyplot(fig)

        # Most common words with an elegant bar chart
        most_common_df = helper.most_common_words(selected_user, df)
        st.title('🔤 Most Common Words')
        st.bar_chart(most_common_df.set_index(0), height=400)

        # Emoji Analysis with a vibrant data table
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("😄 Emoji Analysis")
        st.dataframe(emoji_df.head(10), height=400)

        # Monthly timeline with a dynamic line plot
        st.title("🗓️ Monthly Timeline")
        timeline = helper.monthly_time_line(selected_user, df, time_format)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(timeline['time'], timeline['message'], color=secondary_color, marker='o')
        plt.xticks(rotation='vertical')
        plt.xlabel("Month")
        plt.ylabel("Number of Messages")
        plt.title("Monthly Timeline")
        plt.tight_layout()
        st.pyplot(fig)

        # Daily timeline with an animated line plot
        st.title("📅 Daily Timeline")
        daily_timeline = helper.daily_time_line(selected_user, df)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color=secondary_color, marker='o')
        plt.xticks(rotation='vertical')
        plt.xlabel("Date")
        plt.ylabel("Number of Messages")
        plt.title("Daily Timeline")
        plt.tight_layout()
        st.pyplot(fig)

        # Activity map with a vibrant color scheme
        st.title('⏱️ Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header("📅 Most Active Days")
            busy_day = helper.weekly_activity_map(selected_user, df)
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.bar(busy_day.index, busy_day.values, color=primary_color)
            plt.xticks(rotation='vertical')
            plt.xlabel("Day of Week")
            plt.ylabel("Number of Messages")
            plt.title("Most Active Days")
            plt.tight_layout()
            st.pyplot(fig)

        with col2:
            st.header("📆 Most Active Months")
            busy_month = helper.monthly_activity_map(selected_user, df)
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.bar(busy_month.index, busy_month.values, color=primary_color)
            plt.xticks(rotation='vertical')
            plt.xlabel("Month")
            plt.ylabel("Number of Messages")
            plt.title("Most Active Months")
            plt.tight_layout()
            st.pyplot(fig)

        # Sentiment Analysis with a delightful breakdown
        st.title("😊 Sentiment Analysis")
        sentiment_counts = helper.sentiment_analysis(selected_user, df)

        # Display sentiment avatars with a cheerful tone
        st.subheader("Sentiment Breakdown:")
        st.write(f"😃 Positive: {sentiment_counts['Positive'] / len(df) * 100:.2f}%")
        st.write(f"😐 Neutral: {sentiment_counts['Neutral'] / len(df) * 100:.2f}%")
        st.write(f"😠 Negative: {sentiment_counts['Negative'] / len(df) * 100:.2f}%")

