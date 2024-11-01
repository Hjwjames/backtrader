
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