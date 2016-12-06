#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import yaml

base_dir = os.path.join(os.path.dirname(__file__), '..')


class Config(object):

    temp_dir = os.path.join(base_dir, 'tmp')
    log_dir = os.path.join(base_dir, 'logs')

    def __init__(self, conf):
        self._data = conf

    def __getattr__(self, item):
        try:
            return self._data[item]
        except KeyError:
            raise AttributeError('Config has not {0} attribute.'.format(str(item)))


stage_name = os.getenv('GH_STAGE')

if not stage_name:
    raise Exception('GH_STAGE environment wasn\'t set.')

relative_path = '{0}.yaml'.format(os.path.join('stages', stage_name))
abs_path = os.path.join(base_dir, relative_path)


with open(abs_path, 'r') as fh:
    data = yaml.load(fh)


config = Config(data)
