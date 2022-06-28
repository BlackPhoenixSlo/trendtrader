"""Implments several methods for optimization.

Description
----------
Implements methods for random search optimization, walk forward
optimization.

Classes
----------
    TimeSeriesSplitImproved: Inherits from TimeSeriesSplit
        A class representing windows of data on which to perform cross
        validation such as walk forward optimization.

    AcctValue: Inherits from Observer
        Tracks the value of the account.

    AcctStats: Inherits from Analyzer
        Keeps track of important statistics of the account.

Functions
----------
    read_data: DataFrame, datafeed
        Reads data from a CSV file into a pandas DataFrame and creates
        a backtrader pandas data feed.

    walk_forward:
        Executes walk forward optimization on a given strategy and
        dataset.

    optimize:
        Executes optimization on a given strategy and sets of
        parameters. Can be both grid search or random search
        depending on how the parameter set is being
        constructed.

    test_strategy:
        Runs and evaluates a strategy for one set of parameters.

Exceptions
----------
    Exports no exceptions.
"""


import datetime as dt
from copy import deepcopy
from collections import OrderedDict
import math
import pytz

import backtrader as bt
from sklearn.model_selection import TimeSeriesSplit
from sklearn.utils import indexable
from sklearn.utils.validation import _num_samples
import numpy as np
import pandas as pd

class TimeSeriesSplitImproved(TimeSeriesSplit):
    """Time Series cross-validator

    Provides train/test indices to split time series data samples
    that are observed at fixed time intervals, in train/test sets.
    In each split, test indices must be higher than before, and thus
    shuffling in cross validator is inappropriate.
    This cross-validation object is a variation of :class:`KFold`.
    In the kth split, it returns first k folds as train set and the
    (k+1)th fold as test set.
    Note that unlike standard cross-validation methods, successive
    training sets are supersets of those that come before them.
    Read more in the :ref:`User Guide `.

    Source:
    ----------
    https://ntguardian.wordpress.com/2017/06/19/
        walk-forward-analysis-demonstration-backtrader/

    Parameters
    ----------
    n_splits : int, default=3
        Number of splits. Must be at least 1.

    Notes
    -----
    When ``fixed_length`` is ``False``, the training set has size
    ``i * train_splits * n_samples // (n_splits + 1) + n_samples %
    (n_splits + 1)`` in the ``i``th split, with a test set of size
    ``n_samples//(n_splits + 1) * test_splits``, where ``n_samples``
    is the number of samples. If fixed_length is True, replace ``i``
    in the above formulation with 1, and ignore ``n_samples %
    (n_splits + 1)`` except for the first training set. The number
    of test sets is ``n_splits + 2 - train_splits - test_splits``.
    """

    def split(self, X, y=None, groups=None, fixed_length=False,
              train_splits=1, test_splits=1):
        """Generate indices to split data into training and test set.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Training data, where n_samples is the number of samples
            and n_features is the number of features.
        y : array-like, shape (n_samples,)
            Always ignored, exists for compatibility.
        groups : array-like, with shape (n_samples,), optional
            Always ignored, exists for compatibility.
        fixed_length : bool, whether training sets should always have
            common length
        train_splits : positive int, for the minimum number of
            splits to include in training sets
        test_splits : positive int, for the number of splits to
            include in the test set

        Returns
        -------
        train : ndarray
            The training set indices for that split.
        test : ndarray
            The testing set indices for that split.
        """

        X, y, groups = indexable(X, y, groups)
        n_samples = _num_samples(X)
        n_splits = self.n_splits
        n_folds = n_splits + 1
        train_splits, test_splits = int(train_splits), int(test_splits)
        if n_folds > n_samples:
            raise ValueError(
                ("Cannot have number of folds ={0} greater"
                 " than the number of samples: {1}.").format(n_folds,
                                                             n_samples))
        indices = np.arange(n_samples)
        split_size = (n_samples // n_folds)
        test_size = split_size * test_splits
        train_size = split_size * train_splits
        test_starts = range(train_size + n_samples % n_folds,
                            n_samples - (test_size - split_size),
                            split_size)
        if fixed_length:
            for i, test_start in zip(range(len(test_starts)),
                                     test_starts):
                rem = 0
                if i == 0:
                    rem = n_samples % n_folds
                yield (indices[(test_start - train_size - rem):test_start],
                       indices[test_start:test_start + test_size])
        else:
            for test_start in test_starts:
                yield (indices[:test_start],
                       indices[test_start:test_start + test_size])

class AcctValue(bt.Observer):
    '''A simple observer that tracks the account value'''

    alias = ('Value',)
    lines = ('value',)

    plotinfo = {'plot': True, 'subplot' : True}

    def next(self):
        self.lines.value[0] = self._owner.broker.getvalue()

class AcctStats(bt.Analyzer):
    """A simple analyzer that tracks important performance metrics"""

    def __init__(self):
        self.start_val = self.strategy.broker.get_value()
        self.end_val = None

    def stop(self):
        self.end_val = self.strategy.broker.get_value()

    def get_analysis(self):
        return {"start": self.start_val, "end": self.end_val,
                "growth": self.end_val - self.start_val,
                "return": self.end_val / self.start_val}


def read_data(pair: str = 'BTC-USD', timeframe: str = '1D',
              start_date: dt.datetime =
              dt.datetime(
                  2014,12,1,0,0,0,0,dt.timezone(dt.timedelta(hours=0))),
              end_date: dt.datetime = dt.datetime.now(pytz.utc),
              funding: bool = True):
    """Read in data from a CSV file.

    Description
    ----------
    Read data from a CSV file and store it into a pandas DataFrame and a
    backtrader data feed.

    Parameters:
    ----------
    pair: string
        Give the currency pair to be traded.
    timeframe: string
        Give the time frame of the chart to be traded on.
    start_date: datetime.datetime
        Give the date where the data starts.
    end_date: datetime.datetime
        Give the date where the data ends.
    funding: bool
        If funding data is needed, the data has to be restricted to the
        time from which funding data is available.

    Returns:
    ----------
    df: DataFrame
        A pandas DataFrame with the data for further processing.
    data: datafeed
        A backtrader data feed with the data for use with Cerebro

    Raises:
    ----------
    Does not raise any exceptions.
    """

    #exchange = ccxt.ftx()

    #data = exchange.fetch_ohlcv("BTC/USD", '1d')
    #df = pd.DataFrame(data)
    #df.columns = (['Date Time', 'Open', 'High', 'Low', 'Close', 'Volume'])

    #def parse_dates(ts):
    #    return dt.datetime.fromtimestamp(ts/1000.0)

    #df['Date Time'] = df['Date Time'].apply(parse_dates)
    #df = df.set_index('Date Time')

    #data = bt.feeds.PandasData(dataname=df)

    #ydf = web.DataReader(pair, data_source='yahoo',
    #                   start = '2018-01-01', end=datetime.today())

    df = pd.DataFrame()
    if pair == 'BTC-USD':
        df = pd.read_csv('./data/COINBASE_BTCUSD_' + str(timeframe) + '.csv',
                         encoding='utf7')
    elif pair == 'ETH-USD':
        df = pd.read_csv('./data/COINBASE_ETHUSD_' + str(timeframe) + '.csv',
                         encoding='utf7')

    df['time'] = df['time'].apply(pd.to_datetime)
    df = df[df['time'] > start_date]
    df = df[df['time'] < end_date]

    if pair == 'BTC-USD' and funding:
        df = df[df['time'] >
            dt.datetime(2015,9,25,0,0,0,0,dt.timezone(dt.timedelta(hours=0)))]
    elif pair == 'ETH-USD' and funding:
        df = df[df['time'] >
            dt.datetime(2017,8,2,0,0,0,0,dt.timezone(dt.timedelta(hours=0)))]

    df.set_index('time', inplace=True)

    data = bt.feeds.PandasDataFunding(
        dataname=df,
        datetime=None,
        high='high',
        low='low',
        open='open',
        close='close',
        funding='funding'
    )

    return df, data


def walk_forward(strat_name: str, strategy: bt.Strategy,
                 walk_forward_strat: bt.Strategy,
                 windowset: set, split: int = 2, pair: str = 'BTC-USD',
                 cash: int = 100000, timeframe: str = '1D',
                 start_date : dt.datetime =
                 dt.datetime(
                     2014,12,1,0,0,0,0,dt.timezone(dt.timedelta(hours=0))),
                 end_date: dt.datetime = dt.datetime.now(pytz.utc),
                 funding: bool = False, plot: bool = False,
                 save: bool = True):
    """Execute walk forward optimization for cross validation.

    Description
    ----------
    Split the data into several windows to train and test a strategy on
    and apply walk forward optimization on the split data.

    Parameters:
    ----------
    strat_name: string
        Give the name of the strategy to optimize.
    strategy: backtrader.Strategy
        Give the strategy to optimize.
    walk_forward_strat: backtrader.Strategy
        Give the container for a walk forward strategy that can have
        different sets of parameters on different data windows.
    windowset: set
        Give a set of parameter sets for which to optimize the strategy
        on the training data splits.
    split: integer
        Give the number of splits of data to cross validate.
    pair: string
        Give the currency pair to be traded.
    cash: int
        Give the amount of starting capitl.
    timeframe: string
        Give the time frame of the chart to be traded on.
    start_date: datetime.datetime
        Give the date where the data starts.
    end_date:
        Give the date where the data ends.
    funding: bool
        Indicates if funding data should be considered. If funding data
        is needed, the data has to be restricted to the time from which
        funding data is available.
    plot: bool
        Indicate if the result should be plotted or not.
    save: bool
        Indicate if the result should be saved or not.

    Returns:
    ----------
    Does not return anything.

    Raises:
    ----------
    Does not raise any exceptions.
    """

    print('Optimizing: ' + strat_name + '\n')

    df, data = read_data(pair, timeframe, start_date, end_date, funding)

    tscv = TimeSeriesSplitImproved(split)
    split = tscv.split(df, fixed_length=True, train_splits=2)

    walk_forward_results = list()

    for train, test in split:
        # TRAINING
        windows = list(windowset)

        trainer = bt.Cerebro(stdstats=False, maxcpus=1)
        trainer.broker.set_cash(cash)
        trainer.broker.setcommission(0.0007)

        trainer.addanalyzer(AcctStats)
        trainer.addanalyzer(bt.analyzers.SharpeRatio)
        trainer.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')

        tester = deepcopy(trainer)

        trainer.optstrategy(strategy, par_tuple=windows)

        data = bt.feeds.PandasData(dataname=df.iloc[train],

                                    datetime = None,
                                    high = 'high',
                                    low = 'low',
                                    open = 'open',
                                    close = 'close')
        # Add a subset of data to the trainer
        trainer.adddata(data)

        res = trainer.run()
        # Get optimal combination
        opt_res = pd.DataFrame(
            {r[0].params.par_tuple: r[0].analyzers.acctstats.get_analysis()
            for r in res}
            ).T.loc[:, "return"].sort_values(ascending=False).index[0]
        sharpe = pd.DataFrame(
            {r[0].params.par_tuple : r[0].analyzers.sharperatio.get_analysis()
            for r in res}
            ).T.loc[:, "sharperatio"].sort_values(ascending=False).index[0]
        max_dd = pd.DataFrame(
            {res[0][0].params.par_tuple :
                 OrderedDict(res[0][0].analyzers.drawdown.get_analysis().max)}
            ).T.loc[:, 'drawdown'].sort_values(ascending=True).index[0]

        # TESTING
        tester.addstrategy(strategy, par_tuple=max_dd)
        data = bt.feeds.PandasData(dataname=df.iloc[test])
        # Add a subset of data to the tester
        tester.adddata(data)

        res = tester.run()

        res_dict = res[0].analyzers.acctstats.get_analysis()
        res_dict['params'] = max_dd
        res_dict['start_date'] = df.iloc[test[0]].name
        res_dict['end_date'] = df.iloc[test[-1]].name
#        res_dict['sharpe'] = sharpe
        walk_forward_results.append(res_dict)
        print(res_dict)

    wfdf = pd.DataFrame(walk_forward_results)

    cerebro_wf = bt.Cerebro()

    data = bt.feeds.PandasData(
        dataname=df,
        datetime=None,
        high='high',
        low='low',
        open='open',
        close='close'
    )

    cerebro_wf.adddata(data)
    bt.Strategy.lines
    cerebro_wf.broker.getcash
    cerebro_wf.broker.setcash(cash)
    cerebro_wf.broker.setcommission(0.0007)
    cerebro_wf.addstrategy(walk_forward_strat,
                            par_tuple = [tuple(par) for par in wfdf.params],
                            start_dates=[sd.date() for sd in wfdf.start_date],
                            end_dates=[ed.date() for ed in wfdf.end_date])
    cerebro_wf.addobserver(AcctValue)
    cerebro_wf.addobservermulti(bt.observers.BuySell)
    cerebro_wf.addanalyzer(AcctStats)

    res = cerebro_wf.run()
    print(res[0].params.par_tuple)
    print(res[0].analyzers.acctstats.get_analysis())

    if plot:
        cerebro_wf.plot(style='candlestick', volume=False)
    if save:
        fpath = './plots/' + strat_name
        cerebro_wf.saveplots(style='candlestick', volume=False,
                             file_path=fpath)


def optimize(strat_name: str, strategy: bt.Strategy, par_tuples: list,
             pair: str = 'BTC-USD', cash: int = 10000,
             timeframe: str = '1D',
             start_date: dt.datetime = dt.datetime(
                 2014,12,1,0,0,0,0,dt.timezone(dt.timedelta(hours=0))),
             end_date: dt.datetime = dt.datetime.now(pytz.utc),
             funding: bool =False, plot: bool = False, save: bool = False):
    """Optimize a given strategy on a given set of parameter sets.

    Description
    ----------
    Find the set of parameters for which the strategy minimizes draw
    downs while maximizing returns out of a set of parameter sets
    generated as a grid or by random selection.

    Parameters:
    ----------
    strat_name: string
        Give the name of the strategy to optimize.
    strategy: backtrader.Strategy
        Give the strategy to optimize.
    par_tuples: set
        Give a set of parameter sets for which to optimize the strategy
        on the training data.
    pair: string
        Give the currency pair to be traded.
    cash: int
        Give the amount of starting capitl.
    timeframe: string
        Give the time frame of the chart to be traded on.
    start_date: datetime.datetime
        Give the date where the data starts.
    end_date:
        Give the date where the data ends.
    funding: bool
        Indicates if funding data should be considered. If funding data
        is needed, the data has to be restricted to the time from which
        funding data is available.
    plot: bool
        Indicate if the result should be plotted or not.
    save: bool
        Indicate if the result should be saved or not.

    Returns:
    ----------
    Does not return anything.

    Raises:
    ----------
    Does not raise any exceptions.
    """

    print('Optimizing: ' + strat_name + '\n')

    df, data = read_data(pair=pair, timeframe=timeframe,
                         start_date=start_date, end_date=end_date, funding=funding)

    cerebro_opt = bt.Cerebro()
    cerebro_opt.adddata(data)

    cerebro_opt.optstrategy(strategy, par_tuple=par_tuples)

    cerebro_opt.addanalyzer(bt.analyzers.SharpeRatio, _name='mysharpe')
    cerebro_opt.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
    cerebro_opt.addanalyzer(bt.analyzers.AnnualReturn, _name='annual')
    cerebro_opt.addanalyzer(bt.analyzers.TradeAnalyzer, _name='mytrade')

    cerebro_opt.broker.setcash(cash)
    cerebro_opt.broker.setcommission(commission=0.0007)

    thestrats = cerebro_opt.run()

    num_trades = []
    sharpe = []
    win_rate = []
    max_dd = []
    pnl = []
    for thestrat in thestrats:
        try:
            pnl.append(
                thestrat[0].analyzers.mytrade.get_analysis()['pnl']['net']['total'])
        except:
            pnl.append(0)
        try:
            num_trades.append(
                thestrat[0].analyzers.mytrade.get_analysis()['total']['total'])
        except:
            num_trades.append(0)
        try:
            win_rate.append(
                thestrat[0].analyzers.mytrade.get_analysis()['won']['total'] /
                thestrat[0].analyzers.mytrade.get_analysis()['total']['total'])
        except:
            win_rate.append(0)
        try:
            sharpe.append(
                thestrat[0].analyzers.mysharpe.get_analysis()['sharperatio'])
        except:
            sharpe.append(0)
        try:
            max_dd.append(
                thestrat[0].analyzers.drawdown.get_analysis().max.drawdown)
        except:
            max_dd.append(0)

    analysis = pd.DataFrame({'# trades' : num_trades,
                            'win rate' : win_rate,
                            'sharpe' : sharpe,
                            'max DD' : max_dd,
                            'pnl' : pnl},
                            index=pd.MultiIndex.from_tuples(par_tuples))

    analysis = analysis[analysis['# trades'] > 1]
    analysis = analysis[analysis['sharpe'].notna()]
    analysis = analysis[analysis['pnl'] >= 1000]
    analysis = analysis[analysis['sharpe'] >= 0.1]
    analysis = analysis.sort_values(by='max DD', ascending=True)[0:math.floor(len(analysis*0.05))]
    analysis.sort_values(by='sharpe', ascending=False, inplace=True)
    analysis.sort_values(by='pnl', ascending=False, inplace=True)

    print(analysis.head().to_markdown())

    cerebro_test = bt.Cerebro()
    cerebro_test.adddata(data)
#    cerebro_test.broker.set_fundmode(True, cash)
    cerebro_test.broker.setcash(cash)
    cerebro_test.broker.setcommission(commission=0.0007)
    cerebro_test.addanalyzer(AcctStats)

    opt_res = analysis.index[0]
    cerebro_test.addstrategy(strategy, par_tuple = opt_res)

    cerebro_test.run()

    if plot:
        cerebro_test.plot(style='candlestick', volume=False)
    if save:
        fpath = './plots/' + strat_name
        cerebro_test.saveplots(style='candlestick', volume=False, file_path=fpath)


def test_strategy(strat_name: str, strategy: bt.Strategy, par_tuple,
                  pair: str = 'BTC-USD', timeframe: str = '1D',
                  cash: int = 10000,
                  start_date: dt.datetime = dt.datetime(
                     2014,12,1,0,0,0,0,dt.timezone(dt.timedelta(hours=0))),
                  end_date: dt.datetime = dt.datetime.now(pytz.utc),
                  funding: bool = False, plot: bool = False,
                  save: bool = False):
    """Test and visualize a strategy for a given parameter set."""

    df, data = read_data(pair, timeframe, start_date, end_date, funding)

    cerebro = bt.Cerebro()

    cerebro.addstrategy(strategy, par_tuple=par_tuple)
    cerebro.adddata(data)

    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='mysharpe')
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
    cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name='annual')
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='mytrade')

    cerebro.broker.setcash(cash)
    cerebro.broker.setcommission(commission=0.0007)

    thestrats = cerebro.run()

    thestrat = thestrats[0]

    sharpe = thestrat.analyzers.mysharpe.get_analysis()['sharperatio']
    max_dd = thestrat.analyzers.drawdown.get_analysis().max.drawdown
    num_trades = thestrat.analyzers.mytrade.get_analysis()['total']['total']
    win_rate = thestrat.analyzers.mytrade.get_analysis()['won']['total'] / \
               thestrat.analyzers.mytrade.get_analysis()['total']['total']
    pnl = thestrat.analyzers.mytrade.get_analysis()['pnl']['net']['total']

    stats = pd.DataFrame({'#trades' : num_trades,
                          'win rate' : win_rate,
                          'sharpe' : sharpe,
                          'max DD' : max_dd,
                          'pnl' : pnl},
                          index=pd.MultiIndex.from_tuples((par_tuple,)))

    print(stats.to_markdown())

    if plot:
        cerebro.plot(style='candlestick', volume=False)
    if save:
        fpath = './plots/' + strat_name
        cerebro.saveplots(style='candlestick', volume=False, file_path=fpath)