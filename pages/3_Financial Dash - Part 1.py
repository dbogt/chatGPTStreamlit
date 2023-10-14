import streamlit as st
import pandas as pd
import altair as alt

# Load your financial dataset
df = pd.read_excel('chatGPTDemo.xlsx')
# Assuming your dataset is loaded into a pandas DataFrame named 'df'

# Convert the 'date' column to a datetime format
df['date'] = pd.to_datetime(df['date'])

#%% App Details
appDetails = """
Created by: [Bogdan Tudose](https://www.linkedin.com/in/tudosebogdan/) \n
Date: Oct 16, 2023 \n
ChatGPT Convo: https://chat.openai.com/share/3125e5e4-8aa0-4b46-be3b-dbfdd9868afc
Description: First iteration of dashboard using Altair charts.
"""
with st.expander("See app info"):
    st.write(appDetails)

#%% 1. ChatGPT Code - Total Fees Over Time: Visualize the total fees generated over the quarter to track the revenue trend.
# Group data by date and calculate total fees for each day
fees_over_time = df.groupby('date')['fees'].sum()

st.header("Total Fees Over Time")
st.line_chart(fees_over_time)


#%% 2. ChatGPT Code - Top Clients by Total Fees: Identify your most profitable clients.
# Group data by 'Client Name' and calculate total fees for each client
top_clients = df.groupby('Client Name')['fees'].sum().sort_values(ascending=False).head(10)

st.header("Top Clients by Total Fees")
st.bar_chart(top_clients)

#%% 3. ChatGPT Code - Fees by Sector: Understand which sectors generate the most fees.
# Group data by 'GICS Sector' and calculate total fees for each sector
fees_by_sector = df.groupby('GICS Sector')['fees'].sum()

st.header("Fees by GICS Sector")
st.pie_chart(fees_by_sector)

#%% 4. ChatGPT Code - Total Dollar Volume Traded by Ticker: Visualize the total dollar volume traded for each ticker symbol.
# Calculate total dollar volume for each ticker
df['dollar_volume'] = df['quantity'] * df['fee/share']
total_volume_by_ticker = df.groupby('ticker')['dollar_volume'].sum().sort_values(ascending=False)

st.header("Total Dollar Volume Traded by Ticker")
st.bar_chart(total_volume_by_ticker)

#%% 5. ChtGPT Code - Histogram of Fee per Share: Analyze the distribution of commission fees per share.
st.header("Histogram of Fee per Share")
st.histogram(df['fee/share'], bins=20)
