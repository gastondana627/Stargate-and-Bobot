# Moonrock Collection Game

A simple game developed using Python with Pygame for the game logic and Streamlit for the user interface.  Players control a robot to collect moonrocks and deliver them to a stargate within a time limit.

## Table of Contents

*   [Overview](#overview)
*   [Features](#features)
*   [Requirements](#requirements)
*   [Installation](#installation)
*   [How to Run](#how-to-run)
*   [Game Instructions](#game-instructions)
*   [File Structure](#file-structure)
*   [Configuration](#configuration)
*   [Contributing](#contributing)
*   [License](#license)

## Overview

This game utilizes Pygame for the game engine and rendering and Streamlit to create a web application, allowing users to interact with the game through a browser.  The objective is to guide a robot to pick up moonrocks scattered around a grid and drop them off at a designated stargate zone before the timer runs out.  A high score system tracks the fastest completion times.

## Features

*   **Interactive Gameplay:** Control the robot using on-screen buttons.
*   **Timer:** A countdown timer adds a sense of urgency.
*   **Score Tracking:** The game tracks your score (number of moonrocks delivered).
*   **High Score System:** Saves and displays the top 5 fastest completion times.
*   **Randomized Elements:** Moonrock and stargate locations are randomized for each game.
*   **Welcome/Game Over Screens:** A simple UI to start the game and display game over information.
*   **Sound Effects:** (Optional) Adds sound effects for picking up and dropping off moonrocks.
*   **Responsive UI**: Built with Streamlit, the UI adapts to different screen sizes.

## Requirements

Before running the game, ensure you have the following installed:

*   **Python:** (version 3.6 or higher)
*   **Pygame:** `pip install pygame`
*   **Streamlit:** `pip install streamlit`
*   **Pillow (PIL):** `pip install Pillow`  (for image handling)

## Installation

1.  **Clone the repository:**

    ```bash
    git clone [repository URL]
    cd [repository directory]
    ```

2.  **Create a virtual environment (optional but recommended):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3.  **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

## How to Run

1.  **Navigate to the directory containing `streamlit_app.py`.**
2.  **Run the Streamlit app:**

    ```bash
    streamlit run streamlit_app.py
    ```

    This command will open the game in your default web browser.

## Game Instructions

1.  **Enter your name:**  On the welcome screen, enter your name in the "Your Name" field.
2.  **Set the time limit:**  Adjust the "Game Time Limit (seconds)" field to your desired game duration.
3.  **Start the Game:** Click the "Start Game" button.
4.  **Control the Robot:** Use the on-screen arrow buttons (Up, Down, Left, Right) to move the robot.
5.  **Pick Up Moonrocks:**  Move the robot onto a cell containing a moonrock and click the "Pick Up" button.  The robot can only carry one moonrock at a time.
6.  **Deliver to Stargate:** Move the robot onto a cell within the stargate zone (the 2x2 area).  Click the "Drop" button to deliver the moonrock.
7.  **Score:**  Each successful delivery to the stargate increases your score.
8.  **Win or Lose:** The game ends when you either collect all moonrocks and deliver them to the stargate or when the timer reaches zero.
9.  **High Score:** If you win, you have the option to save your completion time to the high score list.

## File Structure



## Configuration

The `config.py` file contains several constants that you can modify to adjust the game's behavior:

*   `CELL_SIZE`: The size of each cell in the game grid (in pixels).
*   `GRID_SIZE`: The number of cells in each dimension of the grid.
*   `ROBOT_IMAGE_PATH`, `MOONROCK_IMAGE_PATH`, `STARGATE_IMAGE_PATH`:  Paths to the image files.
*   `PICKUP_SOUND_PATH`, `DROP_SOUND_PATH`, `BACKGROUND_MUSIC_PATH`: Paths to the sound files.
*   `WHITE`, `BLACK`, `GRAY`, `GREEN`, `GOLD`: Color definitions.
*   `INITIAL_MOONROCK_COUNT`: Number of moonrocks that spawn each game.
*	`STARGATE_SIZE`: Dimension of the stargate (2x2)

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.  When contributing, please follow these guidelines:

*   Write clear and concise code.
*   Add comments to explain complex logic.
*   Test your changes thoroughly.
*   Follow the existing code style.

## License

This project is licensed under the [MIT License](LICENSE).  See the `LICENSE` file for details.
