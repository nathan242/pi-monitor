#!/usr/bin/python

import sys
import os
import time
import shutil
import signal
import subprocess
import Adafruit_SSD1306
import Adafruit_MCP9808.MCP9808
import brightpi.brightpilib
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# CONFIG
run_dir = "/dev/shm/pi-monitor/"
ctl_id = 33
picam_opts = ["/opt/pi-monitor/picam", "--alsadev", "hw:1,0", "-o", run_dir+"/hls/"]
poll_delay = 1


class Display:
    def __init__(self):
        self.__display = Adafruit_SSD1306.SSD1306_128_32(None)
        self.__display.begin()
        self.__display.clear()
        self.__display.display()
        self.__image = Image.new('1', (self.__display.width, self.__display.height))
        self.__draw = ImageDraw.Draw(self.__image)
        self.__font = ImageFont.load_default()

        self.line1 = ""
        self.line2 = ""
        self.line3 = ""
        self.line4 = ""

    def display(self):
        self.__draw.rectangle((0, 0, self.__display.width, self.__display.height), outline=0, fill=0)
        self.__draw.text((0, -2), self.line1, font=self.__font, fill=255)
        self.__draw.text((0, 6), self.line2, font=self.__font, fill=255)
        self.__draw.text((0, 14), self.line3, font=self.__font, fill=255)
        self.__draw.text((0, 23), self.line4, font=self.__font, fill=255)

        self.__display.image(self.__image)
        self.__display.display()

        self.line1 = ""
        self.line2 = ""
        self.line3 = ""
        self.line4 = ""
    
def exit_handler(signum, frame):
    global run_dir
    global picam_running
    if picam_running:
        picam_proc.terminate()
        count = 0
        while picam_proc.poll() is None:
            time.sleep(1)
            count += 1
            if count > 5:
                picam_proc.kill()

    light.reset()
    display.display()
    shutil.rmtree(run_dir)
    sys.exit(0)

# Check if run_dir already exists
if os.path.isdir(run_dir):
    sys.stderr.write("Run directory already exists. Aborting.\n")
    sys.exit(1)

# Create directories
try:
    os.mkdir(run_dir)
    os.chdir(run_dir)
except:
    sys.stderr.write("Cannot change to run directory. Aborting.\n")
    sys.exit(2)

for d in ['rec', 'hooks', 'state', 'mon-ctl', 'mon-out', 'hls']:
    try:
        os.mkdir(d)
    except:
        sys.stderr.write("Error creating '"+d+"' directory. Aborting.\n")
        sys.exit(3)

try:
    os.chmod('mon-ctl', 0777);
except:
    sys.stderr.write("Cannot change permissions on control directory. Aborting.\n")
    sys.exit(4)

temp_sensor = Adafruit_MCP9808.MCP9808.MCP9808()
display = Display()
light = brightpi.brightpilib.BrightPi()

temp_sensor.begin()
light.reset()

picam_service = False
picam_running = False
led_bri = False
led_ir = False
led_bri_running = False
led_ir_running = False
temp = False

# Exit signal handling
signal.signal(signal.SIGINT, exit_handler)
signal.signal(signal.SIGTERM, exit_handler)

# Main loop
while True:
    # Check control directory
    if os.path.isfile("./mon-ctl/camera"):
        picam_service = True
    else:
        picam_service = False

    if os.path.isfile("./mon-ctl/led-bri"):
        led_bri = True
    else:
        led_bri = False

    if os.path.isfile("./mon-ctl/led-ir"):
        led_ir = True
    else:
        led_ir = False

    # Start/stop picam
    if picam_service and not picam_running:
        picam_proc = subprocess.Popen(picam_opts)
        if picam_proc.poll() is None:
            picam_running = True
    elif not picam_service and picam_running:
        if picam_proc.poll() is not None:
            picam_running = False
        else:
            picam_proc.terminate()
            count = 0
            while picam_proc.poll() is None:
                time.sleep(1)
                count += 1
                if count > 5:
                    picam_proc.kill()
            picam_running = False

    # Control LED's
    if led_bri and not led_bri_running:
        light.set_led_on_off(brightpi.brightpilib.LED_WHITE, brightpi.brightpilib.ON)
        led_bri_running = True
    elif not led_bri and led_bri_running:
        light.set_led_on_off(brightpi.brightpilib.LED_WHITE, brightpi.brightpilib.OFF)
        led_bri_running = False

    if led_ir and not led_ir_running:
        light.set_led_on_off(brightpi.brightpilib.LED_IR, brightpi.brightpilib.ON)
        led_ir_running = True
    elif not led_ir and led_ir_running:
        light.set_led_on_off(brightpi.brightpilib.LED_IR, brightpi.brightpilib.OFF)
        led_ir_running = False

    # Read temperature
    temp = temp_sensor.readTempC()
    with open("./mon-out/temp", "w") as temp_out:
        temp_out.write(str(temp))

    # Update display
    display.line1 = "TEMP: "+str(round(temp,1))+" C"
    display.line2 = "CAMERA: "
    if picam_running:
        display.line2 += "ON"
    else:
        display.line2 += "OFF"
    display.line3 = "LIGHT: "
    if led_bri:
        display.line3 += "BRI "
    if led_ir:
        display.line3 += "IR"
    if not led_bri and not led_ir:
        display.line3 += "OFF"
    display.display()

    time.sleep(poll_delay)


