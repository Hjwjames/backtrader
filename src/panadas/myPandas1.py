import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import os

# 获取股票数据
symbol = "600519.SS"
start_date = "2024-10-23"
end_date = "2024-10-24"
path = "C:\\Users\\Administrator\\AppData\\Local\\py-yfinance\\tkr-tz.csv"
os.remove(path)


maotai = yf.Ticker(symbol)
maotai_hist = maotai.history(start = start_date,end=end_date,interval='1m')
# 简单的数据分析
print(maotai_hist)


# 绘制股价走势图
maotai_hist['Close'].plot(figsize=(15, 6), label=symbol)
plt.title(f"{symbol} Stock Price")
plt.xlabel("Datetime")
plt.ylabel("Open")
plt.legend()
plt.show()