#!/usr/bin/python
# all mesurment logics here


class BaseSensor(object):

    @classmethod
    def set_up(cls):
        pass

    @classmethod
    def tear_down(cls):
        raise NotImplementedError

    @classmethod
    def do_measure(cls):
        pass

