import pygame
import os

# Get the directory of the current script (main.py)
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to the images relative to the script directory
robot_img_path = os.path.join(script_dir, "Graphics_Audio", "img", "robot.png")
moonrock_img_path = os.path.join(script_dir, "Graphics_Audio", "img", "moonrock.png")
stargate_img_path = os.path.join(script_dir, "Graphics_Audio", "img", "stargate.png")

# Initialize Pygame
pygame.init()
pygame.font.init() # Initialize font module

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
GREEN = (0, 200, 0)
GOLD = (255, 215, 0)

# Font setup
font = pygame.font.Font(None, 36)

# Keep these in global scope, but don't initialize the screen yet
CELL_SIZE = 80
GRID_SIZE = 8
WIDTH, HEIGHT = GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE
screen = None # Initialize as None

from game_logic import move_robot, pick_up_rock, drop_rock, get_game_state, GRID_SIZE

# Load and scale images
try:
    # **DEBUGGING: Print paths immediately before loading**
    print("Loading robot image from:", robot_img_path)
    robot_img = pygame.image.load(robot_img_path)
    robot_img = pygame.transform.scale(robot_img, (80, 80)) # Assuming 80 is the cell size

    print("Loading moonrock image from:", moonrock_img_path)
    moonrock_img = pygame.image.load(moonrock_img_path)
    moonrock_img = pygame.transform.scale(moonrock_img, (80, 80))

    print("Loading stargate image from:", stargate_img_path)
    stargate_img = pygame.image.load(stargate_img_path)
    stargate_img = pygame.transform.scale(stargate_img, (160, 160)) # Assuming 160 is the stargate size
except pygame.error as e:
    print(f"Error loading image: {e}")
    pygame.quit()
    exit()

def generate_frame():
    """Generates a single game frame as a Pygame Surface."""
    global robot_img, moonrock_img, stargate_img, robot_img, font, screen

    # Initialize screen if not already initialized
    if screen is None:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Moonrock Collection Game")

    # Get the game state from the logic
    game_state = get_game_state()
    robot_position = game_state["robot_position"]
    moonrocks = game_state["moonrocks"]
    score = game_state["score"]
    carrying_rock = game_state["carrying_rock"]

    screen.fill(BLACK)  # Set background color to black

    # Draw grid lines
    for x in range(0, WIDTH, CELL_SIZE):
        for y in range(0, HEIGHT, CELL_SIZE):
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GRAY, rect, 1)

    # Draw Stargate zone as a 2x2 area
    stargate_top_left = (6, 6)
    screen.blit(stargate_img, (stargate_top_left[0] * CELL_SIZE, stargate_top_left[1] * CELL_SIZE))

    # Draw moonrocks from the global set
    for rock in moonrocks:
        screen.blit(moonrock_img, (rock[0] * CELL_SIZE, rock[1] * CELL_SIZE))

    # Draw robot (based on robot_position)
    screen.blit(robot_img, (robot_position[0] * CELL_SIZE, robot_position[1] * CELL_SIZE))

    # Display Score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Display Carrying Status
    carrying_text = font.render(f"Carrying: {'Yes' if carrying_rock else 'No'}", True, WHITE)
    screen.blit(carrying_text, (10, 40))

    # Convert to a format Streamlit can display
    return screen

def quit_pygame():
    pygame.quit()
