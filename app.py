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
btc = pd.read_csv('BTC-USD.csv', parse_dates = ['Date'])
 
# user input
st.write('''# Choose Date and Amount''')
today = datetime.utcnow().date()
previous_day = today - timedelta(days=1)
HIST_DATE = st.date_input("Date: ", value=previous_day, min_value=datetime(2014,9,17), max_value=previous_day)
ORG_USD = st.number_input("USD Amount: ", min_value=1, max_value=999999999)

#date reformatting
HIST_DATE_REFORMAT = HIST_DATE.strftime("%d-%m-%Y")
HIST_DATE_datetime = datetime.strptime(HIST_DATE_REFORMAT,"%d-%m-%Y")

btc_today = btc.loc[btc['Date'] == today,'Close']
btc_history = btc.loc[btc['Date'] == HIST_DATE,'Close']

st.write('''# Results''')
st.write('''## Historic Analysis''')
st.write("You would have originally bought: ***{:,.2f}*** BTC".format(round((ORG_USD/btc_history),5)))
st.write("At a price of ***{:,.9f}*** per BTC".format(btc_history))
st.write(" ")

st.write('''## Your Current Worth''')
total_btc = ORG_USD/btc_history
current_USD = total_btc * btc_today
perc_change = (current_USD - ORG_USD)/(ORG_USD)*100
usd_diff = current_USD - ORG_USD

st.write("That is currently worth: ***${:,.2f}***".format(round(current_USD,2)))
st.write("Which is a percentage change of ***{:,.2f}%***".format(round(perc_change, 2),))
