import random
import datetime as dt

import parameters
import optimizer
import strategies
import strategies_walk_forward

windowset_smac = set()  # Use a set to avoid duplicates
while len(windowset_smac) < 2500:
    f = random.randint(1, 100)
    s = random.randint(1, 200)
    # Cannot have the fast ma have a longer window than the slow -> swap
    if f > s:
        f, s = s, f
    elif f == s:  # Cannot be equal, so do nothing, discarding results
        continue
    windowset_smac.add((f, s))

windowset_arstc = set()  # Use a set to avoid duplicates
while len(windowset_arstc) < 2500:
    f = random.randint(1, 50) * 2
    s = random.randint(1, 100) * 2
    c = random.randint(1,3) * 5
    d1 = random.randint(1,3) * 2
    d2 = random.randint(1,3) * 2
#    lstc = random.randint(1,2) * 10
#    hstc = random.randint(7,8) * 10
    ar = random.randint(1,3) * 5
    # Cannot have the fast ma have a longer window than the slow -> swap
    if f > s:
        f, s = s, f
    elif f == s:  # Cannot be equal, so do nothing, discarding results
        continue
    windowset_arstc.add((f, s, c, d1, d2, 25, 75, ar,))

windowset_stcsma = set()  # Use a set to avoid duplicates
while len(windowset_stcsma) < 2500:
    f = random.randint(1, 50) * 2
    s = random.randint(1, 100) * 2
    c = random.randint(1,3) * 5
    d1 = random.randint(1,3) * 2
    d2 = random.randint(1,3) * 2
#    lstc = random.randint(1,2) * 10
#    hstc = random.randint(7,8) * 10
    sma = random.randint(1,15) * 10
    # Cannot have the fast ma have a longer window than the slow -> swap
    if f > s:
        f, s = s, f
    elif f == s:  # Cannot be equal, so do nothing, discarding results
        continue
    windowset_stcsma.add((f, s, c, d1, d2, 25, 75, 95,))

windowset_stcvol = set()  # Use a set to avoid duplicates
while len(windowset_stcvol) < 2500:
    f = random.randint(1, 50) * 2
    s = random.randint(1, 100) * 2
    c = random.randint(1,3) * 5
    d1 = random.randint(1,3) * 2
    d2 = random.randint(1,3) * 2
#    lstc = random.randint(1,2) * 10
#    hstc = random.randint(7,8) * 10
    vol = random.randint(1,5) * 3
#    volup = random.randint(4,11) * 10
#    voldown = random.randint(8,15) * 10
    # Cannot have the fast ma have a longer window than the slow -> swap
    if f > s:
        f, s = s, f
    elif f == s:  # Cannot be equal, so do nothing, discarding results
        continue
    windowset_stcvol.add((f, s, c, d1, d2, 25, 75, 10, 90, 120,))

#par_tuple = (6, 2, 4, 15, 20, 18, 15, 15,)
windowset_drsidma = set()  # Use a set to avoid duplicates
while len(windowset_drsidma) < 2500:
    lma = random.randint(1, 20) * 1
    ldma = random.randint(1, 20) * 1
    sma = random.randint(1,5) * 1
    lmom = random.randint(1,10) * 2
    ldmom = random.randint(1,10) * 2
    smom = random.randint(1,10) * 2
    uth = random.randint(1,10) * 0.0005
    lth = random.randint(1,10) * 0.0005

    windowset_drsidma.add((lma, ldma, sma, lmom, ldmom, smom, uth, lth,))

"""
Random Search Parameter Optimization
"""

def random_search_optimization():
    optimizer.optimize('SMAC_BTC_1D', strategies.SMAC, windowset_smac,
                       'BTC-USD', 100000, '1D', dt.datetime(
                       2018,1,1,0,0,0,0,dt.timezone(dt.timedelta(hours=0))),
                       funding=False, plot=True, save=True)
    optimizer.optimize('SMAC_BTC_8H', strategies.SMAC, windowset_smac,
                       'BTC-USD', 100000, '8H',  dt.datetime(
                       2020,1,1,0,0,0,0,dt.timezone(dt.timedelta(hours=0))),
                       funding=False, plot=True, save=True)


    optimizer.optimize('SMAC_ETH_1D', strategies.SMAC, windowset_smac,
                       'ETH-USD', 10000, '1D',  dt.datetime(
                       2018,1,1,0,0,0,0,dt.timezone(dt.timedelta(hours=0))),
                       funding=False, plot=True, save=True)
    optimizer.optimize('SMAC_ETH_8H', strategies.SMAC, windowset_smac,
                       'ETH-USD', 10000, '8H',  dt.datetime(
                       2020,1,1,0,0,0,0,dt.timezone(dt.timedelta(hours=0))),
                       funding=False, plot=True, save=True)

    optimizer.optimize('AROON_STC_BTC_1D', strategies.AroonStc,
                       windowset_arstc, 'BTC-USD', 100000, '1D',
                       dt.datetime(
                           2018, 1, 1, 0, 0, 0, 0, dt.timezone(dt.timedelta(hours=0))),
                       funding=False, plot=True, save=True)
    optimizer.optimize('AROON_STC_BTC_8H', strategies.AroonStc,
                       windowset_arstc, 'BTC-USD', 100000, '8H',
                       dt.datetime(
                           2020, 1, 1, 0, 0, 0, 0, dt.timezone(dt.timedelta(hours=0))),
                       funding=False, plot=True, save=True)

    optimizer.optimize('AROON_STC_ETH_1D', strategies.AroonStc,
                       windowset_arstc, 'ETH-USD', 10000, '1D',
                       dt.datetime(
                           2018, 1, 1, 0, 0, 0, 0, dt.timezone(dt.timedelta(hours=0))),
                       funding=False, plot=True, save=True)
    optimizer.optimize('AROON_STC_ETH_8H', strategies.AroonStc,
                       windowset_arstc, 'ETH-USD', 10000, '8H',
                       dt.datetime(
                           2020, 1, 1, 0, 0, 0, 0, dt.timezone(dt.timedelta(hours=0))),
                       funding=False, plot=True, save=True)

    optimizer.optimize('STC_SMA_Short_BTC_1D', strategies.StcSmaShort,
                       windowset_stcsma, 'BTC-USD', 100000, '1D',
                       dt.datetime(
                           2018, 1, 1, 0, 0, 0, 0, dt.timezone(dt.timedelta(hours=0))),
                       funding=False, plot=True, save=True)
    optimizer.optimize('STC_SMA_Short_BTC_8H', strategies.StcSmaShort,
                       windowset_stcsma, 'BTC-USD', 100000, '8H',
                       dt.datetime(
                           2020, 1, 1, 0, 0, 0, 0, dt.timezone(dt.timedelta(hours=0))),
                       funding=False, plot=True, save=True)
    optimizer.optimize('STC_SMA_Short_ETH_8H', strategies.StcSmaShort,
                       windowset_stcsma, 'ETH-USD', 10000, '8H',
                       dt.datetime(
                           2020, 1, 1, 0, 0, 0, 0, dt.timezone(dt.timedelta(hours=0))),
                       funding=False, plot=True, save=True)
    optimizer.optimize('STC_Vol_BTC_1D', strategies.StcVol, windowset_stcvol,
                       'BTC-USD', 100000, '1D',  dt.datetime(
                       2018,1,1,0,0,0,0,dt.timezone(dt.timedelta(hours=0))),
                       funding=False, plot=True,
                       save=True)


    optimizer.optimize('STC_Vol_ETH_1D', strategies.StcVol, windowset_stcvol,
                       'ETH-USD', 10000, '1D',  dt.datetime(
                       2018,1,1,0,0,0,0,dt.timezone(dt.timedelta(hours=0))),
                       funding=False, plot=True,
                       save=True)
    optimizer.optimize('DRSIDMALong_ETH_1D', strategies.DRSIDMALong,
                       windowset_drsidma, 'ETH-USD', 10000,
                       '1D',  dt.datetime(
                       2018,1,1,0,0,0,0,dt.timezone(dt.timedelta(hours=0))),
                       funding=True, plot=True, save=True)
    optimizer.optimize('DRSIDMAShort_ETH_1D', strategies.DRSIDMAShort,
                       windowset_drsidma, 'ETH-USD', 10000,
                       '1D',  dt.datetime(
                       2018,1,1,0,0,0,0,dt.timezone(dt.timedelta(hours=0))),
                       funding=True, plot=True, save=True)
    optimizer.optimize('DRSIDMALong_BTC_8H', strategies.DRSIDMALong,
                       windowset_drsidma, 'BTC-USD', 100000, '8H',
                       dt.datetime(
                           2020, 1, 1, 0, 0, 0, 0, dt.timezone(dt.timedelta(hours=0))),
                       funding=True, plot=True, save=True)
    optimizer.optimize('DRSIDMALong_ETH_8H', strategies.DRSIDMALong,
                       windowset_drsidma, 'ETH-USD', 10000,
                       '8H',  dt.datetime(
                       2020,1,1,0,0,0,0,dt.timezone(dt.timedelta(hours=0))),
                       funding=True, plot=True, save=True)
    optimizer.optimize('DRSIDMAShort_BTC_1D', strategies.DRSIDMAShort,
                       windowset_drsidma, 'BTC-USD', 100000, '1D',
                       dt.datetime(
                           2018, 1, 2, 0, 0, 0, 0, dt.timezone(dt.timedelta(hours=0))),
                       funding=True, plot=True, save=True)
    optimizer.optimize('DRSIDMALong_BTC_1D', strategies.DRSIDMALong,
                       windowset_drsidma, 'BTC-USD', 100000, '1D',
                       dt.datetime(
                           2018,1,2,0,0,0,0, dt.timezone(dt.timedelta(hours=0))),
                       funding=True, plot=True, save=True)
    optimizer.optimize('STC_Vol_BTC_8H', strategies.StcVol, windowset_stcvol,
                       'BTC-USD', 100000, '8H',  dt.datetime(
                       2020,1,2,0,0,0,0,dt.timezone(dt.timedelta(hours=0))),
                       funding=False, plot=True,
                       save=True)
    optimizer.optimize('DRSIDMAShort_BTC_8H', strategies.DRSIDMAShort,
                       windowset_drsidma, 'BTC-USD', 100000, '8H',
                       dt.datetime(
                           2020, 1, 1, 0, 0, 0, 0, dt.timezone(dt.timedelta(hours=0))),
                       funding=True, plot=True, save=True)
    optimizer.optimize('STC_Vol_ETH_8H', strategies.StcVol, windowset_stcvol,
                       'ETH-USD', 10000, '8H',  dt.datetime(
                       2020,1,1,0,0,0,0,dt.timezone(dt.timedelta(hours=0))),
                       funding=False, plot=True,
                       save=True)
    optimizer.optimize('DRSIDMAShort_ETH_8H', strategies.DRSIDMAShort,
                       windowset_drsidma, 'ETH-USD', 10000,
                       '8H',  dt.datetime(
                       2020,1,1,0,0,0,0,dt.timezone(dt.timedelta(hours=0))),
                       funding=True, plot=True, save=True)
    optimizer.optimize('STC_SMA_Short_ETH_1D', strategies.StcSmaShort,
                       windowset_stcsma, 'ETH-USD', 10000, '1D',
                       dt.datetime(
                           2018, 1, 1, 0, 0, 0, 0, dt.timezone(dt.timedelta(hours=0))),
                       funding=False, plot=True, save=True)

"""
Walk Forward Optimization
"""

def walk_forward_optimization():


    optimizer.walk_forward('SMAC_BTC_8H', strategies.SMAC,
                           strategies_walk_forward.SMACWalkForward,
                           windowset_smac, 2, pair = 'BTC-USD', cash=100000,
                           timeframe='8H')
    optimizer.walk_forward('SMAC_BTC_1D', strategies.SMAC,
                           strategies_walk_forward.SMACWalkForward,
                           windowset_smac, 2, pair = 'BTC-USD', cash=100000,
                           timeframe='1D')

    optimizer.walk_forward('SMAC_ETH_8H', strategies.SMAC,
                           strategies_walk_forward.SMACWalkForward,
                           windowset_smac, 2, pair = 'ETH-USD', cash=10000,
                           timeframe='8H')
    optimizer.walk_forward('SMAC_ETH_1D', strategies.SMAC,
                           strategies_walk_forward.SMACWalkForward,
                           windowset_smac, 2, pair = 'ETH-USD', cash=10000,
                           timeframe='1D')

    optimizer.walk_forward('AROON_STC_BTC_8H', strategies.AroonStc,
                           strategies_walk_forward.AroonSTCWalkForward,
                           windowset_arstc, 2, pair = 'BTC-USD', cash=100000,
                           timeframe='8H')
    optimizer.walk_forward('AROON_STC_BTC_1D', strategies.AroonStc,
                           strategies_walk_forward.AroonSTCWalkForward,
                           windowset_arstc, 2, pair = 'BTC-USD', cash=100000,
                           timeframe='1D')

    optimizer.walk_forward('AROON_STC_ETH_8H', strategies.AroonStc,
                           strategies_walk_forward.AroonSTCWalkForward,
                           windowset_arstc, 2, pair = 'ETH-USD', cash=10000,
                           timeframe='8H')
    optimizer.walk_forward('AROON_STC_ETH_1D', strategies.AroonStc,
                           strategies_walk_forward.AroonSTCWalkForward,
                           windowset_arstc, 2, pair = 'ETH-USD', cash=10000,
                           timeframe='1D')

    optimizer.walk_forward('STC_SMA_Short_BTC_8H', strategies.StcSmaShort,
                           strategies_walk_forward.StcSmaWalkForward,
                           windowset_stcsma, 2, pair = 'BTC-USD', cash=100000,
                           timeframe='8H')
    optimizer.walk_forward('STC_SMA_Short_BTC_1D', strategies.StcSmaShort,
                           strategies_walk_forward.StcSmaWalkForward,
                           windowset_stcsma, 2, pair = 'BTC-USD', cash=100000,
                           timeframe='1D')

    optimizer.walk_forward('STC_SMA_Short_ETH_8H', strategies.StcSmaShort,
                           strategies_walk_forward.StcSmaWalkForward,
                           windowset_stcsma, 2, pair = 'ETH-USD', cash=10000,
                           timeframe='8H')
    optimizer.walk_forward('STC_SMA_Short_ETH_1D', strategies.StcSmaShort,
                           strategies_walk_forward.StcSmaWalkForward,
                           windowset_stcsma, 2, pair = 'ETH-USD', cash=10000,
                           timeframe='1D')

    optimizer.walk_forward('STC Vol BTC 8H', strategies.StcVol,
                           strategies_walk_forward.StcVolWalkForward,
                           windowset_stcvol, 2, pair = 'BTC-USD', cash=100000,
                           timeframe='8H')
    optimizer.walk_forward('STC_Vol_BTC_1D', strategies.StcVol,
                           strategies_walk_forward.StcVolWalkForward,
                           windowset_stcvol, 2, pair = 'BTC-USD', cash=100000,
                           timeframe='1D')

    optimizer.walk_forward('STC_Vol_ETH_8H', strategies.StcVol,
                           strategies_walk_forward.StcVolWalkForward,
                           windowset_stcvol, 2, pair = 'ETH-USD', cash=10000,
                           timeframe='8H')
    optimizer.walk_forward('STC_Vol_ETH_1D', strategies.StcVol,
                           strategies_walk_forward.StcVolWalkForward,
                           windowset_stcvol, 2, pair = 'ETH-USD', cash=10000,
                           timeframe='1D')


def test_strategies():

    par_smac_btc_1d = parameters.get_smac_1d()
    optimizer.test_strategy('SMAC_BTC_1D', strategies.SMAC, par_smac_btc_1d,
                            'BTC-USD', '1D', 100000, plot=True, save=True)
    par_smac_btc_8h = parameters.get_smac_8h()
    optimizer.test_strategy('SMAC_BTC_1D', strategies.SMAC, par_smac_btc_8h,
                            'BTC-USD', '8H', 100000, plot=True, save=True)

    par_smac_eth_1d = parameters.get_smac_1d()
    optimizer.test_strategy('SMAC_ETH_1D', strategies.SMAC, par_smac_eth_1d,
                            'ETH-USD', '1D', 10000, plot=True, save=True)
    par_smac_eth_8h = parameters.get_smac_8h()
    optimizer.test_strategy('SMAC_ETH_8H', strategies.SMAC, par_smac_eth_8h,
                            'ETH-USD', '8H', 10000, plot=True, save=True)

    par_arstc_btc_1d = parameters.get_aroonStc_BTC_1d()
    optimizer.test_strategy('AROON_STC_BTC_1D', strategies.AroonStc,
                            par_arstc_btc_1d, 'BTC-USD', '1D', 100000,
                            plot=True, save=True)
    par_arstc_btc_8h = parameters.get_aroonStc_BTC_8h()
    optimizer.test_strategy('AROON_STC_BTC_8H', strategies.AroonStc,
                            par_arstc_btc_8h, 'BTC-USD', '8H', 100000,
                            plot=True, save=True)

    par_arstc_eth_1d = parameters.get_aroonStc_ETH_1d()
    optimizer.test_strategy('AROON_STC_ETH_1D', strategies.AroonStc,
                            par_arstc_eth_1d, 'ETH-USD', '1D', 10000,
                            plot=True, save=True)
    par_arstc_eth_8h = parameters.get_aroonStc_ETH_8h()
    optimizer.test_strategy('AROON_STC_ETH_8H', strategies.AroonStc,
                            par_arstc_eth_8h, 'ETH-USD', '8H', 10000,
                            plot=True, save=True)

    par_stcsma_btc_1d = parameters.get_stcSmaShort_BTC_1d()
    optimizer.test_strategy('STC_SMA_Short_BTC_1D', strategies.StcSmaShort,
                            par_stcsma_btc_1d, 'BTC-USD', '1D', 100000,
                            plot=True, save=True)
    par_stcsma_btc_8h = parameters.get_stcSmaShort_BTC_8h()
    optimizer.test_strategy('STC_SMA_Short_BTC_8H', strategies.StcSmaShort,
                            par_stcsma_btc_8h, 'BTC-USD', '8H', 100000,
                            plot=True, save=True)

    par_stcsma_eth_1d = parameters.get_stcSmaShort_ETH_1d()
    optimizer.test_strategy('STC_SMA_ETH_Short_1D', strategies.StcSmaShort,
                            par_stcsma_eth_1d, 'ETH-USD', '1D', 10000,
                            plot=True, save=True)
    par_stcsma_eth_8h = parameters.get_stcSmaShort_ETH_8h()
    optimizer.test_strategy('STC_SMA_Short_ETH_8H', strategies.StcSmaShort,
                            par_stcsma_eth_8h, 'ETH-USD', '8H', 10000,
                            plot=True, save=True)

    par_stcvol_btc_1d = parameters.get_stcVol_BTC_1d()
    optimizer.test_strategy('STC_Vol_BTC_1D', strategies.StcVol,
                            par_stcvol_btc_1d, 'BTC-USD', '1D', 100000,
                            plot=True, save=True)
    par_stcvol_btc_8h = parameters.get_stcVol_BTC_8h()
    optimizer.test_strategy('STC_Vol_BTC_8H', strategies.StcVol,
                            par_stcvol_btc_8h, 'BTC-USD', '8H', 100000,
                            plot=True, save=True)

    par_stcvol_eth_1d = parameters.get_stcVol_ETH_1d()
    optimizer.test_strategy('STC_Vol_ETH_1D', strategies.StcVol,
                            par_stcvol_eth_1d, 'ETH-USD', '1D', 10000,
                            plot=True, save=True)
    par_stcvol_eth_8h = parameters.get_stcVol_ETH_8h()
    optimizer.test_strategy('STC_Vol_ETH_8H', strategies.StcVol,
                            par_stcvol_eth_8h, 'ETH-USD', '8H', 10000,
                            plot=True, save=True)

    par_drsidma_btc_1d = parameters.get_drsidma_BTC_1d()
    optimizer.test_strategy('DRSIDMALong_BTC_1D', strategies.DRSIDMALong,
                            par_drsidma_btc_1d, 'BTC-USD', '1D', 100000,
                            plot=True, save=True)
    par_drsidma_btc_8h = parameters.get_drsidma_BTC_8h()
    optimizer.test_strategy('DRSIDMALong_BTC_8H', strategies.DRSIDMALong,
                            par_drsidma_btc_8h, 'BTC-USD', '8H', 100000,
                            plot=True, save=True)

    par_drsidma_eth_1d = parameters.get_drsidma_ETH_1d()
    optimizer.test_strategy('DRSIDMALong_ETH_1D', strategies.DRSIDMALong,
                            par_drsidma_eth_1d, 'ETH-USD', '1D', 10000,
                            plot=True, save=True)
    par_drsidma_eth_8h = parameters.get_drsidma_ETH_8h()
    optimizer.test_strategy('DRSIDMALong_ETH_8H', strategies.DRSIDMALong,
                            par_drsidma_eth_8h, 'BTC-USD', '8H', 10000,
                            plot=True, save=True)

    par_drsidma_btc_1d = parameters.get_drsidma_BTC_1d()
    optimizer.test_strategy('DRSIDMAShort_BTC_1D', strategies.DRSIDMAShort,
                            par_drsidma_btc_1d, 'BTC-USD', '1D', 100000,
                            plot=True, save=True)
    par_drsidma_btc_8h = parameters.get_drsidma_BTC_8h()
    optimizer.test_strategy('DRSIDMAShort_BTC_8H', strategies.DRSIDMAShort,
                            par_drsidma_btc_8h, 'BTC-USD', '8H', 100000,
                            plot=True, save=True)

    par_drsidma_eth_1d = parameters.get_drsidma_ETH_1d()
    optimizer.test_strategy('DRSIDMAShort_ETH_1D', strategies.DRSIDMAShort,
                            par_drsidma_eth_1d, 'ETH-USD', '1D', 10000,
                            plot=True, save=True)
    par_drsidma_eth_8h = parameters.get_drsidma_ETH_8h()
    optimizer.test_strategy('DRSIDMAShort_ETH_8H', strategies.DRSIDMAShort,
                            par_drsidma_eth_8h, 'BTC-USD', '8H', 10000,
                            plot=True, save=True)

random_search_optimization()


#optimizer.optimize('DRSIDMA_BTC_8H', strategies.DRSIDMA,
#                    windowset_drsidma, 'BTC-USD', 100000, '8H',
#                    funding=False, plot=False, save=True)

#optimizer.optimize('DRSIDMA_BTC_8H', strategies.DRSIDMALong,
#                   windowset_drsidma, 'BTC-USD', 100000,
#                   '8H',  dt.datetime(
#                       2018,12,30,0,0,0,0,dt.timezone(dt.timedelta(hours=0))),
#                   dt.datetime(
#                       2022,12,1,0,0,0,0,dt.timezone(dt.timedelta(hours=0))),
#                   funding=True, plot=True, save=True)
