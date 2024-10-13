from gpiozero import RotaryEncoder, Button
from signal import pause

# Set up the rotary encoder
encoder = RotaryEncoder(pin_a=17, pin_b=18, max_steps=0)  # pin_a and pin_b are used

# Optional: Set up the push button if your encoder has one
button = Button(27)

# Function to handle the rotary encoder's movement
def rotary_moved():
    if encoder.steps > 0:
        print("Rotated Right (Clockwise)")
    else:
        print("Rotated Left (Counterclockwise)")
    
    print(f"Position: {encoder.steps}")

# Function to handle button press
def button_pressed():
    print("Button pressed!")

# Assign event handlers for movement and button press
encoder.when_rotated = rotary_moved
button.when_pressed = button_pressed

# Keep the program running
pause()
