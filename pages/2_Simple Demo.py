import streamlit as st

#%% App Details
appDetails = """
Created by: [Bogdan Tudose](https://www.linkedin.com/in/tudosebogdan/) \n
Date: Oct 16, 2023 \n
ChatGPT Prompt: Can you help me create a simple dashboard with streamlit?
"""
with st.expander("See app info"):
    st.write(appDetails)

#%% ChatGPT Code
st.title("Simple Streamlit Dashboard")

# Add a header
st.header("Data Visualization")

# Add some text
st.write("This is a simple Streamlit dashboard.")

# Create a button widget
if st.button("Click me"):
    st.write("You clicked the button!")

# Add a chart (e.g., a line chart)
chart_data = pd.DataFrame({'x': [1, 2, 3, 4, 5], 'y': [10, 20, 30, 40, 50]})
st.line_chart(chart_data)
