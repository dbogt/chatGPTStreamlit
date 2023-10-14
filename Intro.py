import streamlit as st
st.title("2023 Free Learning Series: Financial Dashboards with Python and ChatGPT")
text = """
## This Free Learning Series will take place from 11 am to 12 pm ET on Monday, October 16, 2023 via Zoom.

Learn how to create quick interactive dashboards with Python to drill down on financial data sets for better insights. This complimentary Virtual Learning Series will showcase how ChatGPT can be used to boost productivity by creating some initial dummy Python code for a dashboard using the streamlit and plotly packages.

In a few minutes, our expert will modify the generated code and demo how a dashboard can be created and launched to share their analysis with teammates. Our expert will also compare the live stand-alone web app with integrating Python directly in Excel.

**What we Will Cover?**

- Aggregating and importing financial data from Excel into Python
- Best practices in using ChatGPT to create and improve dummy code for Python
- Creating interactive dashboards and visualizations using streamlit and plotly Python packages
- Using Python directly in Excel to generate powerful graphs without installing any additional software
- Comparing stand-alone Python web apps with dashboards in Excel
- Deploying and sharing streamlit dashboards with teammates at a firm
"""

st.markdown(text)

st.sidebar.markdown("About Instructor:")
st.sidebar.image("https://avatars.githubusercontent.com/u/59750436?v=4")
st.sidebar.write("Bogdan is Co-Head of Data Science and instructor at Training The Street, delivering a variety of courses that focus on financial modeling, data sciences, and programming.")
st.sidebar.write("Github: https://github.com/dbogt")
