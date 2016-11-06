from __future__ import absolute_import, unicode_literals
from celery import Celery
from celery.schedules import crontab


app = Celery('celery',
             broker='amqp://guest@localhost//',
             include=['task.mongodb', 'task.camera'])

app.conf.timezone = 'Europe/Minsk'

app.conf.beat_schedule = {
    'mongo-1-min': {
        'task': 'task.mongodb.insert_all_conditions',
        'schedule': crontab(minute='*/10')
    },
}

if __name__ == '__main__':
    app.start()
