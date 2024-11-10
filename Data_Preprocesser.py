#%%
import pandas as pd
import re
# Data
def preprocess(text_data):

    f = open('D:\\VSCODE\\DA_PROJECT\\WhatsApp Chat with MLDA II.txt', 'r', encoding='utf-8')
    raw_data = f.read()
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[APM]{2}'
    raw_chat = re.split(pattern, raw_data)[1:]
    # Extracting the Cleaned Chat
    pattern1 = r"(^\s*-+\s*|~\s*|'|\u202f)"
    chat = [re.sub(pattern1, '', message) for message in raw_chat]
    dates = re.findall(pattern, raw_data)
    # Creating A DataFrame
    raw_df = pd.DataFrame({'User_Message': chat, 'Message_Date': dates})
    # Insert a space before 'AM' or 'PM' and remove the narrow no-break space (\u202f)
    raw_df['Message_Date'] = raw_df['Message_Date'].str.replace(r'(\d)(AM|PM)', r'\1 \2', regex=True).str.replace(
        '\u202f', '')

    # Parse 'Message_Date' with the corrected format
    raw_df['Message_Date'] = pd.to_datetime(raw_df['Message_Date'], format='mixed')
    # Seprate users and messages
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

    # Creating Columns [Year, Month, Day, Hour, Minute]
    raw_df['Year'] = raw_df['Message_Date'].dt.year
    raw_df['Day'] = raw_df['Message_Date'].dt.day_name()
    raw_df['Date_only'] = raw_df['Message_Date'].dt.date
    raw_df["Month_num"] = raw_df['Message_Date'].dt.month
    raw_df['Month'] = raw_df['Message_Date'].dt.month_name()
    raw_df['Day'] = raw_df['Message_Date'].dt.day
    raw_df['Hour'] = raw_df['Message_Date'].dt.hour
    raw_df['Minute'] = raw_df['Message_Date'].dt.minute

    period = []
    for hour in raw_df[['Day', 'Hour', ]]['Hour']:
        if hour == 23:
            period.append(str(hour) + '-' + str('00'))
        elif hour == 0:
            period.append(str('00') + '-' + str(hour + 1))
        else:
            period.append(str(hour) + '-' + str(hour + 1))
    raw_df['period'] = period
    return raw_df
#%%

































































