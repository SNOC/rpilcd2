import time

# OLED screen
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

# offscreen
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# Raspberry Pi pin configuration:
RST = 25
# Note the following are only used with SPI:
DC = 24
SPI_PORT = 0
SPI_DEVICE = 0

# 128x64 display with hardware SPI:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# buttons
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN) # SW1
GPIO.setup(17, GPIO.IN) # SW2
GPIO.setup(18, GPIO.IN) # SW4
GPIO.setup(27, GPIO.IN) # SW3

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
padding = 2
top = padding
bottom = height-padding
x = padding

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Load default font.
font = ImageFont.load_default()

def drawMenuItem(str, selected, x, y, displayWidth, imageWidth):
	sizeX, sizeY = draw.textsize(str)
	if selected :
		draw.rectangle((x, y, x + sizeX, y + sizeY), outline=255, fill=255)
		draw.text((x, y), str,  font=font, fill=0)
	else :
		draw.text((x, y), str,  font=font, fill=255)
	if imageWidth > (displayWidth - x - sizeX) :
		imageWidth = displayWidth - x - sizeX
	return y + sizeY, imageWidth

selectedItem = 1
itemCount = 5
imageWidth = disp.width
updateMenu = True
updateDisplay = True
repeatDecounter=0
print('Press Ctrl-C to quit.')
while True:
	if not GPIO.input(4): # SW1 - selection UP
		if selectedItem > 1 :
			selectedItem -= 1
			updateMenu = True
			repeatDecounter=15
	elif not GPIO.input(27) : # SW3 - selection DOWN
		if selectedItem < itemCount:
			selectedItem += 1
			updateMenu = True
			repeatDecounter=15
	elif not GPIO.input(18) : # SW4 - display an image named 1.png if item 1 is selected, 2.png if item 2 is selected, etc.
		readImage = Image.open('{0}.png'.format(selectedItem)).convert('1')
		aspectRatio = readImage.size[1] / (readImage.size[0] * 1.0)
		if aspectRatio < 1.0 and readImage.size[0] > imageWidth :
			readImage = readImage.resize((imageWidth, (int) (imageWidth * aspectRatio)), Image.ANTIALIAS)
		elif readImage.size[1] > disp.height :
			readImage = readImage.resize(((int) (disp.height / aspectRatio), disp.height), Image.ANTIALIAS)
		hFill = (imageWidth - readImage.size[0]) / 2
		vFill = (disp.height - readImage.size[1]) / 2
		draw.rectangle((disp.width - imageWidth, 0, disp.width, disp.height), outline=0, fill=0)
		image.paste(readImage, (disp.width - imageWidth + hFill, vFill, disp.width - imageWidth + hFill + readImage.size[0], vFill + readImage.size[1]))
		updateDisplay = True
	elif not GPIO.input(17) : # SW2
		draw.rectangle((disp.width - imageWidth, 0, disp.width, disp.height), outline=0, fill=0)
		updateDisplay = True
	if updateMenu :
		updateMenu = False
		updateDisplay = True
		# Draw a black filled box to clear the image.
		draw.rectangle((0,0,disp.width - imageWidth,height), outline=0, fill=0)
		# Draw menu
		starty = top
		starty, imageWidth = drawMenuItem('Chat 1', selectedItem == 1, x, starty, disp.width, imageWidth)
		starty, imageWidth = drawMenuItem('Chat 2', selectedItem == 2, x, starty, disp.width, imageWidth)
		starty, imageWidth = drawMenuItem('SNOC', selectedItem == 3, x, starty, disp.width, imageWidth)
		starty, imageWidth = drawMenuItem('Yadom', selectedItem == 4, x, starty, disp.width, imageWidth)
		starty, imageWidth = drawMenuItem('Renard', selectedItem == 5, x, starty, disp.width, imageWidth)
		
	if updateDisplay :
		# Display imageFalse
		updateDisplay = False
		disp.image(image)
		disp.display()
		# wait all buttons are released
		while ((not GPIO.input(4)) or (not GPIO.input(27))) and (repeatDecounter != 0) :
			time.sleep(0.05)
			if repeatDecounter != 0:
				repeatDecounter -= 1
		while (not GPIO.input(18)) or (not GPIO.input(17)) :
			time.sleep(0.05)

