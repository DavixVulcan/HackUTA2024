from gpiozero import RotaryEncoder, Button
from signal import pause

# Set up the rotary encoder
encoder = RotaryEncoder(a=17, b=18, max_steps=0)  # pin_a and pin_b are used

# Optional: Set up the push button if your encoder has one
button = Button(27)

position = 0

bloodtrue = True
heartrate = 100
bloodpressure = 100

# Function to handle the rotary encoder's movement
def rotary_moved():
    global position
    global bloodpressure
    global heartrate
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

    if bloodtrue:
        bloodpressure += additive
    else:
        heartrate += additive

    print(f"bloodpressure: {bloodpressure}")
    print(f"heartrate: {heartrate}")

# Function to handle button press
def button_pressed():
    print("Button pressed!")
    bloodtrue = not bloodtrue

# Assign event handlers for movement and button press
encoder.when_rotated = rotary_moved
button.when_pressed = button_pressed

# Keep the program running
pause()
