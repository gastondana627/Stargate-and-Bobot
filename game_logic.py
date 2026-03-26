# game_logic.py
import pygame
import random
import os
import time
from typing import Set, Tuple, Dict, Any
from config import GRID_SIZE, INITIAL_MOONROCK_COUNT, STARGATE_SIZE

class GameState:
    """Encapsulates the entire game state."""

    def __init__(self, grid_size: int = GRID_SIZE, time_limit: int = 60):
        """Initializes the game state."""
        self.grid_size: int = grid_size
        self.robot_position: Tuple[int, int] = (0, 0)
        self.carrying_rock: bool = False
        self.score: int = 0
        self.stargate_zone: Set[Tuple[int, int]] = self._generate_stargate_zone()
        self.moonrocks: Set[Tuple[int, int]] = self._generate_moonrocks()
        self.load_sounds()
        self.time_limit: int = time_limit
        self.start_time: float = time.time()
        self.time_remaining: float = float(time_limit)

    def _generate_stargate_zone(self) -> Set[Tuple[int, int]]:
        """Generates a random stargate location (2x2 area)."""
        x = random.randint(0, self.grid_size - STARGATE_SIZE)
        y = random.randint(0, self.grid_size - STARGATE_SIZE)
        return {(x + i, y + j) for i in range(STARGATE_SIZE) for j in range(STARGATE_SIZE)}

    def _generate_moonrocks(self) -> Set[Tuple[int, int]]:
        """Generates random moonrock positions, avoiding the Stargate."""
        moonrocks: Set[Tuple[int, int]] = set()
        while len(moonrocks) < INITIAL_MOONROCK_COUNT:
            new_rock = (random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1))
            if new_rock not in self.stargate_zone and new_rock not in moonrocks:
                moonrocks.add(new_rock)
        return moonrocks

    def load_sounds(self) -> None:
        """Loads sounds from file paths in config.py."""
        try:
            from config import PICKUP_SOUND_PATH, DROP_SOUND_PATH

            if pygame.mixer.get_init() is None:
                pygame.mixer.init()

            self.pickup_sound = pygame.mixer.Sound(PICKUP_SOUND_PATH)
            self.drop_sound = pygame.mixer.Sound(DROP_SOUND_PATH)

        except (pygame.error, FileNotFoundError, ImportError) as e:
            print(f"Error loading sound: {e}")
            self.pickup_sound = None
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
                self.pickup_sound.play()
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
                self.drop_sound.play()
            print(f"Moonrock delivered to Stargate! Score: {self.score}")
            return True
        else:
            print("You must drop the rock at the Stargate!")
            return False

    def get_game_state(self) -> Dict[str, Any]:
        """Returns the current game state as a dictionary."""
        self.update_time()
        return {
            "robot_position": self.robot_position,
            "carrying_rock": self.carrying_rock,
            "moonrocks": self.moonrocks,
            "score": self.score,
            "grid_size": self.grid_size,
            "stargate_zone": self.stargate_zone,
            "time_remaining": self.time_remaining,
        }

    def all_rocks_collected(self) -> bool:
        """Check if all moonrocks have been collected (dropped at the Stargate)"""
        return len(self.moonrocks) == 0 and not self.carrying_rock

    def update_time(self) -> None:
        """Updates the remaining time."""
        elapsed_time = time.time() - self.start_time
        self.time_remaining = max(0.0, self.time_limit - elapsed_time)
