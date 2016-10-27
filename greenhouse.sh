#! /bin/bash

case "$1" in
  start)
    echo "Starting services"
    # Start the daemon
    PYTHONPATH= python tasks/sens.py start
    ;;
  stop)
    echo "Stopping services"
    # Stop the daemon
    PYTHONPATH= python tasks/sens.py stop
    ;;
  restart)
    echo "Restarting services"
    PYTHONPATH= python tasks/sens.py restart
    ;;
  *)
    # Refuse to do other stuff
    echo "Usage: ./greenhouse.sh {start|stop|restart}"
    exit 1
    ;;
esac

exit 0
