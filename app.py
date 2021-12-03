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
today = datetime(2021,12,1)
previous_day = today - timedelta(days=1)
HIST_DATE = st.date_input("Date: ", value=previous_day, min_value=datetime(2014,9,17), max_value=previous_day)
ORG_USD = st.number_input("USD Amount: ", min_value=1, max_value=999999999)

HIST_DATE2 = HIST_DATE.strftime("%m/%d/%Y %H:%M:%S")
HIST_DATE3 = HIST_DATE2.strptime(HIST_DATE2)
st.write(today)
st.write(HIST_DATE3)

#date reformatting
HIST_DATE_REFORMAT = HIST_DATE.strftime("%d-%m-%Y")
HIST_DATE_datetime = datetime.strptime(HIST_DATE_REFORMAT,"%d-%m-%Y")

btc_today = btc.loc[btc['Date'] == today,'Close']
btc_history = btc.loc[btc['Date'] == HIST_DATE,'Close']

btc_today = btc_today.reset_index(drop = True)
btc_history = btc_history.reset_index(drop = True)

st.write(btc_today)
st.write(btc_history)

total_btc = ORG_USD/btc_history
current_USD = total_btc[0] * btc_today[0]
perc_change = (current_USD - ORG_USD)/(ORG_USD)*100
usd_diff = current_USD - ORG_USD

st.write('''# Results''')
st.write('''## Historic Analysis''')
st.write("You would have originally bought:")
st.write(total_btc[0])
st.write("BTC")
st.write(" ")
st.write("At a price of")
st.write(btc_history[0])
st.write("USD per BTC")
st.write(" ")

st.write('''## Your Current Worth''')

st.write("That is currently worth:")
st.write(round(current_USD,2))
st.write(" ")
st.write("Which is a percentage change of")
st.write(round(perc_change, 2))
