import pygame
import os

# Initialize Pygame
pygame.init()

# Check for audio device
audio_enabled = True
try:
    pygame.mixer.init()
except pygame.error:
    audio_enabled = False

# Constants
GRID_SIZE = 8
CELL_SIZE = 80

# Load assets
ASSET_DIR = "Graphics_Audio"
IMG_DIR = os.path.join(ASSET_DIR, "img")
SND_DIR = os.path.join(ASSET_DIR, "aud")

robot_img = pygame.image.load(os.path.join(IMG_DIR, "robot.png"))
moonrock_img = pygame.image.load(os.path.join(IMG_DIR, "moonrock.png"))
stargate_img = pygame.image.load(os.path.join(IMG_DIR, "Stargate.png"))

if audio_enabled:
    pickup_sound = pygame.mixer.Sound(os.path.join(SND_DIR, "a_robot_beeping.wav"))
    drop_sound = pygame.mixer.Sound(os.path.join(SND_DIR, "a_robot_beeping-2.wav"))

# Game variables
robot_pos = [0, 0]
moonrocks = [[2, 3], [5, 6]]
stargate = [[7, 7], [7, 6]]
carrying = False
score = 0

# Game screen
screen = pygame.Surface((GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE))

def draw_grid():
    """Draws the game elements."""
    screen.fill((0, 0, 0))  # Black background
    
    for rock in moonrocks:
        screen.blit(moonrock_img, (rock[0] * CELL_SIZE, rock[1] * CELL_SIZE))

    for gate in stargate:
        screen.blit(stargate_img, (gate[0] * CELL_SIZE, gate[1] * CELL_SIZE))

    screen.blit(robot_img, (robot_pos[0] * CELL_SIZE, robot_pos[1] * CELL_SIZE))

def generate_frame():
    """Creates and returns a game frame."""
    draw_grid()
    return screen
