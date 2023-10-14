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


#%% Column formats
colFormats = {"date":"{:%Y-%m-%d}",
              "fees":"${:,.0f}",
              "dollar_volume":"${:,.0f}"}

# Load your financial dataset
@st.cache_data
def grabData():
  df = pd.read_excel('chatGPTDemo.xlsx', parse_dates=['date'])
  df['dollar_volume'] = df['quantity'] * df['Adj Close'] #code carried over from Part 2
  return df

df = grabData()

unique_clients = sorted(df['Client Name'].unique())
selected_clients = st.sidebar.multiselect("Select Client(s)", unique_clients)

sectors = sorted(df['GICS Sector'].unique())
selected_sectors = st.sidebar.multiselect("Pick Sector(s):",sectors)
tickers = sorted(df['ticker'].unique())
selected_tickers = st.sidebar.multiselect("Pick Ticker(s):",tickers)

num_picked = len(unique_clients)
#Filter data set by picked clients, sectors and tickers; if any of the dropdowns were left blank, use all the data 
filtered_df = df.copy()
if selected_clients:     # Filter the DataFrame based on the selected clients
    filtered_df = filtered_df[filtered_df['Client Name'].isin(selected_clients)]
    num_picked = len(selected_clients)
if selected_sectors:     # Filter the DataFrame based on the selected secotrs
    filtered_df = filtered_df[filtered_df['GICS Sector'].isin(selected_sectors)]
if selected_tickers:     # Filter the DataFrame based on the selected secotrs
    filtered_df = filtered_df[filtered_df['ticker'].isin(selected_tickers)]

layout_pick = st.sidebar.radio("Pick dashobard view:", ['Summary','Key Client Stats','Advanced Charts'])

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
  fig = px.bar(top_clients, x=top_clients.index, y='fees', title="Top {} Clients by Total Fees".format(num))
  st.plotly_chart(fig)
  
  st.header("Fees by GICS Sector")
  fig = px.pie(filtered_df, names='GICS Sector', values='fees', title="Fees by GICS Sector")
  st.plotly_chart(fig)
  
  st.header("Total Dollar Volume Traded by Ticker")
  total_volume_by_ticker = filtered_df.groupby(['ticker','GICS Sector','Client Name'])['dollar_volume'].sum().sort_values(ascending=False).reset_index()
  fig = px.bar(total_volume_by_ticker, x='ticker', y='dollar_volume', title="Total Dollar Volume Traded by Ticker",color='GICS Sector',hover_name='Client Name')
  fig.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})
  st.plotly_chart(fig)
  
  #%%Histogram of Fee per Share: Analyze the distribution of commission fees per share.
  st.header("Histogram of Fee per Share")
  fig = px.histogram(filtered_df, x='fee/share', nbins=3, title="Histogram of Fee per Share")
  st.plotly_chart(fig)
  
elif layout_pick=='Key Client Stats':
    # Total volume traded and total commissions
    total_volume = filtered_df['dollar_volume'].sum()
    total_commissions = filtered_df['fees'].sum()

    st.subheader("Key Stats for Selected Client(s)")
    kpi1, kpi2 = st.columns(2)
    kpi1.metric(label="Total Fees ($)",value="${:,.2f}".format(total_commissions))
    kpi2.metric(label="Total Volume Traded ($ mm)",value="${:,.2f}".format(total_volume/10**6))
    
    # Top 5 tickers traded (by dollar volume and fees)
    top_tickers_by_volume = filtered_df.groupby('ticker')['dollar_volume'].sum().nlargest(5).reset_index()
    top_tickers_by_fees = filtered_df.groupby('ticker')['fees'].sum().nlargest(5).reset_index()

    st.subheader("Top 5 Tickers Traded")
    # Display tables side by side in two columns
    col1, col2 = st.columns(2)
    col1.write("By Dollar Volume:")
    col1.write(top_tickers_by_volume.style.format(colFormats,na_rep="-"))

    col2.write("By Fees:")
    col2.write(top_tickers_by_fees.style.format(colFormats,na_rep="-"))
  
    # Top 5 sectors traded (by dollar volume and fees)
    top_sectors_by_volume = filtered_df.groupby('GICS Sector')['dollar_volume'].sum().nlargest(5).reset_index()
    top_sectors_by_fees = filtered_df.groupby('GICS Sector')['fees'].sum().nlargest(5).reset_index()

    st.subheader("Top 5 Sectors Traded")

    # Display tables side by side in two columns
    #col3, col4 = st.beta_columns(2) #original ChatGPT code   
    col3, col4 = st.columns(2) 
    col3.write("By Dollar Volume:")
    col3.write(top_sectors_by_volume.style.format(colFormats,na_rep="-"))

    col4.write("By Fees:")
    col4.write(top_sectors_by_fees.style.format(colFormats,na_rep="-"))
elif layout_pick == 'Advanced Charts':
    st.title('Sector Summary')
    chartType = st.radio("Chart Type",('sunburst','treemap'))
    col5, col6, col7, col8 = st.columns(4)
    categories = ['Client Name','GICS Sector', 'GICS Sub Industry','ticker']
    kpi = col5.selectbox("KPI", ['fees','dollar_volume'])
    l1 = col6.selectbox("Pick level 1",categories, 1)
    l2 = col7.selectbox("Pick level 2",categories, 2)
    l3 = col8.selectbox("Pick level 3",categories, 3)

    title = "{} by {}, {}, and {}".format(kpi, l1, l2, l3)
    if chartType == 'sunburst':
        figSector = px.sunburst(filtered_df, values=kpi, path=[l1, l2, l3], title=title)
    else:
        figSector = px.treemap(filtered_df, values=kpi, path=[l1, l2, l3], title=title)
    st.plotly_chart(figSector) 
