#!/usr/bin/env pybricks-micropython

# from pybricks import ev3brick as brick
# from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.ev3devices import (Motor, ColorSensor)
# from pybricks.parameters import (Port, Stop, Direction, Button, Color, SoundFile, ImageFile, Align)
from pybricks.parameters import (Port, Stop, Direction)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase

def angleToDistance(angle):
  return angle / 360 * 196.035381584

def distanceToAngle(distance):
  return distance * 360 / 196.035381584

def accelerate(start_power, final_power, delay, distance, speed_increment, stop: bool, correct: bool):
  current_power = start_power
  if speed_increment == 0:
    speed_increment = abs(final_power - start_power) / distance * 8
  left_motor.reset_angle(0)
  right_motor.reset_angle(0)
  try:
    direction_coefficient = final_power / abs(final_power)
  except ZeroDivisionError:
    direction_coefficient = start_power / abs(start_power)
  while (abs(current_power) < abs(final_power) if abs(current_power) <= abs(final_power) else abs(current_power) > abs(final_power)):
    robot.drive(current_power, 0)
    if ((abs(start_power) <= abs(final_power)) or (abs(start_power) > abs(final_power) and abs(current_power) > 20)):
      print("speed increment:", str(speed_increment), "increase:", speed_increment * direction_coefficient * (1  if abs(current_power) <= abs(final_power) else -1))
      current_power += (speed_increment * direction_coefficient * (1  if abs(current_power) <= abs(final_power) else -1))
    print("moving, power", str(current_power), "left rotations", str(left_motor.angle()), "right rotations", str(right_motor.angle()), "left distance", str(angleToDistance(left_motor.angle())), "right distance", str(angleToDistance(right_motor.angle())), "continue?", (angleToDistance(abs(left_motor.angle())) < distance))
    wait(delay)
    if ((abs(angleToDistance(left_motor.angle())) >= distance) or (angleToDistance(abs(right_motor.angle())) >= distance)):
      break
  while not ((angleToDistance(abs(left_motor.angle())) >= distance) or (angleToDistance(abs(right_motor.angle())) >= distance)):
    wait(delay)
  if stop:
    robot.stop(Stop.HOLD)
    if correct:
      correctRotation(distance)

def move(steering, speed, amount, stop: bool, correct: bool):
  # left_motor.reset_angle(0)
  # right_motor.reset_angle(0)
  # robot.drive(speed, steering)
  # while (angleToDistance(abs(left_motor.angle())) < amount and angleToDistance(abs(right_motor.angle())) < amount):
  #   wait(10)
  # if stop:
  #   robot.stop(Stop.BRAKE)
  #   if steering == 0 and correct:
  #     correctRotation(amount)

  # speed is in mm/s and steering is in degrees/s so time can be calculated
  if speed > steering:
    time = amount / speed
  else:
    time = amount / steering
  robot.drive_time(speed, steering, time)
  # TODO: now turn() isn't needed??

def turn(steering, speed, time):
  robot.drive_time(speed, steering, time)

def correctRotation(distance):
  left_motor_degrees_remaining = abs(left_motor.angle()) - distanceToAngle(distance)
  right_motor_degrees_remaining = abs(right_motor.angle()) - distanceToAngle(distance)
  print("left motor degrees remaining:", str(left_motor_degrees_remaining))
  print("right motor degrees remaining:", str(right_motor_degrees_remaining))
  if (left_motor_degrees_remaining != 0):
    left_motor.reset_angle(0)
    left_motor.run_angle(5, left_motor_degrees_remaining, Stop.HOLD)
  elif (right_motor_degrees_remaining != 0):
    right_motor.reset_angle(0)
    right_motor.run_angle(5, right_motor_degrees_remaining, Stop.HOLD)

def lineFollow(forward: bool, perfect_line_threshold: int):
  run = True
  speed = 50 if forward else -50
  error = 0
  last_error = 0
  integral = 0
  derivative = 0
  kp = 1.2
  ki = 0.0075
  kd = 20
  perfect_steering = 0
  
  while run:
    error = left_colour_sensor.reflection() - right_colour_sensor.reflection()
    integral += error
    derivative = error - last_error
    steering = error * kp + integral * ki + derivative * kd
    if (-2 < steering < 2 and perfect_line_threshold != 0):
      perfect_steering += 1
      if (perfect_line_threshold <= perfect_steering):
        run = False
    else:
      robot.drive(speed, steering)
    last_error = error
  robot.stop(Stop.HOLD)

left_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.D, Direction.COUNTERCLOCKWISE)
robot = DriveBase(left_motor, right_motor, 62.4, 96.5)
left_colour_sensor = ColorSensor(Port.S1)
right_colour_sensor = ColorSensor(Port.S2)