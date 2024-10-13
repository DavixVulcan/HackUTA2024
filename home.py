from gpiozero import RGBLED
from time import sleep

# Set up the RGB LED on GPIO pins
# Adjust GPIO pin numbers for red, green, and blue as needed
led = RGBLED(red=2, green=3, blue=4)

# Set the initial color (fully off)
led.color = (0, 0, 0)

# Function to cycle through some colors
def cycle_colors():
    # Full red
    led.color = (1, 0, 0)
    print("Red")
    sleep(1)
    
    # Full green
    led.color = (0, 1, 0)
    print("Green")
    sleep(1)

    # Full blue
    led.color = (0, 0, 1)
    print("Blue")
    sleep(1)

    # Yellow (red + green)
    led.color = (1, 1, 0)
    print("Yellow")
    sleep(1)

    # Cyan (green + blue)
    led.color = (0, 1, 1)
    print("Cyan")
    sleep(1)

    # Magenta (red + blue)
    led.color = (1, 0, 1)
    print("Magenta")
    sleep(1)

    # White (red + green + blue)
    led.color = (1, 1, 1)
    print("White")
    sleep(1)

    # Dim white (half brightness)
    led.color = (0.5, 0.5, 0.5)
    print("Dim white")
    sleep(1)

    # Turn off the LED
    led.color = (0, 0, 0)
    print("LED off")
    sleep(1)

# Cycle through colors
while True:
    cycle_colors()
