import streamlit as st
import pandas as pd
import plotly.express as px

# Load your financial dataset
df = pd.read_excel('chatGPTDemo.xlsx')
# Assuming your dataset is loaded into a pandas DataFrame named 'df'

# Convert the 'date' column to a datetime format
df['date'] = pd.to_datetime(df['date'])

#%% App Details
appDetails = """
Created by: [Bogdan Tudose](https://www.linkedin.com/in/tudosebogdan/) \n
Date: Oct 16, 2023 \n
ChatGPT Convo: https://chat.openai.com/share/9a47b226-92d2-49b9-a1cf-cdf731a0d430 \n
Description: Second iteration of dashboard using Plotly charts. \n
Prompt: Instead of using altair can you redo those graphs with the plotly library?
"""
with st.expander("See app info"):
    st.write(appDetails)

#%% 1. ChatGPT Code - Total Fees Over Time: Visualize the total fees generated over the quarter to track the revenue trend.
# Group data by date and calculate total fees for each day
fees_over_time = df.groupby('date')['fees'].sum().reset_index()

st.header("Total Fees Over Time")
fig = px.line(fees_over_time, x='date', y='fees', title="Total Fees Over Time")
st.plotly_chart(fig)


#%% 2. ChatGPT Code - Top Clients by Total Fees: Identify your most profitable clients.
# Group data by 'Client Name' and calculate total fees for each client
top_clients = df.groupby('Client Name')['fees'].sum().sort_values(ascending=False).head(10)

st.header("Top Clients by Total Fees")
fig = px.bar(top_clients, x=top_clients.index, y='fees', title="Top Clients by Total Fees")
st.plotly_chart(fig)

#%% 3. ChatGPT Code - Fees by Sector: Understand which sectors generate the most fees.
# Group data by 'GICS Sector' and calculate total fees for each sector
fees_by_sector = df.groupby('GICS Sector')['fees'].sum().reset_index()

st.header("Fees by GICS Sector")
fig = px.pie(fees_by_sector, names='GICS Sector', values='fees', title="Fees by GICS Sector")
st.plotly_chart(fig)

#%% 4. ChatGPT Code - Total Dollar Volume Traded by Ticker: Visualize the total dollar volume traded for each ticker symbol.
# Calculate total dollar volume for each ticker
#df['dollar_volume'] = df['quantity'] * df['fee/share'] #incorrect from chatgpt, this is the same as fees
df['dollar_volume'] = df['quantity'] * df['Adj Close']

total_volume_by_ticker = df.groupby('ticker')['dollar_volume'].sum().sort_values(ascending=False).reset_index()

st.header("Total Dollar Volume Traded by Ticker")
fig = px.bar(total_volume_by_ticker, x='ticker', y='dollar_volume', title="Total Dollar Volume Traded by Ticker")
st.plotly_chart(fig)

#%% 5. ChtGPT Code - Histogram of Fee per Share: Analyze the distribution of commission fees per share.
st.header("Histogram of Fee per Share")
fig = px.histogram(df, x='fee/share', nbins=20, title="Histogram of Fee per Share")
st.plotly_chart(fig)
