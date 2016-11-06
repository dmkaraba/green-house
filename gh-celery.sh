#! /bin/bash

case "$1" in
  w-start)
    echo "Starting celery worker"
    celery multi start w1 -A task \
                --pidfile="$HOME/dev/green-house/logs/celery/%n.pid" \
                --logfile="$HOME/dev/green-house/logs/celery/%n%I.log"
    ;;
  w-restart)
    echo "Restarting celery worker"
    celery multi restart w1 -A task \
                --pidfile="$HOME/dev/green-house/logs/celery/%n.pid" \
                --logfile="$HOME/dev/green-house/logs/celery/%n%I.log"
    ;;
  w-stop)
    echo "Stoping celery worker"
    celery multi stopwait w1 --pidfile="$HOME/dev/green-house/logs/celery/%n.pid"
    ;;
  b-start)
    echo "Starting celery beat"
    celery -A task beat -s $HOME/dev/green-house/logs/celery/celerybeat-schedule \
                --pidfile="$HOME/dev/green-house/logs/celery/celerybeat.pid" --detach
    ;;
  b-stop)
    echo "Stoping celery beat"
    kill `cat $HOME/dev/green-house/logs/celery/celerybeat.pid`
    ;;
  *)
    # Refuse to do other stuff
    echo "Usage: ./sh-celery.sh {w-start|w-restart|w-stop|b-start|b-stop}"
    exit 1
    ;;
esac

exit 0