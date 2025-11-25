# Raspberry Pi PC Tower

A remix of the [Raspberry Pi Media Server](https://www.printables.com/model/269198-raspberry-pi-media-server) project by Noe Ruiz [Learn Guide](https://learn.adafruit.com/pi-ssd-media-server/).

Uses a [40 mm 5V PWM Noctua Fan](https://www.noctua.at/en/products/nf-a4x10-5v-pwm), [STEMMA OLED](https://www.adafruit.com/product/938) and [EMC2101 fan controller breakout](https://www.adafruit.com/product/4808). The `pi_pc.py` file can run as a service to control the fan based on the CPU temperature and display IP address, service status, CPU temp and fan RPM.

### Python Dependencies
The code uses CircuitPython and [requires Blinka](https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi), the CircuitPython compatibility layer for Raspberry Pi.

After installing Blinka, install these library dependencies:
```terminal
pip3 install adafruit-circuitpython-simpleio adafruit-circuitpython-emc2101 adafruit-circuitpython-ssd1306 Pillow
```

### How to create the system service:
```terminal
sudo nano /lib/systemd/system/tftdisplay.service
```
Insert the `tftdisplay.service` file in this repo. Enable the service with:
```terminal
sudo systemctl enable tftdisplay.service
```