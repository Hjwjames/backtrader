import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import os
from datetime import datetime, timedelta


end_date = datetime.now()
start_date = end_date - timedelta(days=59)
symbol_list = ['000568.SZ','513050.SS','000021.SZ','516880.SS','399997.SZ','513820.SS','512480.SS','512810.SS','512700.SS']
good_symbol_list = []

path = "C:\\Users\\Administrator\\AppData\\Local\\py-yfinance\\tkr-tz.csv"
window_a = 30
window_b = 100
window_a_str = 'MA_30'
window_b_str = 'MA_100'
slope_a = 'slope_30'
slope_b = 'slope_100'
slope_close = 'slope_close'

# 如果存在文件则删除
if os.path.exists(path):
    os.remove(path)


for symbol in symbol_list:
    if os.path.exists(path):
        os.remove(path)
    # 下载数据Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
    data = yf.download(symbol, start=start_date, end=end_date, interval="2m")
    # 删除非交易时间的数据 (假设 A 股交易时间：09:30-11:30, 13:00-15:00)
    data = data.between_time('09:30', '11:30').append(data.between_time('13:00', '15:00'))

    # 计算短期（50周期）和长期（200周期）移动平均
    data[window_a_str] = data['Close'].rolling(window=window_a).mean()
    data[window_b_str] = data['Close'].rolling(window=window_b).mean()
    # 计算短期（50周期）的斜率
    data[slope_a] = data[window_a_str].diff()
    data[slope_b] = data[window_b_str].diff()
    data[slope_close] = data['Close'].diff()

    #生成买卖信号
    data.loc[(data[window_a_str] > data[window_b_str]) & ((data['slope_30'].shift(3) > 0) | (data['slope_30'].shift(2) > 0) | (data['slope_30'].shift(1) > 0)), 'Signal'] = 1
    data.loc[(data['slope_30'].shift(2) > 0) & (data['slope_30'].shift(1) > 0) & (data['slope_30'] < 0), 'Signal'] = -1

    if data['Signal'].iloc[-1] == 1:
        good_symbol_list.append(symbol)

print(good_symbol_list)