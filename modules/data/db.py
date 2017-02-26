#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mongoengine import *
from config import config
from modules.data.connections import mongo_connection


class DBSharedProperty(object):

    def __init__(self, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.model[self.name]

    def __set__(self, obj, value):
        obj.model[self.name] = value


class DBQuerySet(QuerySet):

    def get(self, *q_objs, **query):
        return super(QuerySet, self).get(*q_objs, **query)

    def with_id(self, object_id):
        return super(QuerySet, self).with_id(object_id)


class DBDocument(Document):

    meta = {
        'abstract': True,
        'queryset_class': DBQuerySet,
    }

    @classmethod
    def _get_db(cls):
        return mongo_connection[config.mongodb['db_name']]
