import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import warnings
from pmdarima import auto_arima
from statsmodels.tsa.statespace.sarimax import SARIMAX
from pylab import rcParams
import statsmodels.api as sm
from fbprophet import Prophet



st.write("""
# Bitcoin Self Flagellation App

This app is for those wannabe crypto millionaires who want to punish themselves by knowing how much $$ you could have 
today if you had bought Bitcoin on a certain date.  

Select the following two inputs:
- Date You Wish You Would Have Bought Bitcoin
- USD Amount You Wish You Would Have Invested

After you see what you could have missed out on, the app will show you an output of a Facebook Prophet forecast and ARIMA time series model""")
st.write('---')

st.image('BTC.jpg', use_column_width=True)

#get data
btc = pd.read_csv('BTC-USD.csv', parse_dates = ['Date'])
 
# user input
st.write('''# Choose Date and Amount''')
today = datetime(2021,12,6)
previous_day = today - timedelta(days=1)
HIST_DATE = st.date_input("Date: ", value=previous_day, min_value=datetime(2014,9,17), max_value=previous_day)
#ORG_USD = st.number_input("USD Amount: ", min_value=1, max_value=999999999)
ORG_USD = st.slider("USD Amount Purchased",10, 10000, step=10)

#date reformatting
HIST_DATE_REFORMAT = HIST_DATE.strftime("%d-%m-%Y")
HIST_DATE_datetime = datetime.strptime(HIST_DATE_REFORMAT,"%d-%m-%Y")

btc_today = btc.loc[btc['Date'] == today,'Close']
btc_history = btc.loc[btc['Date'] == HIST_DATE_datetime,'Close']

btc_today = btc_today.reset_index(drop = True)
btc_history = btc_history.reset_index(drop = True)

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
st.write(" ")
st.write("At a price of")
st.write(btc_history[0])
st.write("USD per BTC")
st.write(" ")

st.write('''## Your Current Worth''')

st.write("That is currently worth:")
st.write(round(current_USD,2))
st.write("USD")
st.write(" ")
st.write("Which is a percentage change of")
st.write(round(perc_change, 2))


if usd_diff == 0:
   st.write('''# You Broke Even''')
elif usd_diff <= 0:
   st.write('''# You Would Have Lost''')
else:
   st.write('''# You Missed Out On''') 
st.write(abs(round(usd_diff,2)))
st.write("USD") 

st.image('BTC2.jpg', use_column_width=True)

historical_prices = btc.loc[btc['Date'] >= HIST_DATE_datetime,['Date','Close']]

st.write(" ")
st.write(" ")
st.write("BTC price history from selected date to current:")
st.line_chart(historical_prices.set_index('Date'))

st.write(" ")
st.write(" ")
st.write('---')
st.header('Time Series Forecast - Facebook Prophet')
st.write(" ")
st.write("Time series forecast of next year BTC close price with range:")
# Facebook Prophet forecasting
# Re-import BTC data and rename columns to ds and y to comply with Prophet
btc = pd.read_csv('BTC-USD.csv', parse_dates = ['Date'])
btc = pd.DataFrame(btc)
btc = btc.rename(columns={'Date':'ds', 'Close':'y'})

m = Prophet()
m.fit(btc)

future = m.make_future_dataframe(periods=365)
forecast = m.predict(future)
fig1 = m.plot(forecast,xlabel='Year', ylabel='BTC Close Price')
st.pyplot(fig1)

st.write('---')
st.write(" ")
st.write(" ")

st.write("Deeper analysis:")
fig2 = m.plot_components(forecast)
st.pyplot(fig2)

#model2 = sm.tsa.statespace.SARIMAX(train, order = (1, 1, 2), seasonal_order = (1,1,0,12), enforce_stationarity = False, enforce_invertibility=False)
#forecast2 = results.get_prediction(start=pd.to_datetime('2019-12-03'), dynamic = False) 
#pred_ci = forecast2.conf_int()
#
#ax = train['2014-12-06':].plot(label='observed')
#forecast2.predicted_mean.plot(ax=ax, label='One-step ahead Forecast', alpha=.7, figsize=(14, 7))
#ax.fill_between(pred_ci.index,
#                pred_ci.iloc[:, 0],
#                pred_ci.iloc[:, 1], color='k', alpha=.2)
#ax.set_xlabel('Date')
#ax.set_ylabel('BTC Close Price')
#fig, ax = plt.subplots()
#plt.legend()
#plt.show()
#st.pyplot(fig)

st.write('---')
st.write(" ")
st.write(" ")

st.header("Summary of ARIMA time series model: ")
st.write(" ")
st.write(" ")

btc = pd.read_csv('BTC-USD.csv', parse_dates = ['Date'])
warnings.filterwarnings("ignore")
btc2 = pd.read_csv('BTC-USD.csv', index_col = 'Date', parse_dates = ['Date'])
train = btc.iloc[:len(btc2)-365]
test = btc.iloc[len(btc2)-365:]
model = SARIMAX(train['Close'], 
                order = (1, 1, 2),
               seasonal_order =(2, 0, 2, 12))
result = model.fit()
result = result.summary()
st.write(result)


