import time
import pyfirmata2

try:
    print("Establishing connection...")

    # Replace 'COM3' with your actual port (e.g., '/dev/ttyUSB0' for Linux/Mac)
    PORT = pyfirmata2.Arduino.AUTODETECT

    # Initialize the board
    board = pyfirmata2.Arduino(PORT)

    # Specify the pin connected to the servo (e.g., pin 9)
    SERVO_PIN = 9

    # Set up the pin for servo control
    board.digital[SERVO_PIN].mode = pyfirmata2.SERVO

except Exception as e1:
    print("Exiting...")

    try:
        board.exit() # NOQA

    except KeyboardInterrupt:
        print(f"Error: {e1}")

def set_servo_angle(servoAngle, servoSeconds):
    """
    Set the servo to a specific angle.
    :param servoAngle: Angle in degrees (0 to 180)
    """
    if 0 <= servoAngle <= 180:
        board.digital[SERVO_PIN].write(servoAngle)
        time.sleep(servoSeconds)  # Allow time for the servo to move
    else:
        print("Angle out of range. Please specify an angle between 0 and 180.")

def get_integer_input(prompt, min_value=None, max_value=None):
    while True:
        try:
            value = int(input(prompt))
            if (min_value is not None and value < min_value) or (max_value is not None and value > max_value):
                print(f"Please enter an integer between {min_value} and {max_value}.")
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter an integer.")

def get_float_input(prompt, min_value=None):
    while True:
        try:
            value = float(input(prompt))
            if min_value is not None and value < min_value:
                print(f"Please enter a value greater than or equal to {min_value}.")
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter a valid number.")

if __name__ == "__main__":
    try:
        print("Successfully Connected!\nResetting to default rotation (0 Degrees)")
        set_servo_angle(0, 0)

        print("Enter speed {degree(s) per second(s)} and max angle:")
        # Get degrees input
        degrees = get_integer_input("Degree(s): ", min_value=1, max_value=180)
        # Get seconds input
        seconds = get_float_input("Second(s): ", min_value=0.001)

        # Get maxAngle input
        while True:
            maxAngle = get_integer_input("Max Angle: ", min_value=1, max_value=180)
            if maxAngle > degrees:
                break
            print("Max Angle must be greater than degrees. Please try again.")

        print(f"Degrees: {degrees}, Seconds: {seconds}, Max Angle: {maxAngle}")



        # Example usage: Sweep the servo back and forth
        while True:
            for angle in range(0, maxAngle, degrees):  # Sweep from 0 to 180
                print(f"Rotating to {angle} degrees")
                set_servo_angle(angle, seconds)

            for angle in range(maxAngle, 0, -degrees):  # Sweep back from 180 to 0
                print(f"Rotating to {angle} degrees")
                set_servo_angle(angle, seconds)

    except KeyboardInterrupt:
        print("Exiting...")
        board.exit()
