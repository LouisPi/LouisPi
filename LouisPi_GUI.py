from guizero import App, yesno, Box, Text, PushButton
import RPi.GPIO as GPIO
import SimpleMFRC522
import os
import pickle
from squid import *
from button import *

app = App(title = "Louis OS", height = 480, width = 800)

reader = SimpleMFRC522.SimpleMFRC522()

tags = {}

button = Button(17, debounce=0.1)

rgb = Squid(18, 23, 24)

def test():
    print("Yay its working!")

def do_this_on_close():
    if yesno("Close", "Do you want to quit?"):
        app.destroy()
        print("Cleaning up")
        GPIO.cleanup()

def load_tags():
    global tags
    try:
        with open('id_tags.pickle', 'rb') as handle:
            tags = pickle.load(handle)
        print("Loaded Tags")
        print(tags)      
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
        
load_tags()
        
def setup():
        name = input("Please enter your name: ")
        print("Hold a tag next to the reader")
        id = reader.read_id()
        add_person(id, name)
        
def scan():
    while True:
        id = reader.read_id()
        name = tags.get(id, None)
        if name:
            print("Hi " + name)
            if name == 'Louis':
                print("Hello Louis. Please check your app for all options")
                flash(GREEN, 5)
                while True:
                    if button.is_pressed():
                        continue
            else:
                print("Coding for this part in progress")
                continue
        else:
            print("Authentication failed!")
            flash(RED, 5)

box = Box(app, layout = "grid")

button_one = PushButton(box, command = scan, icon='/home/pi/LouisPi/pictures/scan.gif', grid = [0,0])

button_two = PushButton(box, command = setup, icon='/home/pi/LouisPi/pictures/rfid_setup.gif', grid = [1,0])

button_three = PushButton(box, command = test, icon='/home/pi/LouisPi/pictures/settings.gif', grid = [1,1])

app.on_close(do_this_on_close)

app.display()
