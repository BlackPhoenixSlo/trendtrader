import math
import datetime as dt

import backtrader as bt

import custom_indicators


class SMACWalkForward(bt.Strategy):
    """The SMAC strategy in a walk-forward analysis context"""

    params = {'par_tuple': None,
              'start_dates': None,
              'end_dates': None}

    def __init__(self):
        """Initialize the strategy"""

        self.fastma = dict()
        self.slowma = dict()
        self.regime = dict()

        self.date_combos = [c for c in zip(self.p.start_dates,
                                           self.p.end_dates)]

        # Error checking
        if type(self.p.start_dates) is not list or type(self.p.end_dates) \
                is not list or type(self.p.par_tuple) is not list:
            raise ValueError("Must past lists filled with numbers to params "
                             "start_dates, end_dates, fast, slow.")
        elif len(self.p.start_dates) != len(self.p.end_dates) or \
                len(self.p.par_tuple) != len(self.p.start_dates) or \
                len(self.p.par_tuple) != len(self.p.start_dates):
            raise ValueError("All lists passed to params must have same"
                             " length.")

        self.fastma = dict()
        self.slowma = dict()
        self.regime = dict()

        # Additional indexing, allowing for differing start/end dates
        for sd, ed, par in zip(self.p.start_dates, self.p.end_dates,
                               self.p.par_tuple):

            if type(sd) is not dt.date or type(ed) is not dt.date:
                raise ValueError("Only datetime dates allowed in start_dates, "
                                 "end_dates.")
            elif ed - sd < dt.timedelta(0):
                raise ValueError("Start dates must always be before end "
                                 "dates.")

            self.fastma[(sd, ed)] = bt.ind.SimpleMovingAverage(self.data.close,
                                                               period=par[0],
                                                               plot=False)
            self.slowma[(sd, ed)] = bt.ind.SimpleMovingAverage(self.data.close,
                                                               period=par[1],
                                                               plot=False)

            self.regime[(sd, ed)] = self.fastma[(sd, ed)] \
                                    - self.slowma[(sd, ed)]

    def next(self):
        """
        Define what will be done in a single step, including creating
        and closing trades
        """

        curdate = self.datetime.date(0)
        dtidx = None

        for sd, ed in self.date_combos:
            if sd <= curdate and curdate <= ed:
                dtidx = (sd, ed)

        if dtidx is not None:
            if self.position.size == 0:
                if self.regime[dtidx][0] > 0 and self.regime[dtidx][-1] <= 0:
                    self.size = math.floor(self.broker.cash / self.data.close)
                    self.buy(size=self.size)

            else:
                if self.regime[dtidx][0] <= 0 and self.regime[dtidx][-1] > 0:
                    self.close()




class STCWalkForward(bt.Strategy):

    """The STC strategy in a walk-forward analysis context"""

    params = {'par_tuple': None,
              'start_dates': None,
              'end_dates': None}

    def __init__(self):

        """Initialize the strategy"""

        self.stc = dict()
        self.crossup = dict()
        self.crossdown = dict()

        self.date_combos = [c for c in zip(self.p.start_dates,
                                           self.p.end_dates)]

        # Error checking
        if type(self.p.start_dates) is not list or type(self.p.end_dates) \
                is not list or type(self.p.par_tuple) is not list:
            raise ValueError("Must past lists filled with numbers to params "
                             "start_dates, end_dates, fast, slow.")
        elif len(self.p.start_dates) != len(self.p.end_dates) or \
                len(self.p.par_tuple) != len(self.p.start_dates) or \
                len(self.p.par_tuple) != len(self.p.start_dates):
            raise ValueError("All lists passed to params must have same "
                             "length.")

        # Additional indexing, allowing for differing start/end dates
        for sd, ed, par in zip(self.p.start_dates, self.p.end_dates,
                               self.p.par_tuple):

            # Compute the STC value
            self.stc[(sd, ed)] = custom_indicators.STC(self.data.close,
                                                       fast=par[0],
                                                       slow=par[1],
                                                       cycle=par[2],
                                                       d1Length=par[3],
                                                       d2Length=par[4],
                                                       plot=False)

            # Check if one of the crossing conditions if fulfilled for the STC
            self.crossup[(sd, ed)] = bt.ind.CrossUp(self.stc[(sd, ed)],
                                                    bt.LineNum(par[5]),
                                                    plot=False)
            self.crossdown[(sd, ed)] = bt.ind.CrossDown(self.stc[(sd, ed)],
                                                        bt.LineNum(par[6]),
                                                        plot=False)

    def next(self):

        """
        Define what will be done in a single step, including creating
        and closing trades
        """

        curdate = self.datetime.date(0)
        dtidx = None

        for sd, ed in self.date_combos:
            if sd <= curdate and curdate <= ed:
                dtidx = (sd, ed)

        if dtidx is not None:
            if self.position.size == 0:
                if self.crossup[dtidx] > 0:
                    self.size = math.floor(self.broker.cash / self.data.close)
                    self.buy(size=self.size)

            else:
                if self.crossdown[dtidx] > 0:
                    self.close()


class AroonSTCWalkForward(bt.Strategy):

    """The AROON STC strategy in a walk-forward analysis context"""

    params = {'par_tuple': None,
              'start_dates': None,
              'end_dates': None}

    def __init__(self):

        """Initialize the strategy"""

        self.stc = dict()
        self.crossup = dict()
        self.crossdown = dict()
        self.aroonup = dict()
        self.aroondown = dict()

        self.date_combos = [c for c in zip(self.p.start_dates,
                                           self.p.end_dates)]

        # Error checking
        if type(self.p.start_dates) is not list or type(self.p.end_dates) \
                is not list or type(self.p.par_tuple) is not list:
            raise ValueError("Must past lists filled with numbers to params "
                             "start_dates, end_dates, fast, slow.")
        elif len(self.p.start_dates) != len(self.p.end_dates) or \
                len(self.p.par_tuple) != len(self.p.start_dates) \
                or len(self.p.par_tuple) != len(self.p.start_dates):
            raise ValueError("All lists passed to params must have same "
                             "length.")

        for sd, ed, par in zip(self.p.start_dates, self.p.end_dates,
                               self.p.par_tuple):

            # Compute the STC value
             self.stc[(sd,ed)] = custom_indicators.STC(self.data, fast=par[0],
                                                       slow=par[1],
                                                       cycle=par[2],
                                                       d1Length=par[3],
                                                       d2Length=par[4],
                                                       plot=False)

             # Check if one of the crossing conditions if fulfilled for the STC
             self.crossup[(sd,ed)] = bt.ind.CrossUp(self.stc[(sd,ed)],
                                                    bt.LineNum(par[5]),
                                                    plot=False)
             self.crossdown[(sd,ed)] = bt.ind.CrossDown(self.stc[(sd,ed)],
                                                        bt.LineNum(par[6]),
                                                        plot=False)

             self.aroonup[(sd,ed)] = bt.ind.AroonUp(self.data,
                                                    period=int(par[7]),
                                                    plot=False)
             self.aroondown[(sd,ed)] = bt.ind.AroonDown(self.data,
                                                        period=int(par[7]),
                                                        plot=False)


    def next(self):

        """
        Define what will be done in a single step, including creating
        and closing trades
        """

        curdate = self.datetime.date(0)
        dtidx = None

        for sd, ed in self.date_combos:
            if sd <= curdate and curdate <= ed:
                dtidx = (sd, ed)

        if dtidx is not None:
            if self.position.size == 0:
                if self.crossup[dtidx] > 0 and self.aroonup[(sd,ed)] > 50 \
                        and self.aroondown[(sd,ed)] < 50:
                    self.size = math.floor(self.broker.cash / self.data.close)
                    self.buy(size=self.size)

            else:
                if self.crossdown[dtidx] > 0:
                    self.close()


class StcSmaWalkForward(bt.Strategy):

    """The STC SMA strategy in a walk-forward analysis context"""

    params = {'par_tuple': None,
              'start_dates': None,
              'end_dates': None}

    def __init__(self):

        """Initialize the strategy"""

        self.stc = dict()
        self.crossup = dict()
        self.crossdown = dict()
        self.sma = dict()

        self.date_combos = [c for c in zip(self.p.start_dates,
                                           self.p.end_dates)]

        # Error checking
        if type(self.p.start_dates) is not list or type(self.p.end_dates) \
                is not list or type(self.p.par_tuple) is not list:
            raise ValueError("Must past lists filled with numbers to params "
                             "start_dates, end_dates, fast, slow.")
        elif len(self.p.start_dates) != len(self.p.end_dates) or \
                len(self.p.par_tuple) != len(self.p.start_dates) or \
                len(self.p.par_tuple) != len(self.p.start_dates):
            raise ValueError("All lists passed to params must have same "
                             "length.")

        for sd, ed, par in zip(self.p.start_dates, self.p.end_dates,
                               self.p.par_tuple):

            # Compute the STC value
             self.stc[(sd,ed)] = custom_indicators.STC(self.data, fast=par[0],
                                                       slow=par[1],
                                                       cycle=par[2],
                                                       d1Length=par[3],
                                                       d2Length=par[4],
                                                       plot=False)

             # Check if one of the crossing conditions if fulfilled for the STC
             self.crossup[(sd,ed)] = bt.ind.CrossUp(self.stc[(sd,ed)],
                                                    bt.LineNum(par[5]),
                                                    plot=False)
             self.crossdown[(sd,ed)] = bt.ind.CrossDown(self.stc[(sd,ed)],
                                                        bt.LineNum(par[6]),
                                                        plot=False)

             self.sma[(sd,ed)] = bt.ind.SMA(self.data.close, period=par[7],
                                            plot=False)


    def next(self):

        """
        Define what will be done in a single step, including creating
        and closing trades
        """

        curdate = self.datetime.date(0)
        dtidx = None
        for sd, ed in self.date_combos:
            if sd <= curdate and curdate <= ed:
                dtidx = (sd, ed)
        if dtidx is not None:
            if self.position.size == 0:
                if (self.crossdown[dtidx] > 0 and
                        self.data.close < self.sma[dtidx]):
                    self.size = math.floor(self.broker.cash / self.data.close)
                    self.sell(size=self.size)

            else:  # We have an open position
                if (self.crossup[dtidx] > 0) or \
                        (self.data.close > self.sma[dtidx]):
                    self.close()


class StcVolWalkForward(bt.Strategy):

    """
    The STC Volatility strategy in a walk-forward analysis context
    """

    params = {'par_tuple': None,
              'start_dates': None,
              'end_dates': None}

    def __init__(self):

        """Initialize the strategy"""

        self.stc = dict()
        self.vol = dict()
        self.threshlow = dict()
        self.threshhigh = dict()
        self.crossup = dict()
        self.crossdown = dict()

        self.date_combos = [c for c in zip(self.p.start_dates,
                                           self.p.end_dates)]

        # Error checking
        if type(self.p.start_dates) is not list or type(self.p.end_dates) \
                is not list or type(self.p.par_tuple) is not list:
            raise ValueError("Must past lists filled with numbers to params "
                             "start_dates, end_dates, fast, slow.")
        elif len(self.p.start_dates) != len(self.p.end_dates) or \
                len(self.p.par_tuple) != len(self.p.start_dates) or \
                len(self.p.par_tuple) != len(self.p.start_dates):
            raise ValueError("All lists passed to params must have same "
                             "length.")

        for sd, ed, par in zip(self.p.start_dates, self.p.end_dates,
                               self.p.par_tuple):

            # Compute the STC value
             self.stc[(sd,ed)] = custom_indicators.STC(self.data, fast=par[0],
                                                       slow=par[1],
                                                       cycle=par[2],
                                                       d1Length=par[3],
                                                       d2Length=par[4],
                                                       plot=False)

             self.vol[(sd,ed)] = 100 * math.sqrt(365) \
                                 * bt.ind.StandardDeviation(
                 bt.ind.PercentChange(self.data.close, period=1, plot=False),
                 period=par[7])
             self.threshlow[(sd,ed)] = par[8]
             self.threshhigh[(sd,ed)] = par[9]

             # Check if one of the crossing conditions if fulfilled for the STC
             self.crossup[(sd,ed)] = bt.ind.CrossUp(self.stc[(sd,ed)],
                                                    bt.LineNum(par[5]),
                                                    plot=False)
             self.crossdown[(sd,ed)] = bt.ind.CrossDown(self.stc[(sd,ed)],
                                                        bt.LineNum(par[6]),
                                                        plot=False)


    def next(self):
        """
        Define what will be done in a single step, including creating
        and closing trades
        """

        curdate = self.datetime.date(0)
        dtidx = None

        for sd, ed in self.date_combos:
            if sd <= curdate and curdate <= ed:
                dtidx = (sd, ed)

        if dtidx is not None:
            if self.position.size == 0:
                if (self.crossup[dtidx] > 0 and
                        self.vol[dtidx] < self.threshlow[dtidx]):
                    self.size = math.floor(self.broker.cash / self.data.close)
                    self.buy(size=self.size)

            else:  # We have an open position
                if (self.crossdown[dtidx] > 0) or \
                        (self.vol[dtidx] > self.threshhigh[dtidx]):
                    self.close()