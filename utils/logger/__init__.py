#!/usr/bin/python

import os
import logging
from config import Config


config_dir = Config.log_dir

def debug(msg):
    logging.basicConfig(filename=os.path.join(config_dir, 'debug.log'), level=logging.DEBUG,
                        format="%(asctime)s %(levelname)s: %(message)s",
                        datefmt='%d-%m-%Y %I:%M:%S')
    logging.debug(msg)


def info(msg):
    logging.basicConfig(filename=os.path.join(config_dir, 'info.log'), level=logging.DEBUG,
                        format="%(asctime)s %(levelname)s: %(message)s",
                        datefmt='%d-%m-%Y %I:%M:%S')
    logging.info(msg)


def warning(msg):
    logging.basicConfig(filename=os.path.join(config_dir, 'warning.log'), level=logging.DEBUG,
                        format="%(asctime)s %(levelname)s: %(message)s",
                        datefmt='%d-%m-%Y %I:%M:%S')
    logging.warning(msg)


def error(msg):
    logging.basicConfig(filename=os.path.join(config_dir, 'error.log'), level=logging.DEBUG,
                        format="%(asctime)s %(levelname)s: %(message)s",
                        datefmt='%d-%m-%Y %I:%M:%S')
    logging.error(msg)