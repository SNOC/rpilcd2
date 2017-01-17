# rpilcd2 board control scripts

##### The aim of this set of scripts is to use the rpilcd2 board OLED display and buttons.
Those scripts use [Adafruit's SSD1306 implementation](https://github.com/adafruit/Adafruit_Python_SSD1306)

You can purchase the kit on [YADOM.FR](http://yadom.fr/boitier-din-avec-afficheur-oled-et-clavier.html).

Three python scripts are provided :

- testio.py: displays the name of the button pressed in the console.

-  rpilcd2menu.py: vertical menu template with pictures displayed according to the selected item. The pictures' maximum width is adjusted with the menu items texts length.

-  rpilcd2actions.py: displays date, time or IP address. SW1 displays the IP address of the Rapsberry Pi, SW4 just displays the time. Return to the initial display with SW2. SW3 switches mode every second as long as the button is pressed.

##### Usage
```sh
cd to script's directory
sudo python [name of script].py
```
example :
```sh
cd /rpilcd2/rpilcd2menu
sudo python rpilcd2menu.py
```
Type Ctrl-C to exit

##### Prerequisites

- [Activate SPI with raspi-config utility](https://www.raspberrypi.org/documentation/hardware/raspberrypi/spi/README.md):
```sh    
sudo raspi-config
```
-> Advanced Options >> SPI >> Yes >> Ok

- Install Adafruit's libraries :
```sh
sudo apt-get update
sudo apt-get install git build-essential python-dev python-pip python-imaging python-smbus
git clone https://github.com/adafruit/Adafruit_Python_SSD1306.git
cd Adafruit_Python_SSD1306
sudo python setup.py install
```

##### License

MIT License / read license.txt

