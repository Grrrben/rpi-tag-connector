import RPi.GPIO as GPIO
from pirc522 import RFID
from urllib.error import HTTPError


class Rfid:
    def __init__(self, logger):
        self.logger = logger
        self.api = None
        self.rdr = None

        self._positive_handlers = []
        self._negative_handlers = []

    def set_api(self, api):
        self.api = api

    def register_positive_handler(self, handler):
        """
        Registers a handler (function) that will be called when a positive action is performed e.g. Access granted
        There can be any number of handlers
        """
        self._positive_handlers.append(handler)

    def unregister_positive_handler(self, handler):
        """
        Removes a handler from the positive handler list
        """
        self._positive_handlers.remove(handler)

    def register_negative_handler(self, handler):
        """
        Registers a handler (function) that will be called when a negative action is performed e.g. Access denied
        There can be any number of handlers
        """
        self._negative_handlers.append(handler)

    def unregister_negative_handler(self, handler):
        """
        Removes a handler from the positive handler list
        """
        self._negative_handlers.remove(handler)

    def wait(self):
        """
        Waiting for a signal
        """

        self.rdr = RFID()

        while True:
            self.rdr.wait_for_tag()
            (error, tag_type) = self.rdr.request()

            if not error:
                (error, uid) = self.rdr.anticoll()
                if not error:
                    # for MIFARE with a single UID the UID consists of the first 4 bites.
                    # The fifth one is the Block Check Character, it is calculated as exclusive-or over the 4 previous bytes.
                    hex_uid = uid[0:4]
                    hex_uid.reverse()

                    chip_number = hex_uid[0] << 24 | hex_uid[1] << 16 | hex_uid[2] << 8 | hex_uid[3]
                    try:
                        success = self.api.add_chipnumber(chip_number)

                        if success:
                            for handler in self._positive_handlers:
                                handler()
                        else:
                            for handler in self._negative_handlers:
                                handler()

                        print("Tag with chip_number {} added: {}".format(chip_number, success))
                    except HTTPError as e:
                        self.logger.error("HTTPError while trying to api.add_chipnumber; {}".format(e))
                    except Exception as e:
                        self.logger.error("Awkward Exception; {}".format(e))

    def destroy(self):
        # Calls GPIO cleanup
        self.rdr.cleanup()
