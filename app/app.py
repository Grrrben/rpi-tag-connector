import logging
import time

from pad4pi import rpi_gpio

from app.components import *
from app.cache.cache import *
from app.request.req import ApiRequest


class App():
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        self.api = ApiRequest(self.config, self.logger)

    def set_cache(self, cache: Cache):
        self.cache = cache

    def wait(self):
        """
        waiting for a signal
        """
        print("I'm listening")

        led = Led()
        led.blink_blue()

        rfid = Rfid(self.logger)
        rfid.set_api(self.api)

        rfid.register_positive_handler(led.blink_green)
        rfid.register_negative_handler(led.blink_red)

        rfid.wait()