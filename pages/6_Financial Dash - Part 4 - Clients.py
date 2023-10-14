import streamlit as st
import pandas as pd
import plotly.express as px

#%% App Details
appDetails = """
Created by: [Bogdan Tudose](https://www.linkedin.com/in/tudosebogdan/) \n
Date: Oct 16, 2023 \n
ChatGPT Convo: https://chat.openai.com/share/3125e5e4-8aa0-4b46-be3b-dbfdd9868afc \n
Description: Fourth iteration of dashboard with drilldown on clients and better formatting.
"""
with st.expander("See app info"):
    st.write(appDetails)

#%%ChatGPT Code

# Load your financial dataset
df = pd.read_excel('chatGPTDemo.xlsx')
# Assuming your dataset is loaded into a pandas DataFrame named 'df'
df['dollar_volume'] = df['quantity'] * df['fee/share'] #code carried over from Part 2
st.title("Financial Data Dashboard")

# Create a multi-select dropdown to select one or more clients
unique_clients = sorted(df['Client Name'].unique())
selected_clients = st.multiselect("Select Client(s)", unique_clients)

if selected_clients:
    # Filter the DataFrame based on the selected clients
    filtered_df = df[df['Client Name'].isin(selected_clients)]

    # Total volume traded and total commissions
    total_volume = filtered_df['quantity'].sum()
    total_commissions = filtered_df['fees'].sum()

    st.subheader("Key Stats for Selected Client(s)")
    st.write(f"Total Volume Traded: ${total_volume:,.2f}")
    st.write(f"Total Commissions: ${total_commissions:,.2f}")

    # Top 5 tickers traded (by dollar volume and fees)
    top_tickers_by_volume = filtered_df.groupby('ticker')['dollar_volume'].sum().nlargest(5).reset_index()
    top_tickers_by_fees = filtered_df.groupby('ticker')['fees'].sum().nlargest(5).reset_index()

    st.subheader("Top 5 Tickers Traded")
    # Display tables side by side in two columns
    col1, col2 = st.beta_columns(2)
    col1.write("By Dollar Volume:")
    col1.write(top_tickers_by_volume)

    col2.write("By Fees:")
    col2.write(top_tickers_by_fees)
  
 # Top 5 sectors traded (by dollar volume and fees)
    top_sectors_by_volume = filtered_df.groupby('GICS Sector')['dollar_volume'].sum().nlargest(5).reset_index()
    top_sectors_by_fees = filtered_df.groupby('GICS Sector')['fees'].sum().nlargest(5).reset_index()

    st.subheader("Top 5 Sectors Traded")

    # Display tables side by side in two columns
    col3, col4 = st.beta_columns(2)
    col3.write("By Dollar Volume:")
    col3.write(top_sectors_by_volume)

    col4.write("By Fees:")
    col4.write(top_sectors_by_fees)

# Optionally, you can display other charts or insights for the selected clients here
