// SPDX-FileCopyrightText: 2025 Liz Clark
//
// SPDX-License-Identifier: MIT

/* Color test for four Newxie Displays on the Nixie Newxie Shield
 * Each display shows a different color (yellow, red, green or blue)
 */

#include <SPI.h>
#include <Adafruit_GFX.h>
#include <Adafruit_ST7789.h>

#define TFT_RST  -1 // To display reset pin

Adafruit_ST7789  ST7789_3(5, 6, TFT_RST);
Adafruit_ST7789  ST7789_2(7, 8, TFT_RST);
Adafruit_ST7789  ST7789_1(9, 10, TFT_RST);
Adafruit_ST7789  ST7789_0(11, 12, TFT_RST);

void setup() {
  ST7789_3.init(135, 240);
  ST7789_2.init(135, 240);
  ST7789_1.init(135, 240);
  ST7789_0.init(135, 240);

  ST7789_3.fillScreen(0);
  ST7789_2.fillScreen(0);
  ST7789_1.fillScreen(0);
  ST7789_0.fillScreen(0);

}

void loop() {
  ST7789_0.fillScreen(0xFFE0); // yellow
  delay(5);
  ST7789_1.fillScreen(0xF800); // red
  delay(5);
  ST7789_2.fillScreen(0x07E0); // green
  delay(5);
  ST7789_3.fillScreen(0x001F); // blue
  delay(2000);
  ST7789_0.fillScreen(0);
  ST7789_1.fillScreen(0);
  ST7789_2.fillScreen(0);
  ST7789_3.fillScreen(0);
  delay(2000);
}
