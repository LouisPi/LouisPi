#!/usr/bin/python3

import RPi.GPIO as GPIO
import SimpleMFRC522
import os
import pickle
from squid import *
from button import *

rgb = Squid(18, 23, 24)

button = Button(17, debounce=0.1)

reader = SimpleMFRC522.SimpleMFRC522()

tags = {}

def flash(color, time_2):
    rgb.set_color(color)
    time.sleep(time_2)
    rgb.set_color(OFF)

def load_tags():
    global tags
    try:
        with open('id_tags.pickle', 'rb') as handle:
            tags = pickle.load(handle)
        # print("Loaded Tags")
        # print(tags)      
    except:
        pass
    
def save_tags():
    global tags
    print("Saving Tags")
    print(tags)
    with open('id_tags.pickle', 'wb') as handle:
        pickle.dump(tags, handle)
        
def add_person(id, name):
    global tags
    tags[id] = name
    save_tags()

def setup():
        for i in range(0, 1):
            name = input("Please enter your name: ")
            add_person(id, name)
            
load_tags()

try:
    for i in range(0,1):
        # print("Hold a tag next to the reader")
        id = reader.read_id()
        name = tags.get(id, None)
        if name:
            print("Hi " + name)
            if name == 'Louis':
                print("Hello Louis. Please check your app for all options")
                flash(GREEN, 5)
                while True:
                    if button.is_pressed():
                        break        
            else:
                print("Coding for this part in progress")
        else:
            print("Authentication failed!")
            flash(RED, 5)
            print("You haven't registered yet! Starting setup script")
            setup()

finally:
    print("See you later " + name)
    GPIO.cleanup()