"""
#!/usr/bin/env pybricks-micropython
# Importing the required EV3 modules and libraries
from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase

import sys

import movement, missions # Importing the other scipts

# Testing for Beep noise, to check if the speaker is working.
brick.sound.beep(2000, 200, 50)

# Checking for the battery level
# First, checking for the current
if brick.battery.current() < 150:
  brick.sound.beep(1000, 1000, 100) # If the current is less than 150, making a beep to allow the user to know that the battery level is lower.
# Next, checking the voltage
if brick.battery.voltage() < 7000:
  brick.sound.beep(400, 1000, 100) # If the voltage is less than 7000, making a beep to allow the user to know that the battery level is lower.

  # Displaying the exact current and voltage on the console and brick display.
print(str(brick.battery.current()) + "mA")
print(str(brick.battery.voltage()) + "mV")
brick.display.clear()
brick.display.text(str(brick.battery.current()) + "mA", (60, 50))
brick.display.text(str(brick.battery.voltage()) + "mV")


########## TESTING ##########
#############################

# Displaying the options of the colour sensors and brick buttons.
brick.display.text(str("Blue ^ Crane"), (60, 40))
brick.display.text(str("< Red Brown >"), (60, 50))
brick.display.text(str("White V Beams"), (60, 60))

# Using the colour sensor and brick buttons to choose missions - allows faster and easier mission selecting.
colour_sensor = ColorSensor(Port.S3)

while True: # Allows the program to keep running, so no time is wasted running the program itself
  while not (any(brick.buttons())): # Waiting until a button is pressed
    wait(10)
  # Mission 12
  if colour_sensor.color() == Color.GREEN:
    # Display mission number so we know what has been detected
    print("Blue")
    # Clockwise is probable order (i.e. UP -> RIGHT -> DOWN -> LEFT)
    if Button.UP in brick.buttons(): # Checking if the Button UP is pressed
      brick.display.clear()
      brick.display.text(str("Mission 12 Blue"), (60, 50)) # Displaying the mission on brick display for greater information to the user
      missions.Mission12.blue()
    elif Button.RIGHT in brick.buttons(): # Checking if the Button RIGHT is pressed
      brick.display.clear()
      brick.display.text(str("Mission 12 Brown/Elevator"), (60, 50)) 
      missions.Mission12.brown()
    elif Button.DOWN in brick.buttons(): # Checking if the Button DOWN is pressed
      brick.display.clear()
      brick.display.text(str("Mission 12 White"), (60, 50))  # Displaying the mission on brick display for greater information to the user
      missions.Mission12.white()
    elif Button.LEFT in brick.buttons(): # Checking if the Button LEFT is pressed
      brick.display.clear()
      brick.display.text(str("Mission 12 Red"), (60, 50)) 
      missions.Mission12.red() # 
    elif Button.CENTER in brick.buttons():  # In case colour sensor detects wrong colour, CENTER to exit loop.
      break

  # Mission 1,2 & 6/7/9
  elif colour_sensor.color() == Color.RED:
    # Display mission numbers so we know what has been detected
    print("Red")
    if Button.UP in brick.buttons(): # Checking if the Button UP is pressed
      brick.display.clear()
      brick.display.text(str("Mission 2"), (60, 50)) # Displaying the mission on brick display for greater information to the user
      missions.Mission2()
    elif Button.DOWN in brick.buttons(): # Checking if the Button DOWN is pressed
      brick.display.clear()
      brick.display.text(str("Mission 6/7/9"), (60, 50)) # Displaying the mission on brick display for greater information to the user
      missions.Mission9() 
     elif Button.LEFT in brick.buttons():
      pass # Mission 1
    elif Button.CENTER in brick.buttons():  # In case colour sensor detects wrong colour
      break
  brick.display.text(str("Blue ^ Crane"), (60, 40))
  brick.display.text(str("< Red Brown >"), (60, 50))
  brick.display.text(str("White V Beams"), (60, 60))
"""
left_colour_sensor = ColorSensor(Port.S1) # Ports of the sensors are given as a parameter.
right_colour_sensor = ColorSensor(Port.S2)
colour_sensor = ColorSensor(Port.S3) # Ports of the sensors are given as a parameter.
while True:
  print(left_colour_sensor.color(), right_colour_sensor.color(), colour_sensor.color())