"""Implement trading strategies logic.

Description
----------
Implement the logic part of actual trading strategies so they can be used
in optimization and backtesting.

Classes
----------
SMAC: Inherits from Strategy
    Implement the logic of a simple moving average crossover strategy.
Stc: Inherits from Strategy
    Implement the logic of a simple Schaff Trend Cycle strategy.
AroonStc:
    Implement the logic of a strategy combining the AROON and the STC
    indicators.
StcSmaShort:
    Implement the logic of a short strategy combining the STC and SMA
    indicators.
StcVol:
    Implement the logic of a strategy combining the STC indicator and
    volatility.
DRSIDMA:
    Implement the logic of a strategy utilizing the derivative of a
    moving average and an RSI indicator.

Functions
----------
    Implements no module functions.

Exceptions
----------
    Exports no exceptions.
"""

import math

import backtrader as bt

import custom_indicators
import custom_basicops




class SMAC(bt.Strategy):
    """Implement the logic of a sma crossover strategy."""
                            # Fast MA,     Slow MA
    params = {('par_tuple', (float('nan'), float('nan'),))}

    def __init__(self):
        """Initialize the strategy"""

        self.fastma = dict()
        self.slowma = dict()
        self.regime = dict()

        self.fastma = bt.ind.SimpleMovingAverage(self.data.close,
                                                 period=self.params.par_tuple[0],
                                                 plotname="FastMA")
        self.slowma = bt.ind.SimpleMovingAverage(self.data.close,
                                                 period=self.params.par_tuple[1],
                                                 plotname="SlowMA")

        # Get the regime, positive when bullish
        self.l.equity = bt.ind.SimpleMovingAverage()
        self.regime = self.fastma - self.slowma

    def next(self):
        if self.position.size == 0:
            if self.regime[0] > 0 and self.regime[-1] <= 0:
                    self.size = math.floor(self.broker.cash / self.data.close)
                    self.buy(size=self.size)

        else:
            if self.regime[0] <= 0 and self.regime[-1] > 0:
                self.close()



class Stc(bt.Strategy):
    """Implement the logic of a simple Schaff Trend Cycle strategy."""

                             # Fast MA,     Slow MA,      Cycle Length,
    params = {('par_tuple', (float('nan'), float('nan'), float('nan'),
                             # d1 Length,  d2 Length,    Low STC Line,
                             float('nan'), float('nan'), float('nan'),
                             # High STC Line
                             float('nan'),))}

    def __init__(self):
        # Compute the STC value
        self.stc = custom_indicators.STC(self.data, fast=self.p.par_tuple[0],
                                         slow=self.p.par_tuple[1],
                                         cycle=self.p.par_tuple[2],
                                         d1Length=self.p.par_tuple[3],
                                         d2Length=self.p.par_tuple[4])

        # Check if one of the crossing conditions if fulfilled for the STC
        self.crossup = bt.ind.CrossUp(self.stc,
                                      bt.LineNum(self.p.par_tuple[5]),
                                      plot=False)
        self.crossdown = bt.ind.CrossDown(self.stc,
                                          bt.LineNum(self.p.par_tuple[6]),
                                          plot=False)

    def next(self):
        if self.position.size == 0:
            if self.crossup > 0:
                self.size = math.floor(self.broker.cash
                                       / self.data.close)
                self.buy(size=self.size)

        if self.position.size > 0:
            if self.crossdown > 0:
                self.close()

class AroonStc(bt.Strategy):
    """A strategy combining the AROON and the STC indicators."""

                             # Fast MA,     Slow MA,      Cycle Length,
    params = {('par_tuple', (float('nan'), float('nan'), float('nan'),
                            # d1 Length,  d2 Length,    Low STC Line,
                            float('nan'), float('nan'), float('nan'),
                            # High STC Line, AROON Length
                            float('nan'), float('nan'),))}

    def __init__(self):
        # Compute the STC value

        self.stc = custom_indicators.STC(self.data, fast=self.p.par_tuple[0],
                                         slow=self.p.par_tuple[1],
                                         cycle=self.p.par_tuple[2],
                                         d1Length=self.p.par_tuple[3],
                                         d2Length=self.p.par_tuple[4],
                                         plot=False)

        # Check if one of the crossing conditions if fulfilled for the STC
        self.crossup = bt.ind.CrossUp(self.stc,
                                      bt.LineNum(self.p.par_tuple[5]),
                                      plot=False)
        self.crossdown = bt.ind.CrossDown(self.stc,
                                          bt.LineNum(self.p.par_tuple[6]),
                                          plot=False)

        self.aroonup = bt.ind.AroonUp(self.data,
                                      period=int(self.p.par_tuple[7]),
                                      plot=False)
        self.aroondown = bt.ind.AroonDown(self.data,
                                          period=int(self.p.par_tuple[7]),
                                          plot=False)

    def next(self):
        if self.position.size == 0:
            if self.crossup > 0 and self.aroonup > 50 and self.aroondown < 50:
                self.size = math.floor(self.broker.cash / self.data.close)
                self.buy(size=self.size)

        if self.position.size > 0:
            if self.crossdown > 0:
                self.close()


class StcSmaShort(bt.Strategy):
    """A short strategy combining the STC and SMA indicators."""

                             # Fast MA,     Slow MA,      Cycle Length,
    params = {('par_tuple', (float('nan'), float('nan'), float('nan'),
                             # d1 Length,  d2 Length,    Low STC Line,
                             float('nan'), float('nan'), float('nan'),
                             # High STC Line, Lenght SMA
                             float('nan'), float('nan'),))}

    def __init__(self):
        # compute the STC value
        self.stc = custom_indicators.STC(self.data.close,
                                         fast=self.p.par_tuple[0],
                                         slow=self.p.par_tuple[1],
                                         cycle=self.p.par_tuple[2],
                                         d1Length=self.p.par_tuple[3],
                                         d2Length=self.p.par_tuple[4],
                                         plot=False)

        # Check if one of the crossing conditions if fulfilled for the STC
        self.crossup = bt.ind.CrossUp(self.stc,
                                      bt.LineNum(self.p.par_tuple[5]),
                                      plot=False)
        self.crossdown = bt.ind.CrossDown(self.stc,
                                          bt.LineNum(self.p.par_tuple[6]),
                                          plot=False)

        self.sma = bt.ind.MovingAverageSimple(self.data.close,
                                              period=self.p.par_tuple[7],
                                              plot=False)

    def next(self):
        if self.position.size == 0:
            if (self.crossdown > 0 and self.data.close < self.sma):
                self.size = math.floor(self.broker.cash / self.data.close)
                self.sell(size=self.size)

        if self.position.size != 0:
            if (self.crossup > 0) or (self.data.close > self.sma):
                self.close()

class StcVol(bt.Strategy):
    """A strategy combining the STC indicator and volatility."""
                            # Fast MA,     Slow MA,      Cycle Length,
    params = {('par_tuple', (float("nan"), float('nan'), float('nan'),
                             # d1 Length,  d2 Length,    Low STC Line,
                             float("nan"), float('nan'), float('nan'),
                             # High STC Line, Lookback Vol, Vol Thresh Low,
                             float("nan"), float('nan'), float('nan'),
                             # Vol Thresh High
                             float('nan'),))}

    def __init__(self):
        # compute the STC value
        self.stc = custom_indicators.STC(self.data.close,
                                         fast=self.p.par_tuple[0],
                                         slow=self.p.par_tuple[1],
                                         cycle=self.p.par_tuple[2],
                                         d1Length=self.p.par_tuple[3],
                                         d2Length=self.p.par_tuple[4],
                                         plot=False)

        # Compute Volatility
        self.vol = 100 * math.sqrt(365) * bt.ind.StandardDeviation(
            bt.ind.PercentChange(self.data.close, period=1, plot=False),
            period=self.p.par_tuple[7])

        # Check if one of the crossing conditions if fulfilled for the STC
        self.crossup = bt.ind.CrossUp(self.stc,
                                      bt.LineNum(self.p.par_tuple[5]),
                                      plot=False)
        self.crossdown = bt.ind.CrossDown(self.stc,
                                          bt.LineNum(self.p.par_tuple[6]),
                                          plot=False)

    def next(self):
        if self.position.size == 0:
            if self.crossup > 0 and self.vol < self.p.par_tuple[8]:
                self.size = math.floor(self.broker.cash / self.data.close)
                self.buy(size=self.size)

        if self.position.size > 0:
            if self.crossdown > 0 or self.vol > self.p.par_tuple[9]:
                self.close()



class DRSIDMALong(bt.Strategy):
    """A strategy using the derivative of a moving average and RSI."""

                            # MA length,  MA derivative, MA smoothing factor
    params = {('par_tuple', (float("nan"), float('nan'), float('nan'),
                            # Mom length, Mom derivative, Mom smoothing factor
                             float("nan"), float('nan'), float('nan'),
                            # Upper Threshold, Lower Threshold
                             float("nan"), float('nan'),))}

    def __init__(self):
        # Delta MA
        self.tema = bt.ind.TEMA(self.data.close, period=self.p.par_tuple[0],
                                plot=False)
        self.divTema = \
            custom_basicops.BackwardDifferenceQuotient(
                self.tema,
                period=self.p.par_tuple[1])
        self.smoothAvg = bt.ind.SMA(self.divTema, period=self.p.par_tuple[2])

        self.mom = bt.ind.RSI(bt.ind.ROC(self.data.close,
                                         period=self.p.par_tuple[3],
                                         plot=False),
                              period=self.p.par_tuple[3])
        self.divMom = \
            custom_basicops.BackwardDifferenceQuotient(
                self.mom,
                period=self.p.par_tuple[4])
        self.smoothMom = bt.ind.SMA(self.divMom, period=self.p.par_tuple[5])

    def next(self):
        if self.position.size <= 0:
            if (self.smoothAvg >= self.p.par_tuple[6]) \
                    and (self.smoothMom > self.p.par_tuple[6]):

                self.size = math.floor(self.broker.cash / self.data.close)
                self.buy(size=self.size)

        if self.position.size >= 0:
            if (self.smoothAvg < -self.p.par_tuple[7]) \
                    and (self.smoothMom < -self.p.par_tuple[7]):

                if self.position.size > 0:
                    self.close()


class DRSIDMAShort(bt.Strategy):
    """A strategy using the derivative of a moving average and RSI."""

                            # MA length,  MA derivative, MA smoothing factor
    params = {('par_tuple', (float("nan"), float('nan'), float('nan'),
                            # Mom length, Mom derivative, Mom smoothing factor
                             float("nan"), float('nan'), float('nan'),
                            # Upper Threshold, Lower Threshold
                             float("nan"), float('nan'),))}

    def __init__(self):
        # Delta MA
        self.tema = bt.ind.TEMA(self.data.close, period=self.p.par_tuple[0],
                                plot=False)
        self.divTema = \
            custom_basicops.BackwardDifferenceQuotient(
                self.tema,
                period=self.p.par_tuple[1])
        self.smoothAvg = bt.ind.SMA(self.divTema, period=self.p.par_tuple[2])

        self.mom = bt.ind.RSI(bt.ind.ROC(self.data.close,
                                         period=self.p.par_tuple[3],
                                         plot=False),
                              period=self.p.par_tuple[3])
        self.divMom = \
            custom_basicops.BackwardDifferenceQuotient(
                self.mom,
                period=self.p.par_tuple[4])
        self.smoothMom = bt.ind.SMA(self.divMom, period=self.p.par_tuple[5])

    def next(self):
        if self.data.funding < 0:
            if self.position.size <= 0:
                if (self.smoothAvg >= self.p.par_tuple[6]) \
                        and (self.smoothMom > self.p.par_tuple[6]):

                    if self.position.size < 0:
                        self.close()

            if self.position.size >= 0:
                if (self.smoothAvg < -self.p.par_tuple[7]) \
                        and (self.smoothMom < -self.p.par_tuple[7]):
                    self.size = math.floor(self.broker.cash / self.data.close)
                    self.sell(size=self.size)
        else:
            if (self.position.size < 0) \
                    and (self.smoothAvg >= self.p.par_tuple[6]) \
                    and (self.smoothMom > self.p.par_tuple[6]):
                self.close()

