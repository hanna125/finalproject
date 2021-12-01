import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

st.write("""
# Bitcoin Self Flagellation App

This app is for those wannabe crypto bros (and sisses) who want to punish themselves by knowing how much $$ you could have 
today if you had bought Bitcoin on a certain date. 

Select the following two inputs:
- Date You Wish You Would Have Bought Bitcoin
- USD Amount You Wish You Would Have Invested
""")
st.write('---')

st.image('BTC.jpg', use_column_width=True)

#get data
btc = pd.read_csv('BTC-USD.csv')
 
# user input
st.write('''# Choose Date and Amount''')
today = datetime.utcnow().date()
previous_day = today - timedelta(days=1)
HIST_DATE = st.date_input("Date: ", value=previous_day, min_value=datetime(2014,1,1), max_value=previous_day)
ORG_USD = st.number_input("USD Amount: ", min_value=1, max_value=999999999)

#date reformatting
HIST_DATE_REFORMAT = HIST_DATE.strftime("%d-%m-%Y")
HIST_DATE_datetime = datetime.strptime(HIST_DATE_REFORMAT,"%d-%m-%Y")
