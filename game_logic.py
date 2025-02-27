import pygame
import random
import os  

GRID_SIZE = 8
robot_position = (0, 0)
carrying_rock = False
score = 0

STARGATE_ZONE = {(6, 6), (6, 7), (7, 6), (7, 7)}

moonrocks = set()
while len(moonrocks) < 5:
    new_rock = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
    if new_rock not in STARGATE_ZONE:
        moonrocks.add(new_rock)

try:
    if pygame.mixer.get_init() is None:
        pygame.mixer.init()
    
    cwd = os.getcwd()
    pickup_sound_path = os.path.join(cwd, "Graphics_Audio", "aud", "a_robot_beeping.wav")
    drop_sound_path = os.path.join(cwd, "Graphics_Audio", "aud", "a_robot_beeping-2.wav")

    pickup_sound = pygame.mixer.Sound(pickup_sound_path)
    drop_sound = pygame.mixer.Sound(drop_sound_path)

except pygame.error as e:
    print(f"Error loading sound: {e}")
    pickup_sound = None
    drop_sound = None

def move_robot(dx, dy):
    global robot_position
    new_x = robot_position[0] + dx
    new_y = robot_position[1] + dy

    if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
        robot_position = (new_x, new_y)

def pick_up_rock():
    global carrying_rock, moonrocks

    if carrying_rock:
        print("You can only carry one rock at a time!")
        return False

    if robot_position in moonrocks:
        moonrocks.remove(robot_position)
        carrying_rock = True
        if pickup_sound:
            pygame.mixer.Sound.play(pickup_sound)
        return True
    return False

def drop_rock():
    global carrying_rock, score

    if not carrying_rock:
        print("No rock to drop!")
        return False

    if robot_position in STARGATE_ZONE:
        carrying_rock = False
        score += 1
        if drop_sound:
            pygame.mixer.Sound.play(drop_sound)
        return True
    return False

def get_game_state():
    return {
        "robot_position": robot_position,
        "carrying_rock": carrying_rock,
        "moonrocks": list(moonrocks),
        "score": score
    }


