import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import os
from datetime import datetime, timedelta

# 获取股票数据 000568.SZ 泸州老窖 ,513050.SS 中概互联,000021.SZ 深科技,516880.SS 光伏50ETF,399997.SZ 中证白酒,513820.SS 红利,512480.SS,512810.SS 军工，512700.SS 银行
symbol = "399997.SZ"
#end_date = "2022-12-25" #datetime.now() #"2024-10-25"
#start_date = "2020-12-26"#end_date - timedelta(days=59) #"2024-10-18"
end_date = datetime.now()
start_date = end_date - timedelta(days=59)

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

# 下载数据Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
data = yf.download(symbol, start=start_date, end=end_date, interval="2m")

# 删除非交易时间的数据 (假设 A 股交易时间：09:30-11:30, 13:00-15:00)
data = data.between_time('09:30', '11:30').append(data.between_time('13:00', '15:00'))

# 重置索引为整数序列以去掉时间间隔空白
#data 根据时间排序
data.index.names = ['Datetime']
data = data.sort_values(by='Datetime')
data = data.reset_index()


# 确保有足够的数据进行移动平均计算
if len(data) < 1:
    print("数据量不足以计算 50 和 200 的移动平均")
else:
    # 计算短期（50周期）和长期（200周期）移动平均
    data[window_a_str] = data['Close'].rolling(window=window_a).mean()
    data[window_b_str] = data['Close'].rolling(window=window_b).mean()
    #计算短期（50周期）的斜率
    data[slope_a] = data[window_a_str].diff()
    data[slope_b] = data[window_b_str].diff()
    data[slope_close] = data['Close'].diff()

    # 生成买卖信号
    data['Signal'] = 0
    # 策略1：根据短期和长期均线的交叉产生买卖信号
    #data.loc[data[window_a_str] < data[window_b_str], 'Signal'] = 1   # 买入信号
    #data.loc[data[window_a_str] > data[window_b_str], 'Signal'] = -1  # 卖出信号

    #策略2：根据斜率判断买入信号(50周期 前3天斜率为负，今天斜率为正则卖出)
    data.loc[(data[window_a_str] > data[window_b_str]) & ((data['slope_30'].shift(3) > 0) | (data['slope_30'].shift(2) > 0) | (data['slope_30'].shift(1) > 0)) , 'Signal'] = 1
    data.loc[(data['slope_30'].shift(2) > 0) & (data['slope_30'].shift(1) > 0) & (data['slope_30'] < 0), 'Signal'] = -1



    # 绘制股价和移动平均线
    plt.figure(figsize=(15, 6))
    plt.plot(data.index, data['Close'], label='Close Price')
    plt.plot(data.index, data[window_a_str], label=window_a_str+'-period Moving Average')
    plt.plot(data.index, data[window_b_str], label=window_b_str+'-period Moving Average')
    #plt.plot(data.index, data[window_c_str], label=window_c_str + '-period Moving Average')

    # 标记买卖信号
    plt.scatter(data[data['Signal'] == 1].index, data[data['Signal'] == 1][window_a_str], marker='^', color='g', label='Buy Signal', alpha=0.3)
    plt.scatter(data[data['Signal'] == -1].index, data[data['Signal'] == -1][window_a_str], marker='v', color='r', label='Sell Signal', alpha=1)

    # 设置 x 轴的时间刻度标签
    xticks = range(0, len(data), len(data) // 10)  # 每隔固定步长设置一个时间刻度
    xlabels = data['Datetime'].iloc[xticks].dt.strftime('%Y-%m-%d %H:%M')  # 获取对应的时间标签
    plt.xticks(ticks=xticks, labels=xlabels, rotation=45)

    # 设置标题和标签
    plt.title(symbol+" Stock Price with Moving Averages")
    plt.xlabel("Date")
    plt.ylabel("Price (CNY)")
    plt.legend()

    plt.tight_layout()
    plt.show()