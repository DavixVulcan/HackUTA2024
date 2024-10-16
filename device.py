from gpiozero import RotaryEncoder, Button, TonalBuzzer
from gpiozero.tones import Tone
from time import sleep
from signal import pause
import socketio

# Set up the rotary encoder
encoder = None  # pin_a and pin_b are used

# Optional: Set up the push button if your encoder has one
button = None
buzzer = None


position = 0

bloodtrue = 0
heartrate = 80
bloodpressure = 115
bloodoxy = 97

def get_heartrate():
    global heartrate
    return heartrate

def get_bloodpressure():
    global bloodpressure
    return bloodpressure

def get_bloodoxygen():
    global bloodoxy
    return bloodoxy

# Function to handle the rotary encoder's movement
def rotary_moved():
    global position
    global bloodpressure
    global heartrate
    global bloodoxy
    global bloodtrue
    additive = 0
    if encoder.steps < position:
        print("Rotated Right (Clockwise)")
        additive = 1
    else:
        print("Rotated Left (Counterclockwise)")
        additive = -1
    position = encoder.steps
    print(f"Position: {encoder.steps}")

    if bloodtrue == 0:
        bloodpressure += additive
    elif bloodtrue == 1:
        heartrate += additive
    else:
        bloodoxy += additive

    print(f"bloodpressure: {bloodpressure}")
    print(f"heartrate: {heartrate}")
    print(f"bloocoxy: {bloodoxy}")

# Function to handle button press
def button_pressed():
    print("Button pressed!")
    global bloodtrue
    bloodtrue += 1
    if bloodtrue == 3:
        bloodtrue = 0

# Assign event handlers for movement and button press
# encoder.when_rotated = rotary_moved
# button.when_pressed = button_pressed

def initialize_gpio():
    global encoder, button, buzzer
    if encoder is None and button is None and buzzer is None:
        encoder = RotaryEncoder(a=17, b=18, max_steps=0)
        button = Button(27, bounce_time=0.1)
        buzzer = TonalBuzzer(15)
        encoder.when_rotated = rotary_moved
        button.when_pressed = button_pressed

def alert():
    melody = ["C4", "D4", "C4", "D4", "C4", "D4"]

    for note in melody:
        buzzer.play(Tone(note))  # Play each note in the melody
        sleep(0.05)  # Hold the note for half a second
        buzzer.stop()
        sleep(0.01) 
# Set up a client for WebSocket communication
sio = socketio.Client()

@sio.event
def connect():
    print('Connected to server!')

@sio.event
def disconnect():
    print('Disconnected from server.')

# Function to send a message via WebSocket
def send_message_to_server(message):
    sio.emit('message', message)

def send_stream_to_server(message):
    sio.emit('stream', message)

if __name__ == "__main__":
    initialize_gpio()
    alert()
    sio.connect('http://localhost:5000')
    while True:
        if get_heartrate() > 100:
            send_message_to_server(f'Heartrate: {get_heartrate()}')
            alert()
        
        if get_bloodpressure() > 120:
            send_message_to_server(f'Bloodpressure: {get_bloodpressure()}')
            alert()
        
        if get_bloodoxygen() < 90:
            send_message_to_server(f'Bloodoxygen: {get_bloodoxygen()}')
            alert()
        sleep(.5)
        send_stream_to_server(f"{{\"Heartrate\": {get_heartrate()}, \"Bloodpressure\": {get_bloodpressure()}, \"Bloodoxygen\": {get_bloodoxygen()}}}")