#! /bin/bash

case "$1" in
  start)
    echo "Starting services"
    # Start daemons
    PYTHONPATH= python tasks/sensors_mqtt_dmn.py start
    PYTHONPATH= python tasks/fans_mqtt_dmn.py start
    PYTHONPATH= python tasks/lights_mqtt_dmn.py start
    PYTHONPATH= python tasks/pumps_mqtt_dmn.py start
    ;;
  stop)
    echo "Stopping services"
    # Stop the daemon
    PYTHONPATH= python tasks/sensors_mqtt_dmn.py stop
    PYTHONPATH= python tasks/fans_mqtt_dmn.py stop
    PYTHONPATH= python tasks/lights_mqtt_dmn.py stop
    PYTHONPATH= python tasks/pumps_mqtt_dmn.py stop
    ;;
  restart)
    echo "Restarting services"
    PYTHONPATH= python tasks/sensors_mqtt_dmn.py restart
    PYTHONPATH= python tasks/fans_mqtt_dmn.py restart
    PYTHONPATH= python tasks/lights_mqtt_dmn.py restart
    PYTHONPATH= python tasks/pumps_mqtt_dmn.py restart
    ;;
  *)
    # Refuse to do other stuff
    echo "Usage: ./greenhouse.sh {start|stop|restart}"
    exit 1
    ;;
esac

exit 0
