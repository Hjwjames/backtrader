
import backtrader as bt
import pandas as pd
import datetime
from src import yfinance_data as yf_data
import json
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
        self.order = None

        # 生成交易信号
        self.sma5 = bt.indicators.SimpleMovingAverage(period=5)  # 5日均线
        self.sma10 = bt.indicators.SimpleMovingAverage(period=30)  # 10日均线
        self.buy_sig = self.sma5 < self.sma10  # 5日均下线穿30日均线买入
        self.sell_sig = self.sma5 > self.sma10  # 5日均线上穿30日均线卖出
        pass

    def next(self):
        self.log('Close, %.2f' % (self.dataClose[0]))
        if self.order:
            return

        if self.buy_sig:
            # 提取当前时间点
            print('----datetime交易日报开始----', self.datas[0].datetime.date(0))
            # 打印当前值
            print('close', self.data.close[0])
            print('sma5', self.sma5[0])
            print('sma10', self.sma10[0])
            # 比较收盘价与均线的大小
            if self.data.close > self.sma5:
                print('------收盘价上穿5日均线------')
            if self.data.close[0] > self.sma10:
                print('------收盘价上穿10日均线------')
            self.buy(size=100)
            self.log('BUY CREATE, %.2f' % self.dataClose[0])
            print('----datetime交易日报结束----', self.datas[0].datetime.date(0))

        if self.position:
            if self.sell_sig:
                # 提取当前时间点
                print('----datetime交易日报开始----', self.datas[0].datetime.date(0))
                # 打印当前值
                print('close', self.data.close[0])
                print('sma5', self.sma5[0])
                print('sma10', self.sma10[0])
                # 比较收盘价与均线的大小
                if self.data.close > self.sma5:
                    print('------收盘价上穿5日均线------')
                if self.data.close[0] > self.sma10:
                    print('------收盘价上穿10日均线------')
                self.sell(size=100)
                self.log('SELL CREATE, %.2f' % self.dataClose[0])
                print('----datetime交易日报结束----', self.datas[0].datetime.date(0))
        pass

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED,Stock: %s, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (self.dnames,
                     order.executed.price,
                     order.executed.value,
                     order.executed.comm))
                print('当前可用资金', self.broker.getcash(),'当前总资产', self.broker.getvalue() ,'当前持仓量', self.broker.getposition(self.data).size )
                print('当前持仓成本', self.broker.getposition(self.data).price,'当前持仓量', self.getposition(self.data).size,'当前持仓成本', self.getposition(self.data).price)

            else:  # Sell
                self.log('SELL EXECUTED, Stock: %s,Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (self.dnames,
                          order.executed.price,
                          order.executed.value,
                          order.executed.comm))
                print('当前可用资金', self.broker.getcash(), '当前总资产', self.broker.getvalue(), '当前持仓量',
                      self.broker.getposition(self.data).size)
                print('当前持仓成本', self.broker.getposition(self.data).price, '当前持仓量',
                      self.getposition(self.data).size, '当前持仓成本', self.getposition(self.data).price)


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