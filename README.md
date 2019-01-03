# SLX Rpi tag connector

## Connecting a RFID-RC522 chip reader

Connect the RC522 module to the RPI using the following wiring schema:

| Board pin name | Board pin | Physical RPi pin | RPi pin name |
|----------------|-----------|------------------|--------------|
| SDA            | 1         | 24               | GPIO8, CE0   |
| SCK            | 2         | 23               | GPIO11, SCKL |
| MOSI           | 3         | 19               | GPIO10, MOSI |
| MISO           | 4         | 21               | GPIO9, MISO  |
| IRQ            | 5         | 12               | GPIO18       |
| GND            | 6         | 6, 9, 20, 25     | Ground       |
| RST            | 7         | 15               | GPIO22       |
| 3.3V           | 8         | 1,17             | 3V3          |

More information in the [pi-rc522](https://github.com/ondryaso/pi-rc522/blob/master/README.md) repository.