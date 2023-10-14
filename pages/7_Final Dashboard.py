import streamlit as st
import pandas as pd
import plotly.express as px

#%% App Details
appDetails = """
Created by: [Bogdan Tudose](https://www.linkedin.com/in/tudosebogdan/) \n
Date: Oct 16, 2023 \n
ChatGPT Convo: https://chat.openai.com/share/3125e5e4-8aa0-4b46-be3b-dbfdd9868afc \n
Description: Final iteration of dashboard with added code for formatting and layout. Also combined the summary stats and breakdown by client into one dashboard with radio buttons.\n
"""
with st.expander("See app info"):
    st.write(appDetails)


# Load your financial dataset
@st.cache_data
def grabData():
  df = pd.read_excel('chatGPTDemo.xlsx', parse_dates=['date'])
  df['dollar_volume'] = df['quantity'] * df['fee/share'] #code carried over from Part 2
  return df

df = grabData()

unique_clients = sorted(df['Client Name'].unique())
selected_clients = st.sidebar.multiselect("Select Client(s)", unique_clients)
num_picked = len(selected_clients)

if selected_clients:
    # Filter the DataFrame based on the selected clients
    filtered_df = df[df['Client Name'].isin(selected_clients)]
else:
    filtered_df = df

layout_pick = st.sidebar.radio("Pick dashobard view:", ['Summary','Key Client Stats'])

if layout_pick=='Summary':
  # Group data by date and calculate total fees for each day
  fees_over_time = filtered_df.groupby('date')['fees'].sum().reset_index()  
  st.header("Total Fees Over Time")
  fig = px.line(fees_over_time, x='date', y='fees', title="Total Fees Over Time")
  st.plotly_chart(fig)
  
  st.header("Top Clients by Total Fees")
  # Group data by 'Client Name' and calculate total fees for each client
  num = min(num_picked, 10)
  top_clients = filtered_df.groupby('Client Name')['fees'].sum().sort_values(ascending=False).head(num)
  fig = px.bar(top_clients, x=top_clients.index, y='fees', title="Top Clients by Total Fees")
  st.plotly_chart(fig)
  
  st.header("Fees by GICS Sector")
  fig = px.pie(filtered_df, names='GICS Sector', values='fees', title="Fees by GICS Sector")
  st.plotly_chart(fig)
  
  st.header("Total Dollar Volume Traded by Ticker")
  fig = px.bar(filtered_df, x='ticker', y='dollar_volume', title="Total Dollar Volume Traded by Ticker",color='GICS Sector')
  st.plotly_chart(fig)
  
  #%%Histogram of Fee per Share: Analyze the distribution of commission fees per share.
  st.header("Histogram of Fee per Share")
  fig = px.histogram(filtered_df, x='fee/share', nbins=3, title="Histogram of Fee per Share")
  st.plotly_chart(fig)
  
elif layout_pick=='Key Client Stats':
  st.write("Code to come")
  