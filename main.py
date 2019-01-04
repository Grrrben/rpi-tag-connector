import configparser
import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

import RPi.GPIO as GPIO

import app

def init():
    config = configparser.ConfigParser()
    config.read('config.ini')

    rdr = app.App(config)

    now = datetime.now()

    dir_path = os.path.dirname(os.path.realpath(__file__))

    logfile = "{0}/log/smartapi_{1}_{2}.log".format(dir_path, now.month, now.year)
    file_handler = RotatingFileHandler(logfile, maxBytes=10485760, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))

    rdr.logger.addHandler(file_handler)
    rdr.logger.setLevel(logging.INFO)

    rdr.logger.debug("DEBUG in main.init")
    rdr.wait()

def destroy():
    """ ending the program gracefully """
    GPIO.cleanup()

if __name__ == "__main__":
    try:
        init()

    # Cleaning GPIO up when 'Ctrl+C' is pressed
    except KeyboardInterrupt:
        destroy()
