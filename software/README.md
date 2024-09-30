# fischer x pi - Software

This file includes the software setup, description and usage instructions.

# Setup

1. **Install Raspberry Pi OS on sd card**
    - (Legacy, 64-bit) Debian Bullseye with seqruity updates and desktop environment
    - Bookworm is not working with Rpi.GPIO lib!

2. **Create directory**

    Open terminal and run:
    ```zsh
    mkdir git
    cd git
    ```

3. **Clone repository from git**
    - ssh - Add ssh key in user settings
    - https - Add acces token with read access in user settings
    ```zsh
    git clone <url>
    ```
    The url can be found via the blue field

4. **Create virtual envrionment**
    ```zsh
    cd fischer_roboter
    python3 -m venv .venv
    ```

5. **Activate virtual environment**
    ```zsh
    source .venv/bin/activate
    ```

6. **Install requirements**
    ```zsh
    pip3 install -r requirements.txt
    ```

# fischer_main.py

The `fischer_main.py` script serves as the entry point for launching the graphical user interface (GUI) to control the Fischer robot arm using the `fischer_controller.py` script. It is a sample code to illustrate the use of the `fischer_lib.py`. It initializes the Tkinter window and starts the `MotorControllerApp`, which provides the interface for controlling the robot arm's motors and monitoring its limit switches and rotation counters.

## USAGE

To run the GUI and control the Fischer robot arm, follow these steps:

1. **Do the Setup**
    - Not necessary if already done
2. **Connect the Fischer robot arm**
    - Ensure the robot arm's motors and sensors are correctly connected to the adapter pcb
    - Check if the connection cable to the RaspberryPi is plugged the right way round.

3. **Run the application**

    Open new terminal in Desktop Environment:
    ```zsh
    cd git/fischer_robot
    source .venv/bin/activate
    python3 fischer_main.py
    ```

# fischer_lib.py

This library provides functionality to control a Fischer robot arm using a Raspberry Pi. The robot arm's motors and sensors are managed using the GPIO pins on the Pi, allowing control of arm movements and monitoring of the arm's position using limit switches and rotation counters.

## GPIO Pin Mapping

The following GPIO pins on the Raspberry Pi are used to control the motors and read input from limit switches and rotation sensors:

- **Motor control pins**
    | Motor | Positive | Negative |
    |:-----:|:--------:|:--------:|
    |   M1  |  GPIO 23 |  GPIO 27 |
    |   M2  |  GPIO 15 |  GPIO 22 |
    |   M3  |  GPIO 18 |  GPIO 10 |
    |   M4  |  GPIO 17 |  GPIO 9  |

- **Sensor pins**
  - Limit switches: T1, T2, T3, T5
  - Rotation sensors: E1, E2, T4, T6

## Classes and Methods

### 1. `Robot` Class

The `Robot` class is the main class that encapsulates the robot arm's behavior. It manages the motors and sensors of the robot and provides methods to control and home the robot arm.

#### Methods:

- **`__init__(self)`**:
  Initializes the robot, configuring its motors and limit switches. Starts threads for monitoring rotation and limits.

- **`auto_home(self)`**:
  Automatically homes the robot by rotating all motors in the clockwise direction until the limit switches are activated.

### 2. `Motor` Class

The `Motor` class controls individual motors of the robot arm. It provides methods to move the motors in both directions and monitors limit switches to ensure safe operation.

#### Methods:

- **`__init__(self, pin_plus, pin_minus, limit_switch, rotation_switch, range)`**:
  Initializes a motor with its GPIO pins for forward and backward movement, as well as associated limit and rotation switches.

- **`_check_limits(self)`**:
  Continuously checks the state of the motor's limit switch and rotation counter to stop the motor when necessary.

- **`clockwise(self)`**:
  Moves the motor in the clockwise direction.

- **`counterclockwise(self)`**:
  Moves the motor in the counterclockwise direction.

- **`stop(self)`**:
  Stops the motor by setting both motor control pins to LOW.

### 3. `Input` Class

The `Input` class handles sensor inputs from the limit switches and rotation sensors. It tracks the rotation of the motors and detects when a motor has reached its end position.

#### Methods:

- **`__init__(self, pin, motor)`**:
  Initializes an input sensor with its GPIO pin and the motor it is associated with.

- **`_count_flank(self, channel)`**:
  A callback function triggered by a GPIO interrupt to count motor rotations.

- **`start(self)`**:
  Starts the rotation detection by adding an event detect on the GPIO pin.

- **`counter(self)`**:
  Returns the current count of motor rotations.

- **`state(self)`**:
  Returns the state of the limit switch (whether it is triggered or not).

- **`stop(self)`**:
  Stops the rotation detection by removing the event detect.

- **`reset(self)`**:
  Resets the rotation counter to 0.

## Usage Example

Here is an example of how to use the `fischer_lib.py` library to control the Fischer robot arm:

```python
from fischer_lib import Robot

# Initialize the robot
robot = Robot()

# Move the robot arm to the home position
robot.auto_home()

# Control individual motors
robot.motor1.clockwise()  # Move motor 1 clockwise
time.sleep(1)             # Wait for 1 second
robot.motor1.stop()       # Stop motor 1
```

# fischer_controller.py

This project provides a graphical interface for controlling the motors of a Fischer robot arm using a Raspberry Pi. The graphical user interface (GUI) is built using Tkinter, and it allows for manual motor control as well as status monitoring of the limit switches and rotation sensors.

## GUI Layout

The GUI is divided into control panels for each motor, with the following components:

- **Motor Control Buttons**
    - **Clockwise**: Moves the motor clockwise.
    - **Counterclockwise**: Moves the motor counterclockwise.
    - **Stop**: Stops the motor.

- **Status Indicators**
    - **Limit Switch**: Displays the state of the motor's limit switch.
    - **Rotation Detection**: Displays the current rotation count of the motor.

- **Auto Home Button**: Moves all motors to their home position.

- **Reset Counter Button**: Resets the rotation detection counter for a motor.

## Classes and Methods

### 1. `MotorControllerApp` Class

This is the main class that creates the GUI for controlling the robot's motors. It initializes the GUI window and manages the control buttons for the motors as well as status updates for the limit switches and rotation sensors.

#### Methods:

- **`__init__(self, root)`**: Initializes the GUI and motor control components. It sets up buttons for each motor and starts a thread to continuously update the motor's status.

- **`create_header(self)`**: Creates the header for the GUI window, displaying the title "Fischer Roboterarm x Pi".

- **`create_auto_home_button(self)`**: Adds an "Auto Home" button to the GUI, which triggers the robot's `auto_home` function to automatically move the motors to their home positions.

- **`create_motor_frame(self, motor_label, motor, limit_switch, rotation_detection)`**: Creates a control panel for an individual motor. Each panel includes buttons for clockwise, counterclockwise, and stop actions. It also displays the current status of the limit switch and rotation detection sensor.

- **`button_pressed(self, motor, action)`**: Handles motor control button presses, triggering the appropriate action (clockwise, counterclockwise, or stop) for the motor.

- **`update_button_color(self, motor, button_type, color)`**: Resets the color of previously pressed buttons and updates the color of the currently pressed button to indicate the active action.

- **`reset_counter(self, counter)`**: Resets the rotation counter of the motor.

- **`update_status(self)`**: Continuously updates the status of the limit switches and rotation detection labels for all motors in real-time. This method runs in a separate thread.

## Usage
Start the GUI by running the `fischer_main.py` Python script.