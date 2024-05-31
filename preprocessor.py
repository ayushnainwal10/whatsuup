import pandas as pd
import re

def preprocess(data, time_format):
    # Define patterns for 12-hour and 24-hour formats
    pattern_12hr = r"(\d{2}/\d{2}/\d{2}, \d{1,2}:\d{2}\s?[ap]m) - ([^:]+): (.+)"
    pattern_24hr = r"(\d{2}/\d{2}/\d{2}, \d{2}:\d{2}) - ([^:]+): (.+)"

    # Initialize lists to store extracted information
    dates, users, messages, date_formats = [], [], [], []

    # Choose the correct pattern and date format based on user selection
    if time_format == "12-hour":
        pattern = pattern_12hr
        date_format = '%d/%m/%y, %I:%M %p'
    else:
        pattern = pattern_24hr
        date_format = '%d/%m/%y, %H:%M'

    for entry in data.splitlines():
        match = re.match(pattern, entry)
        if match:
            date, user, message = match.groups()
            dates.append(date)
            users.append(user)
            messages.append(message)
            date_formats.append(date_format)
        else:
            try:
                date_time, remainder = entry.split(' - ', 1)
                dates.append(date_time)
                users.append('group_notification')
                messages.append(remainder)
                date_formats.append(None)  # No specific format for group notifications
            except ValueError as e:
                print(f"Error processing entry: {entry}")
                print(e)

    # Create a DataFrame with the extracted information
    df = pd.DataFrame({'date': dates, 'user': users, 'message': messages, 'date_format': date_formats})

    # Convert 'date' column to datetime type using the appropriate formats
    df['date'] = df.apply(lambda row: pd.to_datetime(row['date'], format=row['date_format'], errors='coerce') if row['date_format'] else pd.NaT, axis=1)

    # Extract additional date and time components
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['num_month'] = df['date'].dt.month
    df['only_date'] = df['date'].dt.date
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(f"{hour}-00")
        elif hour == 0:
            period.append(f"00-{hour+1}")
        else:
            period.append(f"{hour}-{hour+1}")
    df['time_period'] = period

    return df
