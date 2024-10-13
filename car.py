from gpiozero import Servo, RGBLED
from time import sleep

import socketio

alert_shot = False
servo = None
led = None
# Create a SocketIO client instance
sio = socketio.Client()

# Event handler for when the client successfully connects to the server
@sio.event
def connect():
    print('Connected to server!')

# Event handler for when the client disconnects from the server
@sio.event
def disconnect():
    print('Disconnected from server.')

@sio.on('alert')
def on_response(data):
    global alert_shot
    if not alert_shot:
        slowdown()
        alert_shot = True
    print(f"Received response from server: {data}")


def init_car():

    servo = Servo(17)
    led = RGBLED(red=2, green=3, blue=4)
    led.color=(1,1,1)
    servo.max()

def slowdown():
    duration = 3  # 3 seconds
    steps = 100   # The number of steps to take between max and min
    step_delay = duration / steps  # The delay between each step
    led.color=(1,0,0)
    for i in range(steps + 1):
        # Calculate the servo value (between 1 and -1)
        value = 1 - 2 * (i / steps)  # Starts at 1 and moves to -1
        servo.value = value
        sleep(step_delay)

if __name__ == "__main__":
    init_car()
    sio.connect('http://localhost:5000')
    pause()