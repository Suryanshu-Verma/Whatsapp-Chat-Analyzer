#%%
import streamlit as st
from IPython.core.pylabtools import figsize
from matplotlib.pyplot import tight_layout
from networkx.algorithms.bipartite.basic import color
from sympy import rotations
import plotly.express as px
import Functions
import Data_Preprocesser
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import plotly as pl


#%%

st.sidebar.title("Whatsapp Chat Analyzer")
upload_file = st.sidebar.file_uploader("Choose A File")
if upload_file is not None:
    bytes_data = upload_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = Data_Preprocesser.preprocess(data)
    # st.dataframe(df)
    # Fetch unique users
    user_list = df['Users'].unique().tolist()
    user_list.remove('Group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox("Show Analysis",user_list)
    if st.sidebar.button("Show Analysis"):
        # Stats Area :
        num_messages, W, number_of_Media_messages, ul = Functions.fetch_stats(selected_user,df)
        # Create 4 columns using the updated method
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(F"{num_messages}")
        with col2:
            st.header("Total Words")
            st.title(F"{W}")
        with col3:
            st.header("Media Shared")
            st.title(F"{number_of_Media_messages}")
        with col4:
            st.header("Links Shared")
            st.title(F"{ul}")

        ## Monthly Timeline Plot
        st.title("Monthly Timeline")
        timeline = Functions.monthly_timeline(selected_user, df)

        # Create the Plotly line plot
        fig_m = px.line(timeline, x='Time', y='MessageCount',
                        labels={'Time': 'Month', 'MessageCount': 'Number of Messages'})

        # Update the line color to red
        fig_m.update_traces(line=dict(color='red'))

        # Rotate x-axis labels for better readability
        fig_m.update_layout(xaxis_tickangle=-90)

        # Display the Plotly chart with a unique key to avoid duplicate element IDs
        st.plotly_chart(fig_m, key="monthly_timeline_chart")

        ## Daily Timeline
        st.title("Daily Timeline")
        daily_time = Functions.daily_timeline(selected_user, df)
        # Create the Plotly plot
        fig_dt = px.line(daily_time, x='Date_only', y='message_chat',
                      # title='Daily Timeline',
                      labels={'Date_only': 'Date', 'message_chat': 'Number of Messages'})

        # Update line color to red
        fig_dt.update_traces(line=dict(color='red'))
        # Rotate x-axis labels
        fig_dt.update_layout(xaxis_tickangle=-90)

        # Show the plot
        st.plotly_chart(fig_dt)

        ## Activity Map
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Active Day")
            busy_day = Functions.weekly_active(selected_user, df)

            # Create a Plotly bar plot for the most active day
            fig_day = px.bar(busy_day,
                             x=busy_day.index,
                             y=busy_day.values,
                             # title="Most Active Day",
                             labels={'x': 'Day', 'y': 'Activity Count'})

            # Customize layout for better readability
            fig_day.update_layout(xaxis_tickangle=-90)
            st.plotly_chart(fig_day)

        with col2:
            st.header("Most Active Month")
            busy_month = Functions.monthly_active(selected_user, df)

            # Create a Plotly bar plot for the most active month
            fig_month = px.bar(busy_month,
                               x=busy_month.index,
                               y=busy_month.values,
                               # title="Most Active Month",
                               labels={'x': 'Month', 'y': 'Activity Count'})

            # Customize layout for better readability
            fig_month.update_layout(xaxis_tickangle=-90)
            st.plotly_chart(fig_month)


        ## Activity Heatmap
        user_heatmap = Functions.Activity_heatmap(selected_user, df)

        # Create a plot for the heatmap
        plt.figure(figsize=(10, 8))  # Adjust the size as needed
        sns.heatmap(user_heatmap, cmap='RdBu', annot=True, fmt="d", linewidths=0.5)

        # Display the heatmap in Streamlit
        st.pyplot(plt)


        ## Most Active Users
        if selected_user == "Overall":
            st.title("Most Active Users")

            # Get the data for active users and the dataframe
            x, ump = Functions.most_bust_users(df)

            # Create the Plotly bar chart for most active users
            figMAU = px.bar(
                x=x.index,
                y=x.values,
                labels={'x': 'User', 'y': 'Message Count'},
                color=x.values,
                color_continuous_scale='Viridis',
                title='Most Active Users in the Group Chat'
            )

            # Update layout for better readability
            figMAU.update_layout(
                xaxis_title='User',
                yaxis_title='Message Count',
                xaxis_tickangle=-45,  # Rotate x-axis labels for better visibility
                template='plotly_white'
            )

            # Show the interactive Plotly chart
            st.plotly_chart(figMAU, use_container_width=True)

            # Display the dataframe of the active users in the other column
            col1, col2 = st.columns(2)
            with col2:
                st.dataframe(ump)

        ## WordCloud
        st.title("WordCloud")

        # Create WordCloud
        df_wc = Functions.create_word_cloud(selected_user, df)

        # Convert the WordCloud image to an array for display
        wordcloud_image = np.array(df_wc)

        # Use Plotly to display the WordCloud image
        fig_wc = px.imshow(wordcloud_image, title="Word Cloud",
                        labels={'x': '', 'y': ''},
                        color_continuous_scale="Blues",
                        width=800, height=800)

        # Remove axis labels
        fig_wc.update_xaxes(showticklabels=False).update_yaxes(showticklabels=False)

        # Display the Plotly chart
        st.plotly_chart(fig_wc, use_container_width=True)

        ## Most Common Words
        st.title("Most Common Words")
        most_common_df = Functions.most_common_words(selected_user, df)

        # Create the Plotly bar chart
        figMC = px.bar(most_common_df,
                     x='Counts',
                     y='Typed',
                     orientation='h',
                     color='Counts',
                     color_continuous_scale='Viridis',
                     labels={'Typed': 'Word/Character', 'Counts': 'Frequency'},
                     title='Most Common Typed Words/Characters')

        # Update layout for better readability
        figMC.update_layout(
            xaxis_title='Frequency',
            yaxis_title='Words/Characters',
            template='plotly_white',
            yaxis={'categoryorder': 'total ascending'}  # Optional: Sort bars in ascending order by frequency
        )

        # Show the Plotly chart
        st.plotly_chart(figMC, use_container_width=True)

        # Show the dataframe below the plot
        st.dataframe(most_common_df)

        ## Emoji analysis
        emoji_df = Functions.most_common_emojis(selected_user, df)
        st.title("Emojis Analysis")
        st.dataframe(emoji_df)

        col1, col2 = st.columns(2)

        with col1:
            # Plot using Plotly
            fig = px.bar(emoji_df.head(10), x="Emoji", y="Count",
                         title="Top 10 Most Common Emojis",
                         labels={"Emoji": "Emoji", "Count": "Frequency"},
                         color="Count",
                         color_continuous_scale="Viridis")

            fig.update_layout(xaxis_title="Emojis", yaxis_title="Frequency", template="plotly_white")

            # Use st.plotly_chart to display the Plotly chart
            st.plotly_chart(fig)
        with col2: pass




