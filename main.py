import pygame
import os
from config import *
import config  # Import the entire module
from game_logic import  get_game_state, game_state # Function to access game state

# Initialize Pygame
pygame.init()
pygame.font.init()  # Initialize font module

# Font setup
font = pygame.font.Font(None, 36)

screen = None  # Initialize as None, it is a surface

def initialize_display():
    """Initializes the Pygame display."""
    global screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Moonrock Collection Game")

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
    stargate_img = pygame.transform.scale(stargate_img, (CELL_SIZE * 2, CELL_SIZE * 2)) # Multiply so that 2x2

except pygame.error as e:
    print(f"Error loading image: {e}")
    pygame.quit()
    exit()
except FileNotFoundError as e:
    print(f"File not found: {e.filename}")
    print("Ensure file names are correctly spelled and match case sensitivity.")
    pygame.quit()
    exit()

def generate_frame():
    """Generates a single game frame as a Pygame Surface."""
    global robot_img, moonrock_img, stargate_img, robot_img, font, screen

    if screen is None: #Calling only once instead of multiple times.
        initialize_display()

    # Get the game state from the logic
    returned_game_state = get_game_state() # Access from the getter function

    # Draw grid lines
    screen.fill(BLACK) # Fill screen with black in the background

    for x in range(0, WIDTH, CELL_SIZE): #Looping the size for the width and heigh in grid size
        for y in range(0, HEIGHT, CELL_SIZE):
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GRAY, rect, 1) # Draw the rectangle on the screen

    # Draw Stargate zone as a 2x2 area, using game state.
    # This may make more sense to move into game logic.
    for stargate_cell in returned_game_state["stargate_zone"]: # Looping through the stargate zones
        screen.blit(stargate_img, (stargate_cell[0] * CELL_SIZE, stargate_cell[1] * CELL_SIZE))

    # Draw moonrocks from the global set
    for rock in returned_game_state["moonrocks"]:
        screen.blit(moonrock_img, (rock[0] * CELL_SIZE, rock[1] * CELL_SIZE))

    # Draw robot (based on robot_position)
    robot_position = returned_game_state["robot_position"]

    screen.blit(robot_img, (robot_position[0] * CELL_SIZE, robot_position[1] * CELL_SIZE))

    # Display Score
    score = returned_game_state["score"] # Getting score from the dictionary to be more readable.
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Display Carrying Status
    carrying = returned_game_state["carrying_rock"]
    carrying_text = font.render(f"Carrying: {'Yes' if carrying else 'No'}", True, WHITE)
    screen.blit(carrying_text, (10, 40))

    # Convert to a format Streamlit can display
    return screen

def quit_pygame():
    pygame.quit()
