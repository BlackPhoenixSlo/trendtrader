"""Implements custom indicators not included in backtrader.

Description
----------
Collects custom made indicators that are not included in the native
backtrader package but that are usefull or necessary for my own
trading strategies.

Classes
----------
STC: Inherits from Indicator
    Represent the Schaff Trend Cycle (STC) indicator.

Functions
----------
    Implements no module functions.

Exceptions
----------
    Exports no exceptions.
"""

import backtrader as bt

class STC(bt.Indicator):
    """The Schaff Trend Cycle indicator is a momentum indicator."""

    lines = ('stc',)
    params = {('fast', float("nan")),
              ('slow', float("nan")),
              ('cycle', float("nan")),
              ('d1Length', float("nan")),
              ('d2Length', float("nan"))}

    def __init__(self):
        super(STC, self).__init__()
        mac = bt.ind.MACD(self.data, period_me1=self.p.fast,
                          period_me2=self.p.slow, period_signal=self.p.cycle,
                          plot=False)

        # Compute Slow Stochastic of MACD
        macLow = bt.ind.Lowest(mac, period=self.p.cycle, plot=False)
        macHigh = bt.ind.Highest(mac, period=self.p.cycle, plot=False)
        k = 100 * bt.DivByZero(mac - macLow, (macHigh - macLow))
        d = bt.ind.ExponentialMovingAverage(k, period=self.p.d1Length,
                                            plot=False)

        # Compute Slow Stochastic of Slow Stochastic of MACD i.e. STC
        dLow = bt.ind.Lowest(d, period=self.p.cycle, plot=False)
        dHigh = bt.ind.Highest(d, period=self.p.cycle, plot=False)
        kd = 100 * bt.DivByZero((d - dLow), (dHigh - dLow))
        self.l.stc = bt.ind.EMA(kd, period=self.p.d2Length, plot=False)