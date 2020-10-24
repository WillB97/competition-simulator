from typing import Tuple

from controller import Robot


class MotorBase:
    def __init__(self, webot: Robot, motor_name: str) -> None:
        self.motor_name = motor_name
        self.webot_motor = webot.getMotor(motor_name)
        self.max_speed = self.webot_motor.getMaxVelocity()


class Wheel(MotorBase):

    def __init__(self, webot: Robot, motor_name: str) -> None:
        super().__init__(webot, motor_name)
        self.webot_motor.setPosition(float('inf'))
        self.webot_motor.setVelocity(0)

    def set_speed(self, speed):
        self.webot_motor.setVelocity(speed)


class LinearMotor(MotorBase):

    def __init__(self, webot: Robot, motor_name: str) -> None:
        super().__init__(webot, motor_name)
        self.webot_motor.setPosition(0)
        self.webot_motor.setVelocity(0)

    def set_speed(self, speed):
        motor = self.webot_motor
        if speed < 0:
            motor.setPosition(motor.getMinPosition() + 0.01)
        else:
            motor.setPosition(motor.getMaxPosition())
        motor.setVelocity(abs(speed))


class Gripper(MotorBase):

    def __init__(self, webot: Robot, motor_names: Tuple[str, str]) -> None:
        self.webot = webot
        self.gripper_motors = [
            LinearMotor(self.webot, name) for name in motor_names
        ]
        self.max_speed = self.gripper_motors[0].max_speed

    def set_speed(self, speed):
        for motor in self.gripper_motors:
            motor.set_speed(speed)
