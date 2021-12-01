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
