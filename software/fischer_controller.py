import tkinter as tk
from threading import Thread
import time
import fischer_lib as fl

class MotorControllerApp:
    """
    Main class for creating the GUI motor controller.

    This class creates a Tkinter-based graphical interface for controlling the Fischer robot arm motors.
    It provides buttons for each motor to move clockwise, counterclockwise, or stop, along with
    real-time status updates for limit switches and rotation detection.
    """
    def __init__(self, root):
        """
        Initializes the GUI window and sets up motor controls and status updates.

        Args:
        - root (tk.Tk): The root window for the Tkinter GUI.
        """
        self.root = root
        self.root.title("Motor Controller")

        self.robi = fl.Robot()

        self.last_pressed_button = {
            self.robi.motor1: {'clockwise': None, 'counterclockwise': None, 'stop': None},
            self.robi.motor2: {'clockwise': None, 'counterclockwise': None, 'stop': None},
            self.robi.motor3: {'clockwise': None, 'counterclockwise': None, 'stop': None},
            self.robi.motor4: {'clockwise': None, 'counterclockwise': None, 'stop': None},
        }

        self.motor_count = 1

        self.create_header()
        self.create_auto_home_button()
        self.motor1_frame, self.limit_switch_label1, self.rotation_detection_label1 = self.create_motor_frame("Motor 1", self.robi.motor1, self.robi.m1_limit_switch, self.robi.m1_rotation_dect)
        self.motor2_frame, self.limit_switch_label2, self.rotation_detection_label2 = self.create_motor_frame("Motor 2", self.robi.motor2, self.robi.m2_limit_switch, self.robi.m2_rotation_dect)
        self.motor3_frame, self.limit_switch_label3, self.rotation_detection_label3 = self.create_motor_frame("Motor 3", self.robi.motor3, self.robi.m3_limit_switch, self.robi.m3_rotation_dect)
        self.motor4_frame, self.limit_switch_label4, self.rotation_detection_label4 = self.create_motor_frame("Motor 4", self.robi.motor4, self.robi.m4_limit_switch, self.robi.m4_rotation_dect)

        self.update_status_thread = Thread(target=self.update_status, daemon=True)
        self.update_status_thread.start()

    def create_header(self):
        """
        Creates the header for the GUI window, displaying the title.
        """
        header_label = tk.Label(self.root, text="Fischer Roboterarm x Pi", font=("Helvetica", 18, "bold"))
        header_label.grid(row=0, column=2, pady=10)

    def create_auto_home_button(self):
        """
        Creates a button in the GUI for the "Auto Home" feature, which moves all motors to their home positions.
        """
        auto_home_button = tk.Button(self.root, text="Auto Home", command=self.robi.auto_home, bg='gray')
        auto_home_button.grid(row=0, column=4, padx=10, pady=10)

    def create_motor_frame(self, motor_label, motor, limit_switch, rotation_detection):
        """
        Creates a control panel for a motor, including buttons for clockwise, counterclockwise, stop, and status indicators.

        Args:
        - motor_label (str): The label for the motor (e.g., "Motor 1").
        - motor (Motor): The motor object to control.
        - limit_switch (Input): The limit switch associated with the motor.
        - rotation_detection (Input): The rotation detection sensor for the motor.

        Returns:
        - frame (tk.Frame): The frame containing the motor control panel.
        - limit_switch_label (tk.Label): Label displaying the current state of the limit switch.
        - rotation_detection_label (tk.Label): Label displaying the current count of rotations.
        """
        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.grid(row=1, column=self.motor_count)

        self.motor_count += 1

        label = tk.Label(frame, text=motor_label, font='bold')
        label.pack()

        clockwise_button = tk.Button(frame, text="Clockwise", command=lambda: self.button_pressed(motor, 'clockwise'), state=tk.NORMAL, bg='gray')
        clockwise_button.pack(pady=5)

        counterclockwise_button = tk.Button(frame, text="Counterclockwise", command=lambda: self.button_pressed(motor, 'counterclockwise'), state=tk.NORMAL, bg='gray')
        counterclockwise_button.pack(pady=5)

        stop_button = tk.Button(frame, text="Stop", command=lambda: self.button_pressed(motor, 'stop'), state=tk.NORMAL, bg='red')
        stop_button.pack(pady=5)

        self.last_pressed_button[motor]['clockwise'] = clockwise_button
        self.last_pressed_button[motor]['counterclockwise'] = counterclockwise_button
        self.last_pressed_button[motor]['stop'] = stop_button

        limit_switch_header = tk.Label(frame, text="\nLimit Switch", font='bold')
        limit_switch_header.pack()

        limit_switch_label = tk.Label(frame, text=f"{limit_switch.state()}")
        limit_switch_label.pack()

        rotation_detection_header = tk.Label(frame, text="\nRotation Detection", font='bold')
        rotation_detection_header.pack()

        rotation_detection_label = tk.Label(frame, text=f"{rotation_detection.counter()}")
        rotation_detection_label.pack()

        reset_button = tk.Button(frame, text="Reset Counter", command=lambda: self.reset_counter(rotation_detection), bg='gray')
        reset_button.pack(pady=5)

        return frame, limit_switch_label, rotation_detection_label

    def button_pressed(self, motor, action):
        """
        Handles motor control button presses and triggers motor movement or stops the motor.

        Args:
        - motor (Motor): The motor to control.
        - action (str): The action to perform ('clockwise', 'counterclockwise', or 'stop').
        """
        if action == 'clockwise':
            motor.clockwise()
            self.update_button_color(motor, 'clockwise', 'green')
        elif action == 'counterclockwise':
            motor.counterclockwise()
            self.update_button_color(motor, 'counterclockwise', 'green')
        elif action == 'stop':
            motor.stop()
            self.update_button_color(motor, 'stop', 'red')

    def update_button_color(self, motor, button_type, color):
        """
        Resets the color of previously pressed buttons and updates the color of the currently pressed button.

        Args:
        - motor (Motor): The motor being controlled.
        - button_type (str): The type of button pressed ('clockwise', 'counterclockwise', or 'stop').
        - color (str): The color to apply to the pressed button.
        """
        for btn_type, button in self.last_pressed_button[motor].items():
            if btn_type != button_type:
                button.config(bg='gray')

        current_pressed_button = self.last_pressed_button[motor][button_type]
        current_pressed_button.config(bg=color)

    def reset_counter(self, counter):
        """
        Resets the rotation counter of a motor.

        Args:
        - counter (Input): The rotation counter sensor for the motor.
        """
        counter.reset()

    def update_status(self):
        """
        Continuously updates the status of the limit switches and rotation detection labels for all motors.
        Runs in a separate thread.
        """
        while True:
            self.limit_switch_label1.config(text=f"{self.robi.m1_limit_switch.state()}")
            self.limit_switch_label2.config(text=f"{self.robi.m2_limit_switch.state()}")
            self.limit_switch_label3.config(text=f"{self.robi.m3_limit_switch.state()}")
            self.limit_switch_label4.config(text=f"{self.robi.m4_limit_switch.state()}")

            self.rotation_detection_label1.config(text=f"{self.robi.m1_rotation_dect.counter()}")
            self.rotation_detection_label2.config(text=f"{self.robi.m2_rotation_dect.counter()}")
            self.rotation_detection_label3.config(text=f"{self.robi.m3_rotation_dect.counter()}")
            self.rotation_detection_label4.config(text=f"{self.robi.m4_rotation_dect.counter()}")

            time.sleep(0.2)
