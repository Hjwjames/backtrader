import pandas as pd
import yfinance as yf
import finplot as fplt
import os

start_date = "2024-10-23"
end_date = "2024-10-24"
path = "C:\\Users\\Administrator\\AppData\\Local\\py-yfinance\\tkr-tz.csv"

# CREATE A TICKER INSTANCE FOR TESLA
os.remove(path)
tsla = yf.Ticker('600519.SS')

# RETRIEVE 1 YEAR WORTH OF DAILY DATA OF TESLA
df = tsla.history(start = start_date,end=end_date,interval='1m')
#for i in range(0, len(df)):
#    print(df.iloc[i])

# 解析df对象



# PLOT THE OHLC CANDLE CHART
#fplt.candlestick_ochl(df[['Open','Close','High','Low']])
#fplt.add_line(df[].keys())
fplt.show()