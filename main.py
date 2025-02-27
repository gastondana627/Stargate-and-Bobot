import streamlit as st
import pygame
import numpy as np
import os

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Load assets
GRID_SIZE = 8
CELL_SIZE = 80

# Paths for graphics & audio
ASSET_DIR = "Graphics_Audio"
IMG_DIR = os.path.join(ASSET_DIR, "img")
SND_DIR = os.path.join(ASSET_DIR, "audio")

# Load images
robot_img = pygame.image.load(os.path.join(IMG_DIR, "robot.png"))
moonrock_img = pygame.image.load(os.path.join(IMG_DIR, "moonrock.png"))
stargate_img = pygame.image.load(os.path.join(IMG_DIR, "Stargate.png"))

# Load sounds
pickup_sound = pygame.mixer.Sound(os.path.join(SND_DIR, "a_robot_beeping.wav"))
drop_sound = pygame.mixer.Sound(os.path.join(SND_DIR, "a_robot_beeping-2.wav"))

# Game State
robot_pos = [0, 0]
moonrocks = [[2, 3], [5, 6]]  # Example positions
stargate = [[7, 7], [7, 6]]  # 2x2 area
carrying = False
score = 0

# Initialize game screen
screen = pygame.Surface((GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE))

def draw_grid():
    """Draws the game grid and elements on the screen."""
    screen.fill((0, 0, 0))  # Black background
    
    # Draw moonrocks
    for rock in moonrocks:
        screen.blit(moonrock_img, (rock[0] * CELL_SIZE, rock[1] * CELL_SIZE))

    # Draw Stargate
    for gate in stargate:
        screen.blit(stargate_img, (gate[0] * CELL_SIZE, gate[1] * CELL_SIZE))

    # Draw robot
    screen.blit(robot_img, (robot_pos[0] * CELL_SIZE, robot_pos[1] * CELL_SIZE))

def move_robot(dx, dy):
    """Moves the robot within grid bounds."""
    global robot_pos
    new_x, new_y = robot_pos[0] + dx, robot_pos[1] + dy
    
    if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
        robot_pos = [new_x, new_y]

def pick_up():
    """Handles picking up a moonrock."""
    global carrying
    if not carrying:
        for rock in moonrocks:
            if rock == robot_pos:
                carrying = True
                moonrocks.remove(rock)
                pickup_sound.play()
                break

def drop():
    """Handles dropping a moonrock at the Stargate."""
    global carrying, score
    if carrying and robot_pos in stargate:
        carrying = False
        score += 1
        drop_sound.play()

def generate_frame():
    """Creates a frame with game elements and returns it as an image."""
    draw_grid()

    # Score & carrying status
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    carrying_text = font.render(f"Carrying: {'Yes' if carrying else 'No'}", True, (255, 255, 255))

    screen.blit(score_text, (10, 10))
    screen.blit(carrying_text, (10, 50))

    return screen

def quit_pygame():
    """Handles quitting Pygame."""
    pygame.quit()

# Streamlit UI
st.title("Moonrock Collection Game")
st.write("Use the buttons below to control the robot:")

col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("⬅ Left"):
        move_robot(-1, 0)
with col2:
    if st.button("⬆ Up"):
        move_robot(0, -1)
    if st.button("⬇ Down"):
        move_robot(0, 1)
with col3:
    if st.button("➡ Right"):
        move_robot(1, 0)

if st.button("Pick Up"):
    pick_up()
if st.button("Drop"):
    drop()

# Display Game Screen
frame = generate_frame()
st.image(pygame.surfarray.pixels3d(frame), use_container_width=True)
