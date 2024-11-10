#%%
from urlextract import URLExtract
extract = URLExtract()
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji
import re
import plotly.express as px

# Fetch Stats

def  fetch_stats(selected_user,df):
    # 1. Fetch Number of Messages :
    if selected_user != 'Overall':
        df = df[df['Users'] == selected_user]
    num_messages = df.shape[0]
        # 2. number of words
    words = []
    for m in df['message_chat']:
        words.extend(m.split())
    W = len(words)


    # Fetch number of media messages
    number_of_media_messages = df[df['message_chat'] == '<Media omitted>\n'].shape[0]
    # Fetch number of Links
    urls_list = []
    for m in df['message_chat']:
        urls_list.extend(extract.find_urls(m))
    ul = len(urls_list)

    return num_messages, W, number_of_media_messages, ul


#%%
def most_bust_users(df):
    x = df['Users'].value_counts().head(10)
    # Users message count and percentage :
    users_message_percentage = round((df['Users'].value_counts() / df.shape[0]) * 100,
                                     2).reset_index().rename(
        columns={'Users': 'Users', 'count': 'Percentage'}).set_index('Users')

    return x, users_message_percentage
#%%
def create_word_cloud(selected_user, df):
    # Load stop words
    with open('stop_hinglish.txt', 'r') as f:
        stopword = f.read().splitlines()

    # Filter messages for the selected user if not 'Overall'
    if selected_user != 'Overall':
        df = df[df['Users'] == selected_user]

    # Remove group notifications and media messages
    temp = df[(df['Users'] != 'Group_notification') & (df['message_chat'] != '<Media omitted>\n')]

    # Function to remove stop words
    def remove_stop_words(message):
        return " ".join([word for word in message.lower().split() if word not in stopword])

    # Apply stop word removal to the 'message_chat' column
    temp['message_chat'] = temp['message_chat'].apply(remove_stop_words)

    # Concatenate messages to a single string for word cloud generation
    text = temp['message_chat'].str.cat(sep=" ")

    # Check if the text is empty
    if not text.strip():
        raise ValueError("No messages available to generate a word cloud.")

    # Generate the word cloud
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(text)

    return df_wc
#%%
# Function most_common_words
def most_common_words(selected_user,df):
    f = open('D:\\VSCODE\\DA_PROJECT\\stop_hinglish.txt','r')
    stopword = f.read()
    if selected_user != 'Overall':
        df = df[df['Users']== selected_user]

    temp = df[df['Users'] != 'Group_notification']
    temp = temp[temp['message_chat'] != '<Media omitted>\n']
    words = []
    for m in temp['message_chat']:
        for i in m.lower().split():
            if i not in stopword:
                words.append(i)

    most_common_df =  pd.DataFrame(Counter(words).most_common(25)).rename(columns={0: 'Typed', 1: 'Counts'})
    return most_common_df
#%%
# most_common_emojis
# Define the emoji pattern
emoji_pattern = re.compile(
    "["  
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F1E0-\U0001F1FF"  # flags
    "\U00002702-\U000027B0"  # additional symbols
    "\U000024C2-\U0001F251"
    "\U0001F900-\U0001F9FF"  # supplemental symbols & pictographs
    "\U0001FA70-\U0001FAFF"  # extended symbols
    "]+",
    flags=re.UNICODE,
)

def most_common_emojis(selected_user, df):
    # Filter messages for the selected user if not 'Overall'
    if selected_user != 'Overall':
        df = df[df['Users'] == selected_user]

    # Extract emojis
    emojis = []
    for m in df['message_chat']:
        emojis.extend(emoji_pattern.findall(m))

    # Count emojis and create a DataFrame
    emojis_df = pd.DataFrame(Counter(emojis).most_common(), columns=["Emoji", "Count"])
    return emojis_df

#%%
def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['Users'] == selected_user]

    # Group by Year, Month and count the messages in 'message_chat'
    timeline = df.groupby(['Year', 'Month_num', 'Month']).count()['message_chat'].reset_index()

    # Add a new column for Time in 'Month-Year' format
    timeline['Time'] = timeline['Month'] + "-" + timeline['Year'].astype(str)

    # Rename 'message_chat' count to 'MessageCount' for clarity
    timeline = timeline.rename(columns={'message_chat': 'MessageCount'})

    return timeline
#%%
def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['Users'] == selected_user]
    daily_timeline = df.groupby(['Date_only'])['message_chat'].count().reset_index()
    return daily_timeline
#%%
def weekly_active(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['Users'] == selected_user]
    df['Day'] = df['Message_Date'].dt.day_name()
    x = df['Day'].value_counts()
    return x
#%%
def monthly_active(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['Users'] == selected_user]
    return df['Month'].value_counts()
#%%
def Activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['Users'] == selected_user]
    pivot_heatmap = df.pivot_table(
        index='Day',  # Rows will be the 'Day'
        columns='period',  # Columns will be the 'period'
        values='message_chat',  # Count of messages in 'message_chat'
        aggfunc='count',  # Aggregate using count
        fill_value=0  # Fill missing values with 0
    )
    return pivot_heatmap



