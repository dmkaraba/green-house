#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import date, time


class DateComparison(date):
    """
    Additional logic to compare <datetime> with <str>
    """

    def __ge__(self, y):
        if not y:
            return False
        return date.today() >= y

    def __le__(self, y):
        if not y:
            return False
        return date.today() <= y

    def __gt__(self, y):
        if not y:
            return False
        return date.today() > y

    def __lt__(self, y):
        if not y:
            return False
        return date.today() < y

    def __eq__(self, y):
        if not y:
            return False
        return date.today() == y


class TimeComparison(time):
    def __ge__(self, y):
        if not y:
            return False
        return time(self.hour, self.minute) >= y

    def __le__(self, y):
        if not y:
            return False
        return time(self.hour, self.minute) <= y

    def __gt__(self, y):
        if not y:
            return False
        return time(self.hour, self.minute) > y

    def __lt__(self, y):
        if not y:
            return False
        return time(self.hour, self.minute) < y

    def __eq__(self, y):
        if not y:
            return False
        return time(self.hour, self.minute) == y
