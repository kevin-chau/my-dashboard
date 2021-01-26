import RPi.GPIO as GPIO
import signal
import sys
import time
import datetime
from tkinter import *
import pygame

# Definitions
BUTTON_PIN = 23
BUTTON_PIN2 = 24
counter = 0
reset = 0
alarm_time = f"08:00:00"

# Setup pins
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(BUTTON_PIN2, GPIO.IN, pull_up_down = GPIO.PUD_UP)

# Turn off the LED at shutdown and clean up.
def shutdown(signal, frame):
  GPIO.cleanup()
  sys.exit(0)

# Handles button presses.
def button_press(channel):
  global counter

  if (GPIO.input(channel) == False):
    counter = counter + 1
    print("Counter: " + str(counter))

def button_press2(channel):
  global reset
  if (GPIO.input(channel) == False):
    print("RESET")
    reset = 1

# Add button press handler.
GPIO.add_event_detect(BUTTON_PIN, edge = GPIO.BOTH, callback = button_press, bouncetime = 300)
GPIO.add_event_detect(BUTTON_PIN2, edge = GPIO.BOTH, callback = button_press2, bouncetime = 300)

# Main entry point.
signal.signal(signal.SIGINT, shutdown)

def alarm(set_alarm_timer):
  global curr_counter
  global reset
  curr_counter = 0
  print("The alarm has been set to:")
  print(set_alarm_timer)
  #current_time = datetime.datetime.now()
  #date = current_time.strftime("%d/%m/%Y")
  #print("The Set Date is:",date)
  while True:
    time.sleep(1)
    current_time = datetime.datetime.now()
    now = current_time.strftime("%H:%M:%S")
    #print("Current time: " + now)
    print(time.ctime(), end="\r", flush=True)
    if now == set_alarm_timer:
      print("Time to Wake up")
      pygame.mixer.init()
      pygame.mixer.music.load("alarm.mp3")
      pygame.mixer.music.set_volume(1.0)
      pygame.mixer.music.play(loops = -1)

      while pygame.mixer.music.get_busy() == True:
        time.sleep(0.1)
        if reset == 1:
          print("ALARM TURNED OFF RESETING FOR TOMORROW")
          pygame.mixer.music.stop()
          reset = 0
          alarm(alarm_time)
        if curr_counter != counter:
          pygame.mixer.music.stop()
          # Snooze
          print("SNOOZE HIT")
          time.sleep(10)
          pygame.mixer.music.play(loops = -1) 
          curr_counter = counter
      break

# MAIN
alarm(alarm_time)


