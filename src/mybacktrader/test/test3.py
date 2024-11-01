# Lesson1：Backtrader来啦
# link: https://mp.weixin.qq.com/s/7S4AnbUfQy2kCZhuFN1dZw

#%%
import backtrader as bt
import pandas as pd
import datetime
from src import yfinance_data as yf_data
import json

# 实例化 cerebro
cerebro = bt.Cerebro()

def get_stock_data(symbol,start_date,end_date,interval):
    global cerebro
    dataframe = yf_data.get_data(symbol, start_date, end_date, interval)
    cerebro = bt.Cerebro(stdstats=False)
    cerebro.addstrategy(bt.Strategy)
    data = bt.feeds.PandasData(dataname=dataframe, datetime='Datetime', nocase=True, )
    cerebro.adddata(data, name=symbol)
    print(symbol + "All stock Done !")

end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days=400)
get_stock_data("000568.SZ",start_date,end_date,"1d")
get_stock_data("513050.SS",start_date,end_date,"1d")

#%%

# 回测策略
class TestStrategy(bt.Strategy):
    params = (
        ('maperiod1', 5),
        ('maperiod2', 30),
    )
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataClose = self.datas[0].close
        self.dnames = self.datas[0]._name
        self.sma1 = bt.indicators.SimpleMovingAverage(self.datas[0], period=self.params.maperiod1)
        self.sma2 = bt.indicators.SimpleMovingAverage(self.datas[0], period=self.params.maperiod2)
        self.myStakes = {}
        self.order = None
        self.price = 0
        self.amount = 0
        pass

    def next(self):
        self.log('Close, %.2f' % (self.dataClose[0]))
        if self.order:
            return


        if (self.sma1[0] < self.sma2[0]):
            self.order = self.buy()
            self.log('BUY CREATE, %.2f' % self.dataClose[0])

        if self.position:
            if(self.sma1[0] > self.sma2[0]):
                self.order = self.sell()
                self.log('SELL CREATE, %.2f' % self.dataClose[0])
        pass

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED,Stock: %s, Price: %.2f, Cost: %.2f, Comm %.2f,remain: %.2f' %
                    (self.dnames,
                     order.executed.price,
                     order.executed.value,
                     order.executed.comm,self.broker.getvalue()))
                self.myStakes[order.ref] = order.executed.price
                self.price = (self.price * self.amount + order.executed.price * order.executed.size) / (self.amount + order.executed.size)
                self.amount = self.amount + order.executed.size

            else:  # Sell
                self.log('SELL EXECUTED, Stock: %s,Price: %.2f, Cost: %.2f, Comm %.2f,remain: %.2f' %
                         (self.dnames,
                          order.executed.price,
                          order.executed.value,
                          order.executed.comm,self.broker.getvalue()))
                self.myStakes[order.ref] = order.executed.price
                self.price = (self.price * self.amount - order.executed.price * order.executed.size) / (self.amount - order.executed.size)
                self.amount = self.amount - order.executed.size


            self.bar_executed = len(self)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None


    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                (trade.pnl, trade.pnlcomm))


# 初始资金 100,000,000
cerebro.broker.setcash(100000000.0)
# 佣金，双边各 0.0003
cerebro.broker.setcommission(commission=0.0003)
# 滑点：双边各 0.0001
cerebro.broker.set_slippage_perc(perc=0.005)

cerebro.addanalyzer(bt.analyzers.TimeReturn, _name='pnl')  # 返回收益率时序数据
#cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name='_AnnualReturn')  # 年化收益率
cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='_SharpeRatio')  # 夏普比率
cerebro.addanalyzer(bt.analyzers.DrawDown, _name='_DrawDown')  # 回撤

# 将编写的策略添加给大脑，别忘了 ！
cerebro.addstrategy(TestStrategy)
# Print out the starting conditions
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
# 启动回测
result = cerebro.run()
# 从返回的 result 中提取回测结果
strat = result[0]
# 返回日度收益率序列
daily_return = pd.Series(strat.analyzers.pnl.get_analysis())
# 打印评价指标
#print("--------------- AnnualReturn -----------------")
#(strat.analyzers._AnnualReturn.get_analysis())
print("--------------- SharpeRatio -----------------")
print(strat.analyzers._SharpeRatio.get_analysis())
print("--------------- DrawDown -----------------")
print(strat.analyzers._DrawDown.get_analysis())
print("--------------- pnl -----------------")
print(strat.analyzers.pnl.get_analysis())
# Print out the final result
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.plot(style='bar', width=50, height=10)



