import RPi.GPIO as gpio
from time import time, sleep
from robot_utils import *
from threading import Thread, Event
from logger import Logger

class SoundSensor:

    def __init__(self, sample_time=10, detection_val=500) -> None:
        self.logger = Logger("Car-SoundSensor")
        # Sensor data
        self.pin = 16
        self.SAMPLE_TIME = sample_time
        self.DETECTION_VALUE = detection_val
        # Runtime
        self.currentMillis = 0
        self.lastMillis = 0
        self.elapsedMillis = 0
        self.sampleBufferValue = 0
        self.peakAmplitude = 0
        self.setup_done = False

    def setup(self):
        if not self.setup_done:
            gpio.setup(self.pin, gpio.IN)
            self.logger.success("Setup was successful.")
            self.setup_done = True

    def is_buzzer_detected(self) -> bool:
        self.currentMillis = time() * 1000  # in millis
        self.elapsedMillis = self.currentMillis - self.lastMillis

        if gpio.input(self.pin) == gpio.LOW:  # Sound has been detected
            self.sampleBufferValue += 1

        if self.elapsedMillis > self.SAMPLE_TIME:
            if self.sampleBufferValue > self.peakAmplitude:
                # Update peak value
                self.peakAmplitude = self.sampleBufferValue
            if self.sampleBufferValue >= self.DETECTION_VALUE:
                self.sampleBufferValue = 0
                self.lastMillis = self.currentMillis
                return True  # INFO: Buzzer has been detected
            self.sampleBufferValue = 0
            self.lastMillis = self.currentMillis
        return False


class LineFollowingSensor():

    def __init__(self, pin) -> None:
        self.logger = Logger("Car-LineFollowingSensor")
        self.pin = pin
        self.setup_done = False

    def setup(self):
        if not self.setup_done:
            gpio.setup(self.pin, gpio.IN)
            self.setup_done = True
            self.logger.success("Setup was successful.")

    def is_on_black_line(self):
        return gpio.input(self.pin) == 1


class Car:

    def __init__(self) -> None:
        self.logger = Logger("Car")
        # Driving pins
        self.pin_left = 1
        self.pin_right = 7
        self.pin_backward = 8
        self.pin_forward = 25
        # Runtime
        self.is_idle = True
        self.setup_done = False
        # Sensors
        self.soundSensor = SoundSensor(15, 100)
        self.leftLF = LineFollowingSensor(21)
        self.rightLF = LineFollowingSensor(20)
        # Inner vars
        self.auto_driver_switcher = Event()

    def setup(self):
        if not self.setup_done:
            self.logger.info("Setting up car...")
            # Setup gpio
            gpio.setmode(gpio.BCM)
            # Setup sensors
            self.soundSensor.setup()
            self.leftLF.setup()
            self.rightLF.setup()
            # Setup driving pins
            gpio.setup(self.pin_left, gpio.OUT)
            gpio.setup(self.pin_right, gpio.OUT)
            gpio.setup(self.pin_forward, gpio.OUT)
            gpio.setup(self.pin_backward, gpio.OUT)
            # Update runtime
            self.is_idle = True
            self.setup_done = True
            self.auto_driver_switcher.clear()
            self.logger.success("Setup was successful.")

    def cleanup(self):
        gpio.cleanup()

    @property
    def is_auto_driving(self):
        return self.auto_driver_switcher.is_set()

    def decide_direction(self, direction):
        if direction == Directions.CMD_DRIVE_FORWARD:
            self.drive_forward()
        elif direction == Directions.CMD_DRIVE_BACKWARD:
            self.drive_backward()
        elif direction == Directions.CMD_ROTATE_RIGHT:
            self.steer_right()
        elif direction == Directions.CMD_ROTATE_LEFT:
            self.steer_left()
        elif direction == Directions.CMD_STOP:
            self.activate_brakes()
        else:
            self.logger.warning(f"Can't decide which direction to go. Input: {direction}")

    def activate_brakes(self):
        gpio.output(self.pin_left, gpio.LOW)
        gpio.output(self.pin_right, gpio.LOW)
        gpio.output(self.pin_backward, gpio.LOW)
        gpio.output(self.pin_forward, gpio.LOW)
        self.logger.info("Stopped.")

    def drive_forward(self):
        gpio.output(self.pin_left, gpio.LOW)
        gpio.output(self.pin_right, gpio.LOW)
        gpio.output(self.pin_backward, gpio.LOW)
        gpio.output(self.pin_forward, gpio.HIGH)
        self.logger.info("Drive Forward.")

    def drive_backward(self):
        gpio.output(self.pin_left, gpio.LOW)
        gpio.output(self.pin_right, gpio.LOW)
        gpio.output(self.pin_backward, gpio.HIGH)
        gpio.output(self.pin_forward, gpio.LOW)
        self.logger.info("Drive Backward.")

    def steer_right(self):
        gpio.output(self.pin_left, gpio.LOW)
        gpio.output(self.pin_right, gpio.HIGH)
        gpio.output(self.pin_backward, gpio.LOW)
        gpio.output(self.pin_forward, gpio.LOW)
        self.logger.info("Rotated Right.")

    def steer_left(self):
        gpio.output(self.pin_left, gpio.HIGH)
        gpio.output(self.pin_right, gpio.LOW)
        gpio.output(self.pin_backward, gpio.LOW)
        gpio.output(self.pin_forward, gpio.LOW)
        self.logger.info("Rotated left.")

    def start_automatic_driving(self):
        if self.is_auto_driving:
            self.logger.warning("AutoDriver is already working !!")
            return
        # Create a CarComputerDriver and make it drive the car
        CarComputerDriver().drive_car(self)

    def stop_automatic_driving(self):
        if self.is_auto_driving:
            self.auto_driver_switcher.clear()


class CarComputerDriver:

    def drive_car(self, car: Car):
        car.logger.info("Initializing CarComputerDriver...")
        car.auto_driver_switcher.set()  # Turn switcher on
        Thread(name="CCD-Thread", target=self.__driver_job, args=[car]).start()

    def __driver_job(self, car: Car):
        car.logger.info("ComputerDriver is now driving the car.")
        lastPeakAmplitude = 0
        car.soundSensor.peakAmplitude = 0
        while car.auto_driver_switcher.is_set():
            if car.is_idle:  # INFO: To stop listening to buzzer while moving
                if car.soundSensor.peakAmplitude > lastPeakAmplitude:
                    lastPeakAmplitude = car.soundSensor.peakAmplitude
                    car.logger.info(
                        f"Detected Max-Amplitude of {lastPeakAmplitude} , Target is {car.soundSensor.DETECTION_VALUE}")
                if car.soundSensor.is_buzzer_detected():
                    car.is_idle = False
                    car.logger.info(f"{'=' * 50}\nBUZZER DETECTED !!!\n{'=' * 50}")
            else:
                lfReadings = (car.leftLF.is_on_black_line(), car.rightLF.is_on_black_line())
                car.logger.info(f"LF Readings: {lfReadings}")
                if lfReadings == (0, 0):  # INFO: (Left: WHITE, Right: WHITE)
                    car.drive_forward()
                elif lfReadings == (0, 1):  # INFO: (Left: WHITE, Right: BLACK)
                    car.steer_right()
                elif lfReadings == (1, 0):  # INFO: (Left: BLACK, Right: WHITE)
                    car.steer_left()
                elif lfReadings == (1, 1):  # INFO: (Left: BLACK, Right: BLACK)
                    car.activate_brakes()
                sleep(0.1)
        car.soundSensor.peakAmplitude = 0
        car.logger.info("ComputerDriver is no longer driving the car.")


class Motor:

    def __init__(self, jid: str, dtp: int):
        self.jid = jid
        self.d = dtp
        self.ag = 0

    def wag(self, ag: int, logger: Logger):
        if ag > 0:
            self.ag = min(ag, 180)
        elif ag < 0:
            self.ag = max(ag, -180)
        # todo: WRITE ANGLE TO MOTOR
        logger.success(f"{self.jid} moved to angle {self.ag}")


class Arm:

    def __init__(self):
        self.logger = Logger('Arm')
        # Servo motors
        self.jts = {
            'joint_1': Motor('joint_1', -1),
            'joint_2': Motor('joint_2', -1),
            'joint_3': Motor('joint_3', -1),
            'joint_4': Motor('joint_4', -1),
            'joint_5': Motor('joint_5', -1),
            'joint_6': Motor('joint_6', -1)
        }

    def handle_mv(self, arm_mv_spec):
        """
        :param arm_mv_spec: (jid, ag)
        """
        if len(arm_mv_spec) != 2:
            return
        if None in arm_mv_spec:
            return
        jid: str = arm_mv_spec[0]
        tgt: int = arm_mv_spec[1]
        jt: Motor = self.jts.get(jid, None)
        if jt is not None:
            jt.wag(tgt, self.logger)
