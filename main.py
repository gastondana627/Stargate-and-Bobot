# main.py

import pygame
import os
from config import *
import config  # Import the entire module
#from game_logic import  get_game_state, game_state # Function to access game state

# Initialize Pygame
pygame.init()
pygame.font.init()  # Initialize font module

# Font setup
font = pygame.font.Font(None, 36)

# You have set the global grid size.

# I just need to set this.

# Setting Global Surfaces - IMPORTANT THIS NEEDS TO BE OUTSIDE.

# Make everything fit here so if needed can always reload in place.
def newGrid():
    """Functions to Set the screen"""
    CELL_SIZE = 40
    GRID_SIZE = 6
 #Make sure when you set the width to have that value and how all functions can see you properly.
def generate_frame(game_state):
    """Generates a single game frame as a Pygame Surface."""
    #Note we want this as small and modular as possible, as all we need is to "draw"
    #the frame.

    #Access global variables
    global robot_img, moonrock_img, stargate_img, screen, font, CELL_SIZE, WIDTH, HEIGHT

    #Accessing the variable from the script to print from different locations.
    newGrid()#Calling
    WIDTH, HEIGHT = GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE#Setting the screen

    screen = pygame.display.set_mode((WIDTH, HEIGHT))# Setting the screen now after setting what the varibles are, and its the proper order now
    pygame.display.set_caption("Moonrock Collection Game")#Name

    screen.fill(BLACK)# Fill the screen with a black background

    for x in range(0, WIDTH, CELL_SIZE):# Iterating the with.
        for y in range(0, HEIGHT, CELL_SIZE):#Iterating the Heigh
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GRAY, rect, 1)# Draw the rectangle on the screen

   # Draw Stargate zone as a 2x2 area
    for stargate_cell in game_state["stargate_zone"]:# Iterate on the star zone for multiple zones
        screen.blit(stargate_img, (stargate_cell[0] * CELL_SIZE, stargate_cell[1] * CELL_SIZE))

    # Draw moonrocks from the global set
    for rock in game_state["moonrocks"]:#Call it.
        screen.blit(moonrock_img, (rock[0] * CELL_SIZE, rock[1] * CELL_SIZE))

    # Draw robot (based on robot_position)
    robot_position = game_state["robot_position"] # Robot initial position, and initial state set.

    screen.blit(robot_img, (robot_position[0] * CELL_SIZE, robot_position[1] * CELL_SIZE))

    # Display Score
    score = game_state["score"] # Access from the dictionary to be more readable.
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # To check the test status and has is happening with the current and all that is going on.
    carrying = game_state["carrying_rock"]#Set a carry value then set a  if for the code.

    # Get time remaining
    time_remaining = game_state["time_remaining"]
    # Display a variable that is loaded at the top from config with all those settings.
    time_text = font.render(f"Time: {int(time_remaining)}", True, WHITE)
    screen.blit(time_text, (WIDTH - 150, 10)) # To have all data on the image what the user wants at the right place.

    # Display Carrying Status
    carrying_text = font.render(f"Carrying: {'Yes' if carrying else 'No'}", True, WHITE)
    screen.blit(carrying_text, (10, 40)) # If the robot was carrying, display.

    # Convert to a format Streamlit can display.
    return screen

def load_images():
    """Load and scale images, handling potential errors."""
    # Load and scale images
    try:
        # **DEBUGGING: Print paths immediately before loading**
        print("Loading robot image from:", ROBOT_IMAGE_PATH)
        robot_img = pygame.image.load(ROBOT_IMAGE_PATH)
        robot_img = pygame.transform.scale(robot_img, (CELL_SIZE, CELL_SIZE))

        print("Loading moonrock image from:", MOONROCK_IMAGE_PATH)
        moonrock_img = pygame.image.load(MOONROCK_IMAGE_PATH)
        moonrock_img = pygame.transform.scale(moonrock_img, (CELL_SIZE, CELL_SIZE))

        print("Loading stargate image from:", STARGATE_IMAGE_PATH)
        stargate_img = pygame.image.load(STARGATE_IMAGE_PATH)
        stargate_img = pygame.transform.scale(stargate_img, (CELL_SIZE * 2, CELL_SIZE * 2)) # To generate 2x2 zone

    except pygame.error as e:
        print(f"Error loading image: {e}")
        pygame.quit()
        exit()
    except FileNotFoundError as e:
        print(f"File not found: {e.filename}")
        print("Ensure file names are correctly spelled and match case sensitivity.")
        pygame.quit()
        exit()

    return robot_img, moonrock_img, stargate_img

robot_img, moonrock_img, stargate_img = load_images() # Setting the global scope at the end

def quit_pygame(): #Quitting when everything is done.
    pygame.quit()




