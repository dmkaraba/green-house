#!/usr/bin/python
import logging


def debug(msg):
    logging.basicConfig(filename='logs/debug.log', level=logging.DEBUG,
                        format="%(asctime)s %(levelname)s: %(message)s",
                        datefmt='%d-%m-%Y %I:%M:%S')
    logging.debug(msg)


def info(msg):
    logging.basicConfig(filename='logs/info.log', level=logging.DEBUG,
                        format="%(asctime)s %(levelname)s: %(message)s",
                        datefmt='%d-%m-%Y %I:%M:%S')
    logging.info(msg)


def warning(msg):
    logging.basicConfig(filename='logs/warning.log', level=logging.DEBUG,
                        format="%(asctime)s %(levelname)s: %(message)s",
                        datefmt='%d-%m-%Y %I:%M:%S')
    logging.warning(msg)


def error(msg):
    logging.basicConfig(filename='logs/error.log', level=logging.DEBUG,
                        format="%(asctime)s %(levelname)s: %(message)s",
                        datefmt='%d-%m-%Y %I:%M:%S')
    logging.error(msg)