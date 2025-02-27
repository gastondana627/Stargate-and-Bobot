# game_logic.py
# game_logic.py
import pygame
import random

# Grid dimensions
GRID_SIZE = 8

# Initialize robot position
robot_position = (0, 0)
carrying_rock = False
score = 0

# Define Stargate Zone (2x2)
STARGATE_ZONE = {(6, 6), (6, 7), (7, 6), (7, 7)}

# Generate random moonrock positions ensuring they don't overlap with the Stargate
moonrocks = set()
while len(moonrocks) < 5:
    new_rock = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
    if new_rock not in STARGATE_ZONE:  # Prevent rocks from spawning inside the Stargate
        moonrocks.add(new_rock)

# Load sounds
pygame.mixer.init()
try:
    pickup_sound = pygame.mixer.Sound("aud/a_robot_beeping.wav")
    drop_sound = pygame.mixer.Sound("aud/a_robot_beeping-2.wav")
except pygame.error as e:
    print(f"Error loading sound: {e}")
    pickup_sound = None  # Disable pickup sound if load fails
    drop_sound = None    # Disable drop sound if load fails


def move_robot(dx, dy):
    """Move the robot within the grid."""
    global robot_position
    new_x = robot_position[0] + dx
    new_y = robot_position[1] + dy

    # Keep robot within grid boundaries
    if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
        robot_position = (new_x, new_y)
        print(f"Robot moved to {robot_position}")  # Debugging movement

def pick_up_rock():
    """Pick up a moonrock if the robot is on one."""
    global carrying_rock, moonrocks

    if carrying_rock:
        print("You can only carry one rock at a time!")
        return False

    if robot_position in moonrocks:
        moonrocks.remove(robot_position)  # Remove rock from grid
        carrying_rock = True
        if pickup_sound:
          pygame.mixer.Sound.play(pickup_sound)
        print(f"Moonrock picked up at {robot_position}")
        return True
    return False

def drop_rock():
    """Drop a moonrock at the Stargate and update the score."""
    global carrying_rock, score

    if not carrying_rock:
        print("No rock to drop!")
        return False

    if robot_position in STARGATE_ZONE:
        carrying_rock = False
        score += 1  # Increase score when rock is delivered
        if drop_sound:
          pygame.mixer.Sound.play(drop_sound)
        print(f"Moonrock delivered to Stargate! Score: {score}")
        return True
    else:
        print("You must drop the rock at the Stargate!")
        return False

def get_game_state():
    global robot_position, carrying_rock, moonrocks, score
    """Return the current state of the game."""
    return {
        "robot_position": robot_position,
        "carrying_rock": carrying_rock,
        "moonrocks": moonrocks,
        "score": score
    }

    