from pymata4.pymata4 import Pymata4
import time

class RaspiController:
    def __init__(self):
        # Create an instance of the Pymata4 class
        self.board = Pymata4()

        # Motor control pins
        self.motor1 = [6, 7, 8]  # ENA, IN1, IN2 for Motor 1
        self.motor2 = [9, 10, 11]  # ENB, IN3, IN4 for Motor 2

        # Ultrasonic sensor pins
        self.TRIGGER_PIN = 2
        self.ECHO_PIN = 3

        # Motor speed and distance threshold configuration
        self.MOTOR_SPEED = 100
        self.DISTANCE_THRESHOLD = 10  # Stop motors if an object is closer than 10 cm

        # Initialize pins and sensors
        self.setup()

        # Initialize motor control state
        self.touchin_object = False
        self.motor_direction = 0  # 0: stop, 1: right, -1: left

    def setup(self):
        # Set all motor pins as outputs
        for pin in self.motor1 + self.motor2:
            self.board.set_pin_mode_digital_output(pin)

        self.board.set_pin_mode_pwm_output(self.motor1[0])  # Motor 1 ENA (PWM pin)
        self.board.set_pin_mode_pwm_output(self.motor2[0])  # Motor 2 ENB (PWM pin)

        # Set up ultrasonic sensor
        self.board.set_pin_mode_sonar(trigger_pin=self.TRIGGER_PIN, echo_pin=self.ECHO_PIN)

    def stop_motors(self):
        self.board.digital_write(self.motor1[0], 0)  # Disable Motor 1
        self.board.digital_write(self.motor2[0], 0)  # Disable Motor 2

    def start_motors(self):
        if self.motor_direction == 1:  # Move to the right
            # Motor 1 Forward
            self.board.pwm_write(self.motor1[0], self.MOTOR_SPEED)  # Set motor 1 speed (PWM)
            self.board.digital_write(self.motor1[1], 0)  # IN1 - Low
            self.board.digital_write(self.motor1[2], 1)  # IN2 - High

            # Motor 2 Forward
            self.board.pwm_write(self.motor2[0], self.MOTOR_SPEED)  # Set motor 2 speed (PWM)
            self.board.digital_write(self.motor2[1], 0)  # IN3 - Low
            self.board.digital_write(self.motor2[2], 1)  # IN4 - High
        elif self.motor_direction == -1:  # Move to the left
            # Motor 1 Reverse
            self.board.pwm_write(self.motor1[0], self.MOTOR_SPEED)  # Set motor 1 speed (PWM)
            self.board.digital_write(self.motor1[1], 1)  # IN1 - High
            self.board.digital_write(self.motor1[2], 0)  # IN2 - Low

            # Motor 2 Reverse
            self.board.pwm_write(self.motor2[0], self.MOTOR_SPEED)  # Set motor 2 speed (PWM)
            self.board.digital_write(self.motor2[1], 1)  # IN3 - High
            self.board.digital_write(self.motor2[2], 0)  # IN4 - Low
        else:
            self.stop_motors()

    def control_motors(self):
        # Read distance from ultrasonic sensor
        distance = self.board.sonar_read(self.TRIGGER_PIN)
        if distance is not None:
            # Print the distance
            print(f"Distance: {distance[0]} cm")

            # Motor control logic based on distance threshold
            if self.touchin_object:
                if distance[0] > self.DISTANCE_THRESHOLD:
                    self.stop_motors()
                    self.touchin_object = False
                    print("Motor stopped, object moved.")
            else:
                if distance[0] < self.DISTANCE_THRESHOLD:
                    print("Object detected! Pushing object.")
                    self.touchin_object = True
                    self.start_motors()
                else:
                    self.start_motors()

    def run(self):
        try:
            while True:
                self.control_motors()
                time.sleep(0.1)  # Control loop frequency
        except KeyboardInterrupt:
            self.stop_motors()
            self.board.shutdown()

# Create the RaspiController instance and run it
if __name__ == '__main__':
    controller = RaspiController()
    controller.run()
