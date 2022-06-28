"""Implements custom basic operations not included in backtrader.

Description
----------
Collects custom made basic operations indicators that are not included
in the native backtrader package but that are usefull or necessary for
my own trading strategies.

Classes
----------
BackwardDifferenceQuotient: Inherits from PeriodN
    A Class representing an indicator that takes the backward finite
    difference of the passed data series at a specified interval.

Functions
----------
    Implements no module functions.

Exceptions
----------
    Exports no exceptions.
"""

from backtrader.indicators import PeriodN

class BackwardDifferenceQuotient(PeriodN):
    """The difference quotient is used for approximation of derivatives.

    Description
    ----------
    Taken to the limit it gives the derivative of a function.

    Attributes
    ----------
    line : Line Object
        A line object that can be plotted on the chart.

    Methods
    ----------
    next(self)
        Implements the next method called on every price candle.
    """

    alias = ('BackwardFiniteDifference',)
    lines = ('bdq',)

    def next(self):
        """Calculate the difference quotient for this price candle.

        Description
        ----------
        Formula:
          - back_diff_q = (f(x) - f(x-h))/h
        for a given function f.
        See also:
          - https://en.wikipedia.org/wiki/Difference_quotient

        Parameters:
        ----------
        Gets no parameters.

        Returns:
        ----------
        Retruns no value.

        Raises:
        ----------
        Does not raise any exceptions.
        """

        self.line[0] = (self.data[0] - self.data[self.p.period]) \
                       / (self.data[0] * self.p.period)

    def once(self, start, end):
        src = self.data.array
        dst = self.line.array
        period = self.p.period

        for i in range(start, end):
            dst[i] = (self.data[i+1] - self.data[i - period + 1]) \
                     / (self.data[0] * period)