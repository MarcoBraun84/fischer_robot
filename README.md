# Fischertechnik Robot Arm 9V Control with Raspberry Pi

This project involves controlling a Fischertechnik 9V robot arm using a Raspberry Pi. The project includes both software and hardware components to achieve full control of the robot arm through custom Python scripts and physical assembly of the robot arm using custom cases and parts.

## Requirements

To successfully complete the project, you will need the following components:

- **Fischertechnik Robot Arm**
- **Raspberry Pi 3 or 4**
- **SD Card**
- **Fischer Adapter PCB**(hardware/pcb/fischer_adapter.f3z)
- **Pi Adapter PCB**(hardware/pcb/pi_adapter.f3z)

## Project Structure

The repository is structured into two main sections:

- **Software**:
  - Contains all Python scripts necessary to control the robot arm, including motor control logic, GUI scripts, and sensor interfacing.
  - For detailed software setup and usage instructions, navigate to the `software/README.md` file.

- **Hardware**:
  - Contains CAD files, BOM, and assembly instructions for constructing the physical components
  - For detailed hardware setup and assembly instructions, navigate to the `hardware/README.md` file.

## Getting Started

### 1. **Software Setup**

To set up the software and control the robot arm via the Raspberry Pi:
1. Navigate to the `software/README.md` file for step-by-step instructions on installing the necessary Python libraries, running the control scripts, and using the GUI.
2. Ensure your Raspberry Pi is properly connected to the robot arm and follow the software guide to begin controlling the motors and sensors.

### 2. **Hardware Assembly**

To build the housing for the pi adapter and the mount for the fischer adapter:
1. Navigate to the `hardware/README.md` file for assembly instructions.
2. Review the Bill of Materials (BOM) and follow the step-by-step guide to assemble the components.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.