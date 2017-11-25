#!/usr/bin/env python2

"""
The daemon responsible for changing the volume in response to a press
of the volume buttons.
These two volume buttons are connected to two GPIOs.

Inspired from the recalbox knob volume monitoring script.
https://github.com/recalbox/recalbox-os/wiki/Rotary-Encoder-via-GPIO-%28EN%29
"""

import RPi.GPIO as GPIO
import sys
import time
import subprocess


DEBUG = False


# ======== #
# SETTINGS #
# ======== #

GPIO_PLUS  = 22
GPIO_MINUS = 23


# The minimum and maximum volumes, as percentages.
# The default max is less than 100 to prevent distortion. The default min is
# greater than zero because if your system is like mine, sound gets
# completely inaudible _long_ before 0%. If you've got a hardware amp or
# serious speakers or something, your results will vary.
VOLUME_MIN = 50
VOLUME_MAX = 100


# The amount you want one click of the knob to increase or decrease the
# volume. I don't think that non-integer values work here, but you're welcome
# to try.
VOLUME_INCREMENT = 4


# =============== #
# VOLUME HANDLING #
# =============== #


class Volume:
    """
    A wrapper API for interacting with the volume settings on the RPi.
    """

    volume = VOLUME_MIN

    def __init__(self):
        self.synchronize()
        # Will update the volume if it is not in the bounds
        self.updateVolume(self.volume)

    def __str__(self):
        return str(self.volume)

    def synchronize(self, output=None):
        """
        Reads the output of `amixer` to get update the volume.
        If no amixer output is given, this will run the amixer subprocess to
        get it.

        This is designed not to do much work because it'll get called with every
        click, which is why we're doing simple string scanning and not regular
        expressions.
        """

        if output is None:
            output = self.amixer("get 'PCM'")

        last = output[-1].decode('utf-8')

        # The last line of output will have two values in square brackets. The
        # first will be the volume (e.g., "[95%]") and the second will be the
        # mute state ("[off]" or "[on]").
        i1 = last.rindex('[') + 1
        i2 = last.rindex(']')

        self.is_muted = last[i1:i2] == 'off'

        i1 = last.index('[') + 1
        i2 = last.index('%')
        # In between these two will be the percentage value.
        pct = last[i1:i2]

        self.volume = int(pct)

    def increase(self):
        """
        Increases the volume by one increment.
        """
        if self.volume == 0:
            self.updateVolume(VOLUME_MIN)
        else:
            self.updateVolume(self.volume + VOLUME_INCREMENT)


    def decrease(self):
        """
        Decreases the volume by one increment.
        """
        if self.volume == VOLUME_MIN:
            self.updateVolume(0)
        else:
            self.updateVolume(self.volume - VOLUME_INCREMENT)

    def updateVolume(self, newVolume):
        """
        Adds the given integer to the volume (to Add can be negative)
        """
        boundedVolume = self.restrictToBounds(newVolume)
        if(boundedVolume != self.volume):
            output = self.amixer("set 'PCM' unmute {}%".format(boundedVolume))
            self.synchronize(output)

    def restrictToBounds(self, volume):
        """
        Returns the volume inside the bounds.
        """
        if volume <= 0:
            return 0
        elif volume < VOLUME_MIN:
            return VOLUME_MIN
        elif volume > VOLUME_MAX:
            return VOLUME_MAX
        else:
            return volume

    def amixer(self, cmd):
        """
        Runs the amixer cmd and returns the standard output.
        """
        p = subprocess.Popen("amixer {}".format(cmd), shell=True, stdout=subprocess.PIPE)
        code = p.wait()
        if code != 0:
            raise VolumeError("Unknown error")
            sys.exit(0)

        output = p.stdout.readlines()
        return output



# ============= #
# GPIO HANDLING #
# ============= #

if __name__ == "__main__":

    volume = Volume()

    if DEBUG:
        print("Initial Volume : {}".format(volume))
        sys.stdout.flush()

    def click_handler(pin):
        if pin == GPIO_PLUS:
            volume.increase()
            if DEBUG:
                print("Plus : {}".format(volume))
                sys.stdout.flush()

        if pin == GPIO_MINUS:
            volume.decrease()
            if DEBUG:
                print("Minus : {}".format(volume))
                sys.stdout.flush()

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(GPIO_PLUS, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(GPIO_MINUS, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(GPIO_PLUS, GPIO.FALLING, click_handler, bouncetime=300)
    GPIO.add_event_detect(GPIO_MINUS, GPIO.FALLING, click_handler, bouncetime=300)

    while True:
        time.sleep(10000)



