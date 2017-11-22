Retrogear
=========

This repository contains the initial setup of the recalbox os on a Raspberry Pi
Zero W used in the Retrogear project.

## Setup

* Install the last version of recalbox using the Pi0 image and setup the
wifi connection using the emulation station configuration menu.

* Ensure the wifi and ssh connections of the Rpi0W are enabled by using the
following command.
```
(ssh -q root@recalbox echo > /dev/null && echo "Connection OK") || echo "Connection Failed"
```

* Run the `setup.sh` script to setup the system.
```
./setup.sh
```


## GPIO Branching

This section describes how to connect Rpi0W pins to hardware or buttons.

BCM | Pin Number | Connected to
--- | ---------- | ------------
GPIO #18 | Pin #12 | Right Audio Channel
GPIO #13 | Pin #33 | Left Audio Channel
GPIO #22 | Pin #15 | Volume + Button
GPIO #23 | Pin #16 | Volume - Button
GPIO #2 | Pin #3 | MCP-23017 SDA

You can use this schema to find the matching pins on the Pi:

![GPIOs](https://www.element14.com/community/servlet/JiveServlet/previewBody/80667-102-2-338789/GPIO.png)



