#! /bin/bash

case "$1" in
  start)
    echo "Starting services"
    # Start daemons
    PYTHONPATH= python task/sensors_mqtt_dmn.py start
    PYTHONPATH= python task/fans_mqtt_dmn.py start
    PYTHONPATH= python task/lights_mqtt_dmn.py start
    PYTHONPATH= python task/pumps_mqtt_dmn.py start
    ;;
  stop)
    echo "Stopping services"
    # Stop the daemon
    PYTHONPATH= python task/sensors_mqtt_dmn.py stop
    PYTHONPATH= python task/fans_mqtt_dmn.py stop
    PYTHONPATH= python task/lights_mqtt_dmn.py stop
    PYTHONPATH= python task/pumps_mqtt_dmn.py stop
    ;;
  restart)
    echo "Restarting services"
    PYTHONPATH= python task/sensors_mqtt_dmn.py restart
    PYTHONPATH= python task/fans_mqtt_dmn.py restart
    PYTHONPATH= python task/lights_mqtt_dmn.py restart
    PYTHONPATH= python task/pumps_mqtt_dmn.py restart
    ;;
  *)
    # Refuse to do other stuff
    echo "Usage: ./gh-mqtt.sh {start|stop|restart}"
    exit 1
    ;;
esac

exit 0
