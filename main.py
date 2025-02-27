import pygame
import os

# Get the current working directory
cwd = os.getcwd()

# Construct the absolute path to the images
robot_img_path = os.path.join(cwd, "Graphics_Audio", "img", "robot.png")
moonrock_img_path = os.path.join(cwd, "Graphics_Audio", "img", "moonrock.png")
stargate_img_path = os.path.join(cwd, "Graphics_Audio", "img", "stargate.png")

# Print the absolute paths to verify them
print(f"Robot image path: {robot_img_path}")
print(f"Moonrock image path: {moonrock_img_path}")
print(f"Stargate image path: {stargate_img_path}")

from game_logic import move_robot, pick_up_rock, drop_rock, get_game_state, GRID_SIZE

pygame.init()

# Screen and grid settings (keep these but don't run the loop)
CELL_SIZE = 80
WIDTH, HEIGHT = GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Initialize here but don't use the loop
pygame.display.set_caption("Moonrock Collection Game")

# Load and scale images
try:
    robot_img = pygame.image.load(robot_img_path)  # Use the absolute path
    robot_img = pygame.transform.scale(robot_img, (CELL_SIZE, CELL_SIZE))

    moonrock_img = pygame.image.load(moonrock_img_path)  # Use the absolute path
    moonrock_img = pygame.transform.scale(moonrock_img, (CELL_SIZE, CELL_SIZE))

    stargate_img = pygame.image.load(stargate_img_path)  # Use the absolute path
    stargate_img = pygame.transform.scale(stargate_img, (CELL_SIZE * 2, CELL_SIZE * 2))
except pygame.error as e:
    print(f"Error loading image: {e}")
    pygame.quit()
    exit()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
GREEN = (0, 200, 0)
GOLD = (255, 215, 0)

# Font setup
font = pygame.font.Font(None, 36)

def generate_frame():
    """Generates a single game frame as a Pygame Surface."""
    global robot_img, moonrock_img, stargate_img, robot_img, font
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
