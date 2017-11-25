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

* Restart RecalboxOS


## GPIO Branching

This section describes how to connect Rpi0W pins to hardware or buttons.

Pin Number | BCM | Connected to
--- | ---------- | ------------
Pin #2 | 5V | Powerboost 500C 5V
Pin #6 | Ground | Powerboost 500C GND
Pin #3 | SDA #2 | MCP-23017 SDA
Pin #5 | SCL #2 | MCP-23017 SCL
Pin #9 | Ground | MCP-23017 A0
Pin #9 | Ground | MCP-23017 A1
Pin #9 | Ground | MCP-23017 A2
Pin #12 | GPIO #18 | Right Audio Channel
Pin #14 | Ground | Volume + Button
Pin #14 | Ground | Volume - Button
Pin #15 | GPIO #22 | Volume + Button
Pin #16 | GPIO #23 | Volume - Button
Pin #33 | GPIO #13 | Left Audio Channel

You can use this schema to find the matching pins on the Pi:

![GPIOs](/images/raspberry-pi-pinout.png)



