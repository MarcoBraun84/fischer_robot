import RPi.GPIO as GPIO
import threading
import time

# GPIO-Initialization
GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)

# GPIO-Pin-Assignment
D_M1_positive = 23
D_M1_negative = 27
D_M2_positive = 15
D_M2_negative = 22
D_M3_positive = 18
D_M3_negative = 10
D_M4_positive = 17
D_M4_negative = 9
D_T1 = 11
D_T2 = 1
D_T3 = 0
D_T4 = 5
D_T5 = 12
D_T6 = 6
D_E1 = 13
D_E2 = 19

# Thresholds
M1_Limit = 1700
M2_Limit = 1500
M3_Limit = 200
M4_Limit = 28

class Robot:
    """
    Main class for controlling the robot arm.

    The Robot class initializes and manages four motors and their associated limit switches
    and rotation sensors. It provides methods to control motor movements and homing functionality.
    """
    def __init__(self):
        """
        Initializes the Robot object by setting up motors and sensors for all four axes.
        """
        self.m1_limit_switch = Input(D_T1, None)
        self.m2_limit_switch = Input(D_T2, None)
        self.m3_limit_switch = Input(D_T3, None)
        self.m4_limit_switch = Input(D_T5, None)
        self.m1_rotation_dect = Input(D_E1, None)
        self.m2_rotation_dect = Input(D_E2, None)
        self.m3_rotation_dect = Input(D_T4, None)
        self.m4_rotation_dect = Input(D_T6, None)

        self.motor1 = Motor(D_M1_positive, D_M1_negative, self.m1_limit_switch, self.m1_rotation_dect, M1_Limit)
        self.motor2 = Motor(D_M2_positive, D_M2_negative, self.m2_limit_switch, self.m2_rotation_dect, M2_Limit)
        self.motor3 = Motor(D_M3_positive, D_M3_negative, self.m3_limit_switch, self.m3_rotation_dect, M3_Limit)
        self.motor4 = Motor(D_M4_positive, D_M4_negative, self.m4_limit_switch, self.m4_rotation_dect, M4_Limit)

        self.m1_limit_switch.motor = self.motor1
        self.m2_limit_switch.motor = self.motor2
        self.m3_limit_switch.motor = self.motor3
        self.m4_limit_switch.motor = self.motor4
        self.m1_rotation_dect.motor = self.motor1
        self.m2_rotation_dect.motor = self.motor2
        self.m3_rotation_dect.motor = self.motor3
        self.m4_rotation_dect.motor = self.motor4

        self.m1_rotation_dect.start()
        self.m2_rotation_dect.start()
        self.m3_rotation_dect.start()
        self.m4_rotation_dect.start()

    def auto_home(self):
        """
        Automatically moves all four motors clockwise to home the robot arm by hitting the limit switches.
        """
        self.motor1.clockwise()
        self.motor2.clockwise()
        self.motor3.clockwise()
        self.motor4.clockwise()

class Motor:
    """
    Class for controlling an individual motor of the robot arm.

    It controls motor movement (clockwise, counterclockwise), and monitors motor limits and rotations.
    """
    def __init__(self, pin_positive, pin_negative, limit_switch, rotation_switch, range):
        """
        Initializes the motor with the GPIO pins for forward and backward movement, limit and rotation switches,
        and the range for counterclockwise movement.

        Args:
        - pin_positive (int): GPIO pin for clockwise movement.
        - pin_negative (int): GPIO pin for counterclockwise movement.
        - limit_switch (Input): The limit switch for stopping motor.
        - rotation_switch (Input): The sensor tracking motor rotation.
        - range (int): The maximum allowable rotation for counterclockwise movement.
        """
        self.pin_positive = pin_positive
        self.pin_negative = pin_negative
        self.limit_switch = limit_switch
        self.rotation_switch = rotation_switch
        self.range = range

        self.is_running = False
        self.state = "stop"

        GPIO.setup(pin_positive, GPIO.OUT)
        GPIO.setup(pin_negative, GPIO.OUT)
        GPIO.output(self.pin_positive, GPIO.LOW)
        GPIO.output(self.pin_negative, GPIO.LOW)

        self.lock = threading.Lock()

        self.limit_thread = threading.Thread(target=self._check_limits)
        self.limit_thread.daemon = True
        self.limit_thread.start()

    def _check_limits(self):
        """
        Continuously monitors motor's limit switch and rotation counter to stop movement when necessary.
        This method runs in a background thread.
        """
        while True:
            with self.lock:
                if self.is_running:
                    if not self.limit_switch.state() and self.state == "clockwise":
                        self.rotation_switch.reset()
                        self.stop()
                    elif (self.rotation_switch.counter() > self.range) and self.state == "counterclockwise":
                        self.stop()
                time.sleep(0.1)

    def clockwise(self):
        """
        Moves the motor in the clockwise direction if the limit switch is not triggered.
        """
        if self.limit_switch.state():
            GPIO.output(self.pin_positive, GPIO.HIGH)
            GPIO.output(self.pin_negative, GPIO.LOW)
            self.state = "clockwise"
            self.is_running = True

    def counterclockwise(self):
        """
        Moves the motor in the counterclockwise direction if the rotation counter is below the allowed range.
        """
        if self.rotation_switch.counter() < self.range:
            GPIO.output(self.pin_positive, GPIO.LOW)
            GPIO.output(self.pin_negative, GPIO.HIGH)
            self.state = "counterclockwise"
            self.is_running = True

    def stop(self):
        """
        Stops the motor by setting both control GPIO pins to LOW.
        """
        GPIO.output(self.pin_positive, GPIO.LOW)
        GPIO.output(self.pin_negative, GPIO.LOW)
        self.state = "stop"
        self.is_running = False

class Input:
    """
    Class for handling input from sensors (limit switches and rotation sensors).

    It tracks motor rotations and the state of limit switches.
    """
    def __init__(self, pin, motor):
        """
        Initializes an input object for a sensor.

        Args:
        - pin (int): The GPIO pin connected to the sensor.
        - motor (Motor): The motor object associated with this sensor.
        """
        self.pin = pin
        self.count = 0
        self.motor = motor
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def _count_flank(self, channel):
        """
        Callback function triggered by a GPIO interrupt to count motor rotations.
        """
        if self.motor.state == "clockwise":
            self.count -= 1
        elif self.motor.state == "counterclockwise":
            self.count += 1

    def start(self):
        """
        Starts rotation detection by enabling GPIO interrupt on the sensor's pin.
        """
        self.count = 0
        GPIO.add_event_detect(self.pin, GPIO.RISING, callback=self._count_flank)

    def counter(self):
        """
        Returns the current rotation count.
        """
        return self.count

    def state(self):
        """
        Returns the current state of the limit switch (True if activated, False otherwise).
        """
        return GPIO.input(self.pin)

    def stop(self):
        """
        Stops rotation detection by removing the GPIO interrupt on the sensor's pin.
        """
        GPIO.remove_event_detect(self.pin)

    def reset(self):
        """
        Resets the rotation counter to 0.
        """
        self.count = 0