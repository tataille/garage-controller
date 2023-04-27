import RPi.GPIO as gpio
import time
from signal import signal, SIGINT
from sys import exit

LED = 12 #Définit le numéro du port GPIO qui alimente la led

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
    gpio.output(LED, gpio.LOWD) #On l'allume


def init():
    # on passe en mode BMC qui veut dire que nous allons utiliser directement
    # le numero GPIO plutot que la position physique sur la carte
    gpio.setmode(gpio.BCM)

    # defini le port GPIO 4 comme etant une sortie output
    gpio.setup(14, gpio.OUT, initial=1)
    gpio.setup(LED, gpio.OUT, initial=0) #Active le contrôle du GPIO

    signal(SIGINT, handler)

    # Mise a 1 pendant 2 secondes puis 0 pendant 2 seconde
    # while True:
    #     print("on")
    #     gpio.output(14, gpio.HIGH)
    #     time.sleep(0.7)
    #     print("off")
    #     gpio.output(14, gpio.LOW)
    #     time.sleep(2)
