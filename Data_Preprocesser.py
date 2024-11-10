import pandas as pd
import re
import streamlit as st

def preprocess(uploaded_file):
    # Read the uploaded file as text data
    raw_data = uploaded_file.read().decode("utf-8")

    # Regex pattern to identify timestamps
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[APM]{2}'
    raw_chat = re.split(pattern, raw_data)[1:]

    # Extracting the Cleaned Chat
    pattern1 = r"(^\s*-+\s*|~\s*|'|\u202f)"
    chat = [re.sub(pattern1, '', message) for message in raw_chat]
    dates = re.findall(pattern, raw_data)

    # Creating DataFrame
    raw_df = pd.DataFrame({'User_Message': chat, 'Message_Date': dates})

    # Format date and remove unwanted characters
    raw_df['Message_Date'] = raw_df['Message_Date'].str.replace(r'(\d)(AM|PM)', r'\1 \2', regex=True).str.replace(
        '\u202f', '')

    # Parse 'Message_Date' with corrected format
    raw_df['Message_Date'] = pd.to_datetime(raw_df['Message_Date'], format='mixed')

    # Separate users and messages
    users = []
    message_chat = []
    for mess in raw_df['User_Message']:
        entry = re.split(r'([\w\W]+?):\s', mess)
        if entry[1:]:  # user name
            users.append(entry[1])
            message_chat.append(entry[2])
        else:
            users.append('Group_notification')
            message_chat.append(entry[0])

    raw_df['Users'] = users
    raw_df['message_chat'] = message_chat
    raw_df.drop(columns=['User_Message'], inplace=True)

    # Extract Date components
    raw_df['Year'] = raw_df['Message_Date'].dt.year
    raw_df['Day'] = raw_df['Message_Date'].dt.day_name()
    raw_df['Date_only'] = raw_df['Message_Date'].dt.date
    raw_df["Month_num"] = raw_df['Message_Date'].dt.month
    raw_df['Month'] = raw_df['Message_Date'].dt.month_name()
    raw_df['Day'] = raw_df['Message_Date'].dt.day
    raw_df['Hour'] = raw_df['Message_Date'].dt.hour
    raw_df['Minute'] = raw_df['Message_Date'].dt.minute

    # Create period based on hour
    period = []
    for hour in raw_df[['Day', 'Hour']]['Hour']:
        if hour == 23:
            period.append(str(hour) + '-' + str('00'))
        elif hour == 0:
            period.append(str('00') + '-' + str(hour + 1))
        else:
            period.append(str(hour) + '-' + str(hour + 1))
    raw_df['period'] = period
    
    return raw_df


# Streamlit UI for file upload
uploaded_file = st.file_uploader("Upload a WhatsApp Chat File", type=["txt"])

if uploaded_file is not None:
    # Process the file and display the dataframe
    df = preprocess(uploaded_file)
    st.write(df)
