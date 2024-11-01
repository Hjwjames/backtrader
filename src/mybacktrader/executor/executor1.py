import backtrader
import backtrader as bt
import pandas as pd
import datetime
import json

from src import yfinance_data as yf_data
from src.mybacktrader.strategy import strategy1 as Strategy1
from src.mybacktrader.strategy import strategy2 as Strategy2
# 获取股票数据 000568.SZ 泸州老窖 ,513050.SS 中概互联,000021.SZ 深科技,516880.SS 光伏50ETF,399997.SZ 中证白酒,513820.SS 红利,512480.SS,512810.SS 军工，512700.SS 银行,600519.SS 贵州茅台
def get_stock_data(symbol,start_date,end_date,interval):
    global cerebro
    dataframe = yf_data.get_data(symbol, start_date, end_date, interval)
    cerebro = bt.Cerebro(stdstats=False)
    cerebro.addstrategy(bt.Strategy)
    data = bt.feeds.PandasData(dataname=dataframe, datetime='Datetime', nocase=True, )
    cerebro.adddata(data, name=symbol)
    print(symbol + "All stock Done !")


class my_BuySell(bt.observers.BuySell):
    params = (('barplot', True), ('bardist', 0.02))
    plotlines = dict(
        buy=dict(marker=r'$\Uparrow$', markersize=10.0, color='#d62728'),
        sell=dict(marker=r'$\Downarrow$', markersize=10.0, color='#2ca02c'))

# 修改 Trades 观测器的样式
class my_Trades(bt.observers.Trades):
    plotlines = dict(
    pnlplus=dict(_name='Positive',
                 marker='^', color='#ed665d',
                 markersize=8.0, fillstyle='full'),
    pnlminus=dict(_name='Negative',
                  marker='v', color='#729ece',
                  markersize=8.0, fillstyle='full'))

if __name__ == '__main__':
    # 实例化 cerebro
    cerebro = bt.Cerebro()
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=400)
    get_stock_data("600519.SS", start_date, end_date, "1d")
    #get_stock_data("513050.SS", start_date, end_date, "1d")

    # 初始资金 100,000,000
    cerebro.broker.setcash(100000000.0)
    # 佣金，双边各 0.0001
    cerebro.broker.setcommission(commission=0.001)
    # 滑点：双边各 0.0001
    cerebro.broker.set_slippage_perc(perc=0.001)
    cerebro.addanalyzer(bt.analyzers.TimeReturn, _name='pnl')  # 返回收益率时序数据
    cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name='_AnnualReturn')  # 年化收益率
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='_SharpeRatio')  # 夏普比率
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='_DrawDown')  # 回撤

    # 将编写的策略添加给大脑
    cerebro.addstrategy(Strategy2.TestStrategy)

    # 画图
    cerebro.addobserver(bt.observers.Broker)
    cerebro.addobserver(bt.observers.BuySell)
    cerebro.addobserver(bt.observers.DrawDown)
    #cerebro.addobserver(my_Trades)
    #cerebro.addobserver(my_BuySell)

    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    # 启动回测
    result = cerebro.run()
    # 从返回的 result 中提取回测结果
    strat = result[0]
    # 返回日度收益率序列
    daily_return = pd.Series(strat.analyzers.pnl.get_analysis())
    # 打印评价指标
    print("--------------- AnnualReturn -----------------")
    print(strat.analyzers._AnnualReturn.get_analysis())
    print("--------------- SharpeRatio -----------------")
    print(strat.analyzers._SharpeRatio.get_analysis())
    print("--------------- DrawDown -----------------")
    print(strat.analyzers._DrawDown.get_analysis())
    print("--------------- pnl -----------------")
    print(strat.analyzers.pnl.get_analysis())
    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.plot(iplot=False,
                 style='candel',  # 设置主图行情数据的样式为蜡烛图
                 numfigs=1,
                 #lcolors=tableau10,  # 重新设置主题颜色
                 plotdist=0.1,  # 设置图形之间的间距
                 barup='#ff9896', bardown='#98df8a',  # 设置蜡烛图上涨和下跌的颜色
                 volup='#ff9896', voldown='#98df8a',  # 设置成交量在行情上涨和下跌情况下的颜色
                 )








