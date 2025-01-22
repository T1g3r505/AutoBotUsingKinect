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
        board.exit()

    except KeyboardInterrupt:
        print(f"Error: {e1}")

def set_servo_angle(servoAngle, servoSeconds):
    """
    Set the servo to a specific angle with reversed output.
    :param servoAngle: Angle in degrees (0 to 180)
    :param servoSeconds: Time to delay after setting the angle
    """
    if 0 <= servoAngle <= 180:
        reversed_angle = 180 - servoAngle  # Reverse the angle
        board.digital[SERVO_PIN].write(reversed_angle)
        time.sleep(servoSeconds)  # Allow time for the servo to move
    else:
        print("Angle out of range. Please specify an angle between 0 and 180.")

if __name__ == "__main__":
    try:
        set_servo_angle(0, 0.05)
        print("Successfully Connected!\nResetting to default rotation (180 Degrees)")
        print("Enter speed {degree(s) per second(s)} and max angle:")
        degrees = int(input("Degree(s): "))
        seconds = float(input("Second(s): "))
        maxAngle = int(input("Max Angle: "))

        # Example usage: Sweep the servo back and forth
        while True:
            for angle in range(0, maxAngle, degrees):  # Sweep from 0 to maxAngle
                print(f"Rotating to {angle} degrees")
                set_servo_angle(angle, seconds)

            for angle in range(maxAngle, 0, -degrees):  # Sweep back from maxAngle to 0
                print(f"Rotating to {angle} degrees")
                set_servo_angle(angle, seconds)

    except KeyboardInterrupt:
        print("Exiting...")
        board.exit()
