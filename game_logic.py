# game_logic.py
import pygame
import random
import os  # Import the os module
from config import GRID_SIZE # Import from config to change in one place
import time # Importing a timer
class GameState:
    """Encapsulates the entire game state."""

    def __init__(self, grid_size=GRID_SIZE, time_limit = 60):  # Default value from config
        """Initializes the game state."""
        self.grid_size = grid_size
        self.robot_position = (0, 0)
        self.carrying_rock = False
        self.score = 0
        self.stargate_zone = self._generate_stargate_zone()
        self.moonrocks = self._generate_moonrocks()
        self.load_sounds() # Importing the sounds from the main to set
        self.time_limit = time_limit # Setting default value from the GUI or to 60 for time_limit.

        self.start_time = time.time()
        self.time_remaining = self.time_limit # Setting start time for start with.
        #Setting attributes for the game, the robot.
    def _generate_stargate_zone(self):
        """Generates a random stargate location (2x2 area)."""
        stargate_size = 2 # StarGate size
        x = random.randint(0, self.grid_size - stargate_size) # Setting bounds
        y = random.randint(0, self.grid_size - stargate_size) # Setting bounds
        return {(x + i, y + j) for i in range(stargate_size) for j in range(stargate_size)} # Cleaner set comprehension

    def _generate_moonrocks(self):
        """Generates random moonrock positions, avoiding the Stargate."""
        moonrocks = set()
        while len(moonrocks) < 5: # To generate the MoonRoccks
            new_rock = (random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)) # Randomizing
            if new_rock not in self.stargate_zone and new_rock not in moonrocks:  # Added duplicate check
                moonrocks.add(new_rock)
        return moonrocks

    def load_sounds(self):
        """Loads sounds from file paths in config.py."""
        try:
            from config import PICKUP_SOUND_PATH, DROP_SOUND_PATH # Loading the sounds from config

            if pygame.mixer.get_init() is None: # To load sounds from the config file
                pygame.mixer.init()

            self.pickup_sound = pygame.mixer.Sound(PICKUP_SOUND_PATH) # setting the attributes
            self.drop_sound = pygame.mixer.Sound(DROP_SOUND_PATH) # setting the attributes

        except pygame.error as e:
            print(f"Error loading sound: {e}") # If theres an error, then just print it to not ruin the process.
            self.pickup_sound = None  # Disable pickup sound if load fails
            self.drop_sound = None    # Disable drop sound if load fails
        except FileNotFoundError as e:
            print(f"Error loading sound: {e}") # Printing sound
            self.pickup_sound = None  # Disable pickup sound if load fails
            self.drop_sound = None # Disabiling sound

    def move_robot(self, dx: int, dy: int) -> None: # Moving the Robot function
        """Moves the robot within the grid boundaries."""
        new_x = self.robot_position[0] + dx # Setting the new position
        new_y = self.robot_position[1] + dy # Setting the new position
        if 0 <= new_x < self.grid_size and 0 <= new_y < self.grid_size: # Check if moving the robot is out of place
            self.robot_position = (new_x, new_y) # Setting the attributes.

    def pick_up_rock(self) -> bool: # Function to pick up the rock.
        """Picks up a moonrock if the robot is on one."""
        if self.carrying_rock: # Setting if is carrying a rock, return False.
            print("You can only carry one rock at a time!") # Print
            return False

        if self.robot_position in self.moonrocks: # If the robots position is inside the moonrocks variable, then return
            self.moonrocks.remove(self.robot_position) # To set that it is no longer in the moonrocks list
            self.carrying_rock = True # is is carrying and set to true
            if self.pickup_sound: # Load that to if the robot is carrying
                pygame.mixer.Sound.play(self.pickup_sound)
            print(f"Moonrock picked up at {self.robot_position}") # Setting message
            return True
        return False

    def drop_rock(self) -> bool: # Function to drop the rock and return if is doing it.
        """Drops a moonrock at the Stargate and updates the score."""
        if not self.carrying_rock: # If not, carrying, return False
            print("No rock to drop!") #Set Print
            return False

        if self.robot_position in self.stargate_zone: # If the robot can set on the gate, set to True
            self.carrying_rock = False # To no longer carry a rock to 0 and set to False.
            self.score += 1 # Setting the atribute to the score set.
            if self.drop_sound: # setting sound
                pygame.mixer.Sound.play(self.drop_sound) # Set the current dropping of the sound.
            print(f"Moonrock delivered to Stargate! Score: {self.score}") # Send that to the enduser.
            return True
        else: # Else send that this can only be dropped at a specific location
            print("You must drop the rock at the Stargate!") # Message
            return False

    def get_game_state(self) -> dict:
        """Returns the current game state as a dictionary."""
        self.update_time() # Call before creating this.
        return {
            "robot_position": self.robot_position, # Position
            "carrying_rock": self.carrying_rock, # boolean
            "moonrocks": self.moonrocks, #MoonRoccks value
            "score": self.score, # integer
            "grid_size": self.grid_size, # Integer
            "stargate_zone": self.stargate_zone, # Area where to drop stuff
            "time_remaining": self.time_remaining, # Time to play until the time is set.
        }

    def all_rocks_collected(self) -> bool:
        """Check if all moonrocks have been collected (dropped at the Stargate)"""
        return len(self.moonrocks) == 0 and not self.carrying_rock

    def update_time(self): #Function to set and update the time function for the timer.
        """Updates the remaining time."""
        elapsed_time = time.time() - self.start_time # Setting initial
        self.time_remaining = max(0, self.time_limit - elapsed_time) # Time starts to decrement

# Initialize the game state (outside the class definition, but module level)
#game_state = GameState()
# The reason for calling the function here is because other files have dependencies on this.

def move_robot(dx, dy): #Function to move the robot on a new position
    #The reason why this has the global gamestate here, is because streamlit uses the function.
    #Therefore the file needs access to it and so does streamlit so I am not defining it again inside streamlit.
    print ("No Long Used Function")
def pick_up_rock(): #Function to call the game state's pick_up_rock
    print ("No Long Used Function")

def drop_rock(): #Function to call the game state's drop_rock
    print ("No Long Used Function")

def get_game_state(): #Function to access gamestate
    #Calling a function, for the attributes.
    print ("No Long Used Function")

def all_rocks_collected(): #Function to check the collection of rocks
    print ("No Long Used Function")


