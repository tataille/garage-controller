import RPi.GPIO as GPIO
import sys
import time

led=1

def start():
    try:
      GPIO.setmode(GPIO.BCM)
      GPIO.setwarnings(False)
      GPIO.setup(led, GPIO.OUT)
      GPIO.output(led, 0)
      count = 0
      while True:
        GPIO.output(led, 1)
        time.sleep(1)
        GPIO.output(led, 0)
        time.sleep(1)
    except:
      print(sys.exc_info()[0])
      raise
    finally:
      self.stop()

def stop():
    GPIO.output(led, 0)
    GPIO.cleanup()
    sys.exit(0)

def _handle_sigterm(self, sig, frame):
    self.logger.warning('SIGTERM received...')
    self.stop()

if __name__ == '__main__':
    start()
