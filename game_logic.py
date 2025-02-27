# game_logic.py

import pygame
import random
import os  # Import the os module
from config import GRID_SIZE # Import from config to change in one place

class GameState:
    """Encapsulates the entire game state."""

    def __init__(self, grid_size=GRID_SIZE):  # Default value from config
        """Initializes the game state."""
        self.grid_size = grid_size
        self.robot_position = (0, 0)
        self.carrying_rock = False
        self.score = 0
        self.stargate_zone = self._generate_stargate_zone()
        self.moonrocks = self._generate_moonrocks()
        self.load_sounds()

    def _generate_stargate_zone(self):
        """Generates a random stargate location (2x2 area)."""
        stargate_size = 2
        x = random.randint(0, self.grid_size - stargate_size) # Keep stargate within bounds
        y = random.randint(0, self.grid_size - stargate_size)
        return {(x + i, y + j) for i in range(stargate_size) for j in range(stargate_size)} # Cleaner set comprehension


    def _generate_moonrocks(self):
        """Generates random moonrock positions, avoiding the Stargate."""
        moonrocks = set()
        while len(moonrocks) < 5: # To generate initial moonrocks
            new_rock = (random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1))
            if new_rock not in self.stargate_zone and new_rock not in moonrocks:  # Added duplicate check
                moonrocks.add(new_rock)
        return moonrocks

    def load_sounds(self):
        """Loads sounds from file paths in config.py."""
        try:
            from config import PICKUP_SOUND_PATH, DROP_SOUND_PATH

            if pygame.mixer.get_init() is None:
                pygame.mixer.init()

            self.pickup_sound = pygame.mixer.Sound(PICKUP_SOUND_PATH)
            self.drop_sound = pygame.mixer.Sound(DROP_SOUND_PATH)

        except pygame.error as e:
            print(f"Error loading sound: {e}")
            self.pickup_sound = None  # Disable pickup sound if load fails
            self.drop_sound = None    # Disable drop sound if load fails
        except FileNotFoundError as e:
            print(f"Error loading sound: {e}")
            self.pickup_sound = None  # Disable pickup sound if load fails
            self.drop_sound = None

    def move_robot(self, dx: int, dy: int) -> None:
        """Moves the robot within the grid boundaries."""
        new_x = self.robot_position[0] + dx
        new_y = self.robot_position[1] + dy
        if 0 <= new_x < self.grid_size and 0 <= new_y < self.grid_size:
            self.robot_position = (new_x, new_y)

    def pick_up_rock(self) -> bool:
        """Picks up a moonrock if the robot is on one."""
        if self.carrying_rock:
            print("You can only carry one rock at a time!")
            return False

        if self.robot_position in self.moonrocks:
            self.moonrocks.remove(self.robot_position)
            self.carrying_rock = True
            if self.pickup_sound:
                pygame.mixer.Sound.play(self.pickup_sound)
            print(f"Moonrock picked up at {self.robot_position}")
            return True
        return False

    def drop_rock(self) -> bool:
        """Drops a moonrock at the Stargate and updates the score."""
        if not self.carrying_rock:
            print("No rock to drop!")
            return False

        if self.robot_position in self.stargate_zone:
            self.carrying_rock = False
            self.score += 1
            if self.drop_sound:
                pygame.mixer.Sound.play(self.drop_sound)
            print(f"Moonrock delivered to Stargate! Score: {self.score}")
            return True
        else:
            print("You must drop the rock at the Stargate!")
            return False

    def get_game_state(self) -> dict:
        """Returns the current game state as a dictionary."""
        return {
            "robot_position": self.robot_position,
            "carrying_rock": self.carrying_rock,
            "moonrocks": self.moonrocks,
            "score": self.score,
            "grid_size": self.grid_size,
            "stargate_zone": self.stargate_zone
        }


# Initialize the game state (outside the class definition, but module level)
game_state = GameState() # Changed to be an instantiation from the GameState
# The reason for calling the function here is because other files have dependencies on this.

def move_robot(dx, dy): #Function to move the robot on a new position
    game_state.move_robot(dx,dy)
    # The reason why this has the global gamestate here, is because streamlit uses the function.
    # Therefore the file needs access to it and so does streamlit so I am not defining it again inside streamlit.
def pick_up_rock(): #Function to call the game state's pick_up_rock
    game_state.pick_up_rock()

def drop_rock(): #Function to call the game state's drop_rock
    game_state.drop_rock()

def get_game_state(): #Function to access gamestate
    return game_state.get_game_state() # Calling a function, for the attributes.
    }


