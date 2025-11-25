# Raspberry Pi PC Tower

A remix of the [Raspberry Pi Media Server](https://www.printables.com/model/269198-raspberry-pi-media-server) project by Noe Ruiz [Learn Guide](https://learn.adafruit.com/pi-ssd-media-server/).

Uses a 40 mm 5V PWM Noctua Fan, STEMMA OLED and EMC2101 fan controller breakout. The pi_pc.py file can run as a service to control the fan based on the CPU temperature and display IP address, service status, CPU temp and fan RPM.

### How to create the system service:
```terminal
sudo nano /lib/systemd/system/tftdisplay.service
```
Insert the `tftdisplay.service` file in this repo. Enable the service with:
```terminal
sudo systemctl enable tftdisplay.service
```