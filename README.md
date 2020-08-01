# PSUControl-Button
Add a physical button to the Raspberry Pi to toggle your printers PSU via the Octoprint plugin PSUControl.

This small and simple script has the following features:

* Ties into PSUControl by making API calls rather than altering GPIO directly.
* Debounce code to reject fast input from button bounce.
* Adjustable toggle delay to prevent cycling power too fast.
* You can kill the script externally by pressing the button five times after an initial click and half second delay.
* Threaded to utilize minimum resources when idle. (0% cpu usage through use off callbacks and 3.7MB of memory due to python when IDLE.)

### Physical Setup:

I have a button setup with power coming from pin 1 with pin 11 set as input running through a 10k ohm resistor. In my testing a capacitor only caused issues, and there a basic but reliable debounce delay into the code. If you desire, you can also implement a debounce circuit in hardware and reduce or eliminate the debounce time variable.

### Software Setup:

Download the Repo either by downloading from the website and unpacking or by cloning using the collowing steps.

`cd ~`

`git clone https://github.com/aricshow/PSUControl-Button.git`


This will create folder in your home directory called PSUControl-Button.

You will need to edit psubutton.py to add your Octoprint API key, as well as to alter any of the settings declared as constants at the top of the file such as the GPIO pin number and toggle delay.

You can get you API key from the settings menu of Octoprint under API.

`chmod 755 start.sh`

You can run the code to test it and see the log data output to console to test your setup. More advanced users may wish to comment out the API calls to power the PSU on and off, and uncomment the debounce message to fine tune your debounce timing - but the default settings ought to work fine for most.

You can start the script on bootup by adding a cronjob. Use the command `sudo crontab -e` and add the following line:

`@reboot sh /home/pi/PSUControl-Button/start.sh >>/home/pi/PSUControl-Button/log 2>&1`

Happy printing.
