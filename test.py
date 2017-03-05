#!/usr/bin/env python
# -*- coding: utf-8 -*-

from modules.greenhouse.objects import Lifecycle
from web_interface.web_events.config_requests import CreateLifecycle, Timer, Conditions
from datetime import datetime


T = Timer({
    'start_time': datetime(2017, 3, 5, 10, 0, 0),
    'end_time': datetime(2017, 3, 5, 22, 00, 0),
    # 'start_date': datetime(2017, 3, 3, 0, 0, 0),
    # 'end_date': datetime(2017, 3, 4, 0, 0, 0),
})
C = Conditions({'min_value': 30, 'max_value': 70})

data = {
    'by_time': True,
    'type': 'light',
    'timer': T,
    # 'conditions': C
    }


if __name__ == '__main__':
    lc = CreateLifecycle(data)
    Lifecycle.create(**lc)
