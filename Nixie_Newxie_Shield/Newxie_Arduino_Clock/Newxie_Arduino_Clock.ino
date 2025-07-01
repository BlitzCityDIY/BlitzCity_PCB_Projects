// SPDX-FileCopyrightText: 2025 Liz Clark
//
// SPDX-License-Identifier: MIT

#include <SPI.h>
#include <Adafruit_GFX.h>
#include <time.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <Adafruit_ST7789.h>
#include "img.h"

#define TFT_RST  -1 // To display reset pin
const char* ssid = "your-ssid-here";
const char* password = "your-password-here";
// timezone as UTC offset and text
int timezone = -4;
const char* tz_text = "EST5EDT";
int WIDTH = 135;
int HEIGHT = 240;
int count = 0;
int hourTens = 0;
int hourOnes = 0;
int minuteTens = 0;
int minuteOnes = 0;

bool fetch = true;
unsigned long lastUpdate = 0;
unsigned long lastMillis = 0;
unsigned long lastScroll = 0;
int LOOP_DELAY = 30000;
char timeBuffer[10];
String clockEndpoint = "http://worldtimeapi.org/api/timezone/Etc/UTC";

Adafruit_ST7789  ST7789_3(5, 6, TFT_RST);
Adafruit_ST7789  ST7789_2(7, 8, TFT_RST);
Adafruit_ST7789  ST7789_1(9, 10, TFT_RST);
Adafruit_ST7789  ST7789_0(11, 12, TFT_RST);

void setup() {
  Serial.begin(115200);
  //while ( !Serial ) delay(10);

  // Connect to WiFi
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println();
  Serial.println("WiFi connected");
  ST7789_3.init(WIDTH, HEIGHT);
  ST7789_2.init(WIDTH, HEIGHT);
  ST7789_1.init(WIDTH, HEIGHT);
  ST7789_0.init(WIDTH, HEIGHT);

  ST7789_3.fillScreen(0);
  ST7789_2.fillScreen(0);
  ST7789_1.fillScreen(0);
  ST7789_0.fillScreen(0);

  lastMillis = millis();

}

void loop() {
  if (millis() > (lastUpdate + LOOP_DELAY) or fetch) {
      fetch = false;
      if (WiFi.status() == WL_CONNECTED) {
        HTTPClient http;
        http.begin(clockEndpoint);
        int httpResponseCode = http.GET();
        if (httpResponseCode > 0) {
          String payload = http.getString();
          Serial.println(payload);
          DynamicJsonDocument doc(1024);
          DeserializationError error = deserializeJson(doc, payload);
          if (!error) {
                String datetime = doc["utc_datetime"].as<String>();
                Serial.println(datetime);
                struct tm timeinfo = parseISO8601(datetime, timezone);
                int hour12 = timeinfo.tm_hour % 12;
                if (hour12 == 0) hour12 = 12;

                hourTens = hour12 / 10;
                hourOnes = hour12 % 10;
                minuteTens = timeinfo.tm_min / 10;
                minuteOnes = timeinfo.tm_min % 10;

                Serial.print("Time digits: ");
                Serial.print(hourTens);
                Serial.print(hourOnes);
                Serial.print(":");
                Serial.print(minuteTens);
                Serial.println(minuteOnes);
                strftime(timeBuffer, sizeof(timeBuffer), "%I:%M", &timeinfo);
            } else {
            Serial.print("deserializeJson() failed: ");
            Serial.println(error.f_str());
          }
        } else {
          Serial.print("Error code: ");
          Serial.println(httpResponseCode);
        }
        http.end();
      } else {
        Serial.println("WiFi Disconnected");
        WiFi.begin(ssid, password);
      }
    lastUpdate = millis();
  }

  const uint16_t* bitmap;
  bitmap = fetch_nixie(hourTens);
  // will make the updates more efficient, right now it works
  ST7789_0.drawRGBBitmap(0, 0, bitmap, WIDTH, HEIGHT);
  delay(5);
  bitmap = fetch_nixie(hourOnes);
  ST7789_1.drawRGBBitmap(0, 0, bitmap, WIDTH, HEIGHT);
  delay(5);
  bitmap = fetch_nixie(minuteTens);
  ST7789_2.drawRGBBitmap(0, 0, bitmap, WIDTH, HEIGHT);
  delay(5);
  bitmap = fetch_nixie(minuteOnes);
  ST7789_3.drawRGBBitmap(0, 0, bitmap, WIDTH, HEIGHT);
  delay(5);
}

const uint16_t* fetch_nixie(int index) {
  count += 1;
  if (count > (nixie_allArray_LEN - 1)) {
    count = 0;
  }
  const uint16_t* b = nixie_allArray[index];
  return b;
}

struct tm parseISO8601(String d, int tzo) {
  struct tm tm;
  sscanf(d.c_str(), "%d-%d-%dT%d:%d:%d",
         &tm.tm_year, &tm.tm_mon, &tm.tm_mday,
         &tm.tm_hour, &tm.tm_min, &tm.tm_sec);
  tm.tm_year -= 1900;
  tm.tm_mon -= 1;
  tm.tm_isdst = -1;
  Serial.println(tm.tm_hour);
  Serial.println(tzo);
  tm.tm_hour += tzo;
  Serial.println(tm.tm_hour);
  mktime(&tm);
  return tm;
}
