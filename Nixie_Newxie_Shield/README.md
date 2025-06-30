# Nixie Newxie Shield

A PCB that lets you plug four [Newxie Vertical Displays](https://www.adafruit.com/product/6113) into an Arduino/Metro format board.

It uses the 2x3 SPI pins on the edge of the board and pins 5-12 for CS and DC for each display.

Tested with an [Adafruit Metro ESP32-S3](https://www.adafruit.com/product/5500). Two Arduino examples are available:
	* Color Test - Blinks a different color on each of the four displays (yellow, red, blue and green)
	* Nixie Clock - Fetches the time from the [Worldtime API](http://worldtimeapi.org/api/timezone/Etc/UTC) and displays it using Nixie tube number images
		* The Nixie tube images are from [Wikimedia](https://commons.wikimedia.org/w/index.php?search=nixie+tube+Z566M&title=Special%3AMediaSearch&type=image). They were cropped, converted to bitmaps and converted to byte arrays with [image2cpp](https://javl.github.io/image2cpp/).