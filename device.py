import RPi.GPIO as GPIO
import time

# Define GPIO pins
PIN_CLK = 17  # Connect to rotary encoder A pin (CLK)
PIN_DT = 18   # Connect to rotary encoder B pin (DT)
PIN_SW = 27   # Optional, connect to push button pin (SW)

# Initialize GPIO mode
GPIO.setmode(GPIO.BCM)

# Set up pins as input with pull-up resistors
GPIO.setup(PIN_CLK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_DT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_SW, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Track the previous state
clk_last_state = GPIO.input(PIN_CLK)

# Define a counter to track the position
counter = 0

def rotary_callback(channel):
    global counter, clk_last_state
    clk_state = GPIO.input(PIN_CLK)
    dt_state = GPIO.input(PIN_DT)
    
    # If A (CLK) has changed, check B (DT) to determine direction
    if clk_state != clk_last_state:
        if dt_state != clk_state:
            counter += 1  # Clockwise rotation
            print("Rotated Right (Clockwise)")
        else:
            counter -= 1  # Counterclockwise rotation
            print("Rotated Left (Counterclockwise)")
        
        print(f"Position: {counter}")
    
    # Update last state for the next callback
    clk_last_state = clk_state

# Set up event detection on the CLK pin
GPIO.add_event_detect(PIN_CLK, GPIO.BOTH, callback=rotary_callback)

running = True
while running == True:
    # Detect button press if you wired the SW pin
    if GPIO.input(PIN_SW) == 0:
        print("Button pressed!")
        time.sleep(0.3)  # Debounce delay
        running =  False
    time.sleep(0.01)  # Small delay to avoid high CPU usage

GPIO.cleanup()  # Clean up GPIO on exit
