import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import os
from datetime import datetime, timedelta

# 获取股票数据 000568.SZ 泸州老窖 ,513050.SS 中概互联,000021.SZ 深科技,516880.SS 光伏50ETF,399997.SZ 中证白酒,513820.SS 红利,512480.SS,512810.SS 军工，512700.SS 银行
def_symbol = "000568.SZ"
#end_date = "2022-12-25" #datetime.now() #"2024-10-25"
#start_date = "2020-12-26"#end_date - timedelta(days=59) #"2024-10-18"
def_end_date = datetime.now()
def_start_date = def_end_date - timedelta(days=59)
def_interval = "1d"
def get_data(symbol,start_date,end_date,interval):
    path = "C:\\Users\\Administrator\\AppData\\Local\\py-yfinance\\tkr-tz.csv"

    # 如果存在文件则删除
    if os.path.exists(path):
        os.remove(path)

    # 下载数据Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
    data = yf.download(symbol, start=start_date, end=end_date, interval=interval)

    # 删除非交易时间的数据 (假设 A 股交易时间：09:30-11:30, 13:00-15:00)
    if(interval != "5m" and interval != "1d" and interval != "1wk" and interval != "1mo" and interval != "3mo"):
        data = data.between_time('09:30', '11:30').append(data.between_time('13:00', '15:00'))

    data.index.names = ['Datetime']
    data = data.sort_values(by='Datetime')
    data = data.reset_index()
    return data

if __name__ == '__main__':
    data = get_data(def_symbol,def_start_date,def_end_date,def_interval)
    print(data)