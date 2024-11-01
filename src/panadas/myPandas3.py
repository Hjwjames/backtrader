import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import os

# 获取贵州茅台股票数据
symbol = "600519.SS"
start_date = "2024-10-21"
end_date = "2024-10-24"
path = "C:\\Users\\Administrator\\AppData\\Local\\py-yfinance\\tkr-tz.csv"
os.remove(path)

data = yf.download(symbol, start=start_date, end=end_date,interval="1m")

# 计算短期（50天）和长期（200天）移动平均
data['MA_50'] = data['Close'].rolling(window=50).mean()
data['MA_200'] = data['Close'].rolling(window=200).mean()

print(len(data.index))
print(data.index.values)

# 生成买卖信号
data['Signal'] = 0
data['Signal'][data['MA_50'] > data['MA_200']] = 1  # 短期均线上穿长期均线，产生买入信号
data['Signal'][data['MA_50'] < data['MA_200']] = -1  # 短期均线下穿长期均线，产生卖出信号

# 绘制股价和移动平均线
plt.figure(figsize=(15, 6))
plt.plot(data['Close'], label='Close Price')
plt.plot(data['MA_50'], label='50-day Moving Average')
plt.plot(data['MA_200'], label='200-day Moving Average')


# 标记买卖信号
plt.scatter(data[data['Signal'] == 1].index, data[data['Signal'] == 1]['MA_50'], marker='^', color='g', label='Buy Signal')
plt.scatter(data[data['Signal'] == -1].index, data[data['Signal'] == -1]['MA_50'], marker='v', color='r', label='Sell Signal')

plt.title("Maotai Stock Price with Moving Averages")
plt.xlabel("Date")
plt.ylabel("Price (CNY)")
plt.legend()
plt.show()