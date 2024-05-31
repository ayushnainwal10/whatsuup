import pandas as pd
from collections import Counter
from urlextract import URLExtract
from wordcloud import WordCloud
import emoji
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

extractor = URLExtract()
def fetch_stats(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    # Fetch number of messages
    num_messages = df.shape[0]

    # Fetch number of words
    words = []
    for message in df["message"]:
        words.extend(message.split())

    # Fetch number of media messages
    num_media_messages = df[df["message"] == "<Media omitted>\n"].shape[0]

    # Fetch number of links
    links = []
    for message in df["message"]:
        links.extend(extractor.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)


def most_busy_users(df):
    x = df["user"].value_counts()
    df = (
        round(df["user"].value_counts() / df.shape[0] * 100, 2)
        .reset_index()
        .rename(columns={"index": "name", "user": "percentage"})
    )
    return x, df


def create_wordcloud(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    with open("stop_hinglish.txt", "r") as f:
        stop_words = f.read()
    # Remove group notifications
    temp = df[df["user"] != "group_notification"]
    # Remove media omitted
    temp = temp[temp["message"] != "<Media omitted>\n"]

    # Remove stop words
    def remove_stop_words(message):
        Y = []
        for word in message.lower().split():
            if word not in stop_words:
                Y.append(word)
        return " ".join(Y)

    wc = WordCloud(width=400, height=400, min_font_size=10, background_color="#fff")
    temp["message"] = temp["message"].apply(remove_stop_words)
    df_wc = wc.generate(temp["message"].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    with open("stop_hinglish.txt", "r") as f:
        stop_words = f.read()
    words = []
    for message in df["message"]:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    return_df = pd.DataFrame(Counter(words).most_common(20))
    return return_df


def emoji_helper(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    emojis = []
    for message in df["message"]:
        for c in message:
            if c in emoji.EMOJI_DATA:
                emojis.extend(c)

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df


def monthly_time_line(selected_user, df, time_format):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    timeline = (
        df.groupby(["year", "num_month", "month"]).count()["message"].reset_index()
    )
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline["month"][i] + "-" + str(timeline["year"][i]))

    timeline["time"] = time

    if time_format == "12-hour":
        df["time"] = df["date"].dt.strftime("%I:%M %p")
    else:
        df["time"] = df["date"].dt.strftime("%H:%M")

    return timeline


def daily_time_line(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    daily_timeline = df.groupby("only_date").count()["message"].reset_index()
    return daily_timeline


def weekly_activity_map(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    return df["day_name"].value_counts()


def monthly_activity_map(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    return df["month"].value_counts()


def activity_heat_map(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    activity_heatmap = df.pivot_table(
        index="day_name", columns="time_period", values="message", aggfunc="count"
    ).fillna(0)
    return activity_heatmap


def sentiment_analysis(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    analyzer = SentimentIntensityAnalyzer()
    sentiments = []
    for message in df["message"]:
        sentiment_score = analyzer.polarity_scores(message)
        sentiment = "Neutral"
        if sentiment_score["compound"] > 0.05:
            sentiment = "Positive"
        elif sentiment_score["compound"] < -0.05:
            sentiment = "Negative"
        sentiments.append(sentiment)

    df["sentiment"] = sentiments
    sentiment_counts = df["sentiment"].value_counts()

    return sentiment_counts
