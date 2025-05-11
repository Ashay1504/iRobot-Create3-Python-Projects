# iRobot Create 3 Python Projects (using EDU SDK)

Welcome! This repository contains a collection of Python projects developed for the iRobot Create 3 robot using the `irobot_edu_sdk`. Each script demonstrates different capabilities of the robot, from simple interactions to more complex navigation and game-like behaviors.

## Projects Included:

*   **`CodeBreaker.py`**:
    *   A game where the user tries to input a correct 5-digit code using the robot's touch buttons (1 & 2) and bumpers (3 & 4).
    *   The robot provides feedback through sounds and lights.
*   **`CollisionWarning.py`**:
    *   The robot moves forward and uses its IR proximity sensor (center-front) to detect obstacles.
    *   It slows down as it gets closer to an object and stops if too close, changing light colors and playing notes to indicate proximity.
    *   Can be stopped by pressing touch buttons or bumpers.
*   **`RobotPong.py`**:
    *   A "Pong"-like behavior where the robot moves forward and uses its IR array to detect an "object" (like a hand or wall).
    *   When an object is detected within a certain range, it calculates an approximate reflection angle and turns to "bounce" off.
    *   Lights change to indicate bounces. Can be stopped by touch buttons or bumpers.
*   **`AutonomousDelivery.py`** (assisted by `AuxAutonomousDelivery.py`):
    *   A more advanced navigation script where the robot attempts to reach a predefined `DESTINATION` coordinate.
    *   It includes logic for realignment, obstacle detection using IR sensors, and a basic form of wall-following/obstacle avoidance.
    *   The `AuxAutonomousDelivery.py` file contains helper functions for angle calculations and position checking.
*   **`MazeSolver.py`** (assisted by `AuxMazeSolver.py`):
    *   An ambitious project for a robot to autonomously navigate and solve a predefined grid-based maze.
    *   It uses a dictionary to represent the maze, updates cell costs using a Flood Fill like algorithm, and makes decisions based on sensor readings (IR for walls) and the current maze knowledge.
    *   `AuxMazeSolver.py` contains crucial helper functions for maze representation, neighbor finding, orientation, and cost updates.

## Prerequisites:

*   An iRobot Create 3 (or a compatible robot supported by the iRobot EDU SDK).
*   Python 3.7+ installed on your computer.
*   Bluetooth capability on your computer to connect to the robot.
*   The `irobot_edu_sdk` Python package.

## Setup:

1.  **Clone the repository:**
    ```bash
    git clone [<your-repository-url>](https://github.com/Ashay1504/iRobot-Create3-Python-Projects.git)
    cd iRobot-Create3-Python-Projects
    ```

2.  **Install the iRobot EDU SDK:**
    If you haven't already, install the SDK using pip:
    ```bash
    pip install irobot_edu_sdk
    ```

3.  **IMPORTANT: Update Robot Bluetooth Name:**
    *   Before running any script, you **MUST** update the Bluetooth name of your robot within the script.
    *   Open the Python file you want to run (e.g., `CodeBreaker.py`).
    *   Find the line:
        ```python
        robot = Create3(Bluetooth("Name")) # Or "SOPHIA", "C-3PO", etc.
        ```
    *   **Replace `"Name"` (or the placeholder name) with the actual Bluetooth name of YOUR iRobot.** This name is typically found on a sticker on the robot or can be seen when scanning for Bluetooth devices.

## How to Run a Project:

1.  Ensure your iRobot Create 3 is turned on and discoverable via Bluetooth.
2.  Navigate to the directory where you cloned the repository.
3.  Ensure you have updated the Bluetooth name in the script you wish to run (see Setup step 3).
4.  Run the desired Python script from your terminal:
    ```bash
    python CodeBreaker.py
    ```
    or
    ```bash
    python CollisionWarning.py
    ```
    ...and so on for the other scripts.

5.  The script will attempt to connect to your robot. Observe the terminal for print statements and the robot for its actions.
6.  To stop a script, you can usually press `Ctrl+C` in the terminal. Some scripts also have built-in stop conditions (e.g., pressing bumpers/buttons).

## Notes:

*   **Bluetooth Connection:** Establishing a Bluetooth connection can sometimes be tricky. Ensure your robot is close, powered on, and not connected to another device. If you have issues, try restarting the robot and your computer's Bluetooth.
*   **Sensor Calibration & Environment:** The performance of IR sensors can be affected by ambient light and the reflective properties of surfaces. Thresholds in scripts (e.g., `WALL_THRESHOLD` in `MazeSolver.py`, proximity values in `CollisionWarning.py`) might need adjustment for your specific environment.
*   **Coordinate System:** For projects like `AutonomousDelivery.py` and `MazeSolver.py` that use coordinates, be aware that the robot's internal coordinate system starts at (0,0) when it's powered on or when its pose is reset. The accuracy can drift over time and distance.
*   **Safety:** Always supervise your robot when running autonomous scripts, especially those involving movement, to prevent collisions with valuable objects or falls.
*   **Auxiliary Files:**
    *   `AutonomousDelivery.py` requires `AuxAutonomousDelivery.py` to be in the same directory.
    *   `MazeSolver.py` requires `AuxMazeSolver.py` to be in the same directory.

## Contributing:

Feel free to fork this repository, make improvements, or add new projects! Pull requests are welcome.

## License:

This project is open-source and available under the [MIT License](LICENSE).

