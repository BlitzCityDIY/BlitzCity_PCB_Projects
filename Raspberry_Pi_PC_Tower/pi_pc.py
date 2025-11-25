# SPDX-FileCopyrightText: 2025 Liz Clark
#
# SPDX-License-Identifier: MIT

import subprocess
import os
import time
from PIL import Image, ImageDraw, ImageFont
import simpleio
import board
from adafruit_emc2101 import EMC2101
import adafruit_ssd1306

i2c = board.I2C()
emc = EMC2101(i2c)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3d)

def get_temp():
        try:
                with open('/sys/class/thermal/thermal_zone0/temp', 'r') as temp_file:
                        raw_temp = temp_file.read().strip()
                        temp_c = float(raw_temp) / 1000.0
                        return temp_c
        except Exception as e:
                print(f"error! {e}")
                return None

oled.fill(0)
oled.show()

image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

def get_ip():
        cmd = "hostname -I | cut -d' ' -f1"
        ip = subprocess.check_output(cmd, shell=True).decode("utf-8")
        return ip
def check_hyperhdr():
        cmd = "sudo systemctl is-active hyperhdr@pi.service"
        hdr_status = subprocess.check_output(cmd, shell=True).decode("utf-8")
        return hdr_status 

while True:
        try:
                image = Image.new("1", (oled.width, oled.height))
                draw = ImageDraw.Draw(image)
                status = check_hyperhdr()
                ip_addr = get_ip()
                pi_temp = get_temp()
                mapped_speed = simpleio.map_range(pi_temp, 40, 85, 25, 100)
                emc.manual_fan_speed = mapped_speed
                fan_text = f"Fan Speed: {emc.fan_speed:.1f} RPM"
                ip_text = f"IP Address: {ip_addr}"
                hyper_text = f"HyperHDR Status: {status}"
                temp_text = f"CPU Temp: {pi_temp:.1f}°C"
                text = f"{ip_text}{hyper_text}{temp_text}\n{fan_text}"
                draw.multiline_text((0,0),
                          text,
                          fill = 255,
                          font = font)
                oled.image(image)
                oled.show()
                print(f"fan speed: {emc.fan_speed}")
                print(emc.internal_temperature)
                print(pi_temp)
                print(status, ip_addr)
                time.sleep(15)
        except Exception as e:
                print(f"error! {e}")
                time.sleep(10)
