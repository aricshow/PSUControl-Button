# MIT License
#
# Copyright (c) 2020 Aric Showalter
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import RPi.GPIO as GPIO
import time
import json
import requests
import threading

#Define CONSTANTS
API_URL = "http://127.0.0.1/api/plugin/psucontrol" #Default for Octopi, can be varified from a browser.
API_KEY = "1234567890" #Replace with your API Key
HEADER = {'X-Api-Key': API_KEY}
CLK_ID = time.CLOCK_REALTIME
TIMEOUT = 10.0  # Delay in seconds between allowed power cycles.
BOUNCE = 0.5  # Delay for debounce, can be fine tuned lower or higher as desired.
SPEED = 3.0  # Max amount of time for quick presses to exit script.
EXITNUM = 5  # Number of quick presses required to exit.
GPIOPIN = 11  # Number of the GPIO Pin that your button input is connected to.

# Global Variables
last_press = time.clock_gettime(CLK_ID)-TIMEOUT  # Prevent wait X sec after startup
quick_presses = 0  # Count for how many times the button has been pressed quickly.
quit_request = threading.Event()

def button_callback(channel):
	global last_press
	global quick_presses
	this_press = time.clock_gettime(CLK_ID)
	if ((thispress-last_press)<TIMEOUT):
		#print("Filtered fast input:"+(this_press-last_press))
		#Uncomment this line to test button bounce
		if(SPEED>(this_press-last_press)>BOUNCE): 
			quick_presses  += 1
			if(quick_presses >= EXITNUM):
				print(time.ctime()+": Quick button exit activated.")
				quit_request.set()
	else:
		quick_presses = 0. # Reset quick presses
		status = requests.get(API_URL, headers=HEADER).json()
		if status['isPSUOn']:
			print(time.ctime()+": Turning PSU OFF")
			# Comment this next line out during testing to prevent actual power cycle.
			requests.post(API_URL, json={'command': 'turnPSUOff'}, headers=HEADER)  # If this throws any errors, it will end up in the log.
		else:
			print(time.ctime()+": Turning PSU ON")
			# Comment this next line out during testing to prevent actual power cycle
			requests.post(API_URL, json={'command': 'turnPSUOn'}, headers=HEADER)
		last_press = this_press

GPIO.setwarnings(True)  # Log any warnings. Can set to false to ignore GPIO warnings in your logs.
GPIO.setmode(GPIO.BOARD)
GPIO.setup(GPIOPIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(GPIOPIN, GPIO.RISING, callback=button_callback)

print(time.ctime()+": Script Started")

# Will now suspend and wait uptil quit event triggered
quit_request.wait()

GPIO.cleanup()
print(time.ctime()+": Performed cleanup and exiting.")

if __name__ == "__main__":
	main()
