# RPI tag_reader


## Introductie

Dit is het installatie document dat beschrijft hoe je:

1. Een Raspberry Pi (RPI3) 3 als gateway opzet
2. Een Raspberry Pi Zero (Zero) als kaartlezer opzet
3. en deze koppelt aan een Smart API website.


## (1) Gateway

De RPI3 gebruiken we als WiFi gateway voor een of meer paslezers.
We gaan de WiFi dus omgekeerd gebruiken op de RPI3, als access point, en
sluiten de RPI3 zelf aan  via een LAN kabel.

### (1.1) Raspian

Zet de laatste Raspbian versie op een SD kaart.
Download Raspbian hier: https://www.raspberrypi.org/downloads/raspbian/

### (1.2) Access point

De Raspberry Pi foundation heeft er een blog aan gewijd, die up-to-date is aan de
laatste RPI3 versie.

https://www.raspberrypi.org/documentation/configuration/wireless/access-point.md

Ze hebben het hier na een tijdje over de settings van file `/etc/hostapd/hostapd.conf`.
Hier staan de naam en wachtwoord van de WIFI hotspot in. Pas deze naar wens aan en noteer
ze even voor later gebruik.

```
# cat /etc/hostapd/hostapd.conf
ssid=NameOfNetwork
wpa_passphrase=AardvarkBadgerHedgehog
```

Let ook even op dit regeltje in de dhcpcd setting /etc/dhcpcd.conf:

`static ip_address=192.168.4.1/24`

## (2) Kaartlezer

Van de Zero maken we een kaartlezer. Maar eerst koppelen we hem via WiFi aan de RPI3.

### (2.1) Headless PI ssh setup

Een Zero heeft geen netwerkaansluiting en alleen een micro hdmi aansluiting, door wat wijzigingen
aan het SD kaartje van de Zero te maken kun je hem "headless" installeren, en SSH beschikbaar maken.

`dd` Raspbian op de SD kaart en ga dan naar de /boot directory. Hier kun je de WiFi instellen met
een bestandje dat je `wpa_supplicant.conf` noemt waarin je de login gegevens zet.

```
country=NL
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
network={
    ssid="NameOfNetwork"
    psk="AardvarkBadgerHedgehog"
    key_mgmt=WPA-PSK
}
```
SSID is de naam van je eerder gedefinieerde WiFi netwerk, psk is het WiFi wachtwoord.

Om SSH beschikbaar te maken zet je in dezelfde dir een leeg bestand met de naam `ssh`, dus `touch ssh`.

### (2.2) Software setup

Je kan nu in de Zero komen via de RPI3. Gebruik `nmap` om de RPI3 op te zoeken.

`nmap -sP 172.29.4.*`

Daar kun je verder "nmappen" om de Zero te vinden en in te loggen via SSH.

Om goed met de GPIO om te kunnen gaan moet SPI aan staan op de Zero. Dit kan via `raspi-config`.
Zie ook https://www.raspberrypi.org/documentation/hardware/raspberrypi/spi/README.md

#### 2.2.1. Git

Maak een SSH keypair aan en voeg deze toe aan je account op Github.

```
ssh-keygen -o
cat .ssh/id_rsa.pub

```

Clone de repository op https://github.com/Grrrben/rpi-tag-connector:

```
git clone git@github.com:Grrrben/rpi-tag-connector.git
```

### (2.3) Board setup

Om de koppeling tussen de RC522 tagreader en de Zero te maken gebruik je onderstaand schema:

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


(Pinout)[https://pinout.xyz/] is een goede website om de nummers van de verschillende pinnen te bekijken.
De software maakt gebruik van de Physical RPi pin, ook wel BOARD schema genoemd.

Bij het instellen van de Led worden board pins 35, 36 en 37 voor RGB gebruikt.

## (3) Koppelen

Installeer PIP en ga naar de `~/rpi-tag-connector` directory en installleer de dependencies.

`python3 -m venv venv`
`pip install -r requirements.txt`

Maak een `config.ini` bestandje aan in de root van het project, gebaseerd op de `config.dist`.

### (3.1) Systemd

Opstarten van de reader via systemd kan met de volgende unitfile:

```
# cat /etc/systemd/system/tag_connector.service

[Unit]
Description=RPI Tag Connector
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/home/pi/rpi-tag-connector
ExecStart=/home/pi/rpi-tag-connector/venv/bin/python /home/pi/rpi-tag-connector/main.py
Restart=always

[Install]
WantedBy=multi-user.target

```
sudo systemctl enable tag_connector.service


### Debuggen



tail -f log/smartapi_1_2019.log

