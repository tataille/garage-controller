import RPi.GPIO as gpio
import threading
import time
from signal import signal, SIGINT
from sys import exit

LED = 12 #Définit le numéro du port GPIO qui alimente la led
button=16
timeout=100

def handler(signal_received, frame):
    # on gère un cleanup propre
    print('')
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    gpio.cleanup()
    exit(0)

def push():
    gpio.output(LED, gpio.LOW) #On l’éteint
    
    print("press")
    gpio.output(14, gpio.LOW)
    gpio.output(LED, gpio.HIGH) #On l'allume
    time.sleep(0.5)
    print("release")
    gpio.output(14, gpio.HIGH)
    gpio.output(LED, gpio.LOW) #On l'éteind

def check_button():
    while 1:
        if (gpio.input(button) == 1):
            push()
        time.sleep(timeout/1000)


def init():
    # on passe en mode BMC qui veut dire que nous allons utiliser directement
    # le numero GPIO plutot que la position physique sur la carte
    gpio.setmode(gpio.BCM)

    # defini le port GPIO 4 comme etant une sortie output
    gpio.setup(14, gpio.OUT, initial=1)
    gpio.setup(LED, gpio.OUT, initial=0) #Active le contrôle du GPIO
    gpio.setup(button, gpio.IN)
    gpio.add_event_detect(button, gpio.RISING, callback=push, bouncetime=200)
    signal(SIGINT, handler)
