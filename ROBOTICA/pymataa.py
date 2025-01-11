from pymata4.pymata4 import Pymata4
import time


class MotorControl:
    def __init__(self):
        # Especificar el puerto manualmente
        self.board = Pymata4(com_port='/dev/tty.usbmodem2101')

        # Pines de control del motor
        self.motor1 = [6, 7, 8]  # ENA, IN1, IN2 para el Motor 1
        self.motor2 = [9, 10, 11]  # ENB, IN3, IN4 para el Motor 2

        # Configuración de la velocidad del motor
        self.MOTOR_SPEED = 100

        # Inicializar los pines y configuración
        self.setup()

        # Dirección inicial del motor
        self.motor_direction = 0

    def setup(self):
        # Configurar todos los pines como salida digital
        for pin in self.motor1 + self.motor2:
            self.board.set_pin_mode_digital_output(pin)

        # Configurar los pines PWM
        self.board.set_pin_mode_pwm_output(self.motor1[0])  # Motor 1 ENA (PWM pin)
        self.board.set_pin_mode_pwm_output(self.motor2[0])  # Motor 2 ENB (PWM pin)

    def start_motors(self):
        if self.motor_direction == 1:  # Mover a la derecha
            # Motor 1 Adelante
            self.board.pwm_write(self.motor1[0], self.MOTOR_SPEED)  # Velocidad (PWM)
            self.board.digital_write(self.motor1[1], 0)  # IN1 - Bajo
            self.board.digital_write(self.motor1[2], 1)  # IN2 - Alto

            # Motor 2 Adelante
            self.board.pwm_write(self.motor2[0], self.MOTOR_SPEED)  # Velocidad (PWM)
            self.board.digital_write(self.motor2[1], 1)  # IN3 - Bajo
            self.board.digital_write(self.motor2[2], 0)  # IN4 - Alto
        elif self.motor_direction == -1:  # Mover a la izquierda
            # Motor 1 Reversa
            self.board.pwm_write(self.motor1[0], self.MOTOR_SPEED)
            self.board.digital_write(self.motor1[1], 1)  # IN1 - Alto
            self.board.digital_write(self.motor1[2], 0)  # IN2 - Bajo

            # Motor 2 Reversa
            self.board.pwm_write(self.motor2[0], self.MOTOR_SPEED)
            self.board.digital_write(self.motor2[1], 0)  # IN3 - Alto
            self.board.digital_write(self.motor2[2], 1)  # IN4 - Bajo
        elif self.motor_direction == 0:
            self.board.digital_write(self.motor1[0], 0)  # Desactivar Motor 1
            self.board.digital_write(self.motor2[0], 0)  # Desactivar Motor 2

    def change_motor_direction(self):
        while True:
            self.motor_direction = -1
            print("Dirección del motor: Izquierda")
            self.start_motors()
            time.sleep(3)

            self.motor_direction = 0
            print("Dirección del motor: Detenido")
            self.start_motors()
            time.sleep(3)

            self.motor_direction = 1
            print("Dirección del motor: Derecha")
            self.start_motors()
            time.sleep(3)


def main():
    motor_control = MotorControl()
    motor_control.change_motor_direction()


if __name__ == '__main__':
    main()
