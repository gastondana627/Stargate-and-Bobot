# main.py
import pygame
from typing import Dict, Any, Tuple
from config import (
    CELL_SIZE, ROBOT_IMAGE_PATH, MOONROCK_IMAGE_PATH, STARGATE_IMAGE_PATH,
    BLACK, GRAY, WHITE, STARGATE_SIZE
)

class GameRenderer:
    """Handles all rendering for the Moonrock Collection Game."""

    def __init__(self):
        """Initializes Pygame and loads assets."""
        if not pygame.get_init():
            pygame.init()
        if not pygame.font.get_init():
            pygame.font.init()

        self.font = pygame.font.Font(None, 36)
        self.robot_img, self.moonrock_img, self.stargate_img = self._load_images()

        # We don't need to call set_mode with a visible window for Streamlit,
        # but we need a surface to draw on. The size will be determined by grid_size * CELL_SIZE.
        self.screen = None

    def _load_images(self) -> Tuple[pygame.Surface, pygame.Surface, pygame.Surface]:
        """Loads and scales game images."""
        try:
            # Note: convert_alpha() requires a display mode to be set.
            # In a headless/Streamlit environment, we might not have one.
            robot_img = pygame.image.load(ROBOT_IMAGE_PATH)
            moonrock_img = pygame.image.load(MOONROCK_IMAGE_PATH)
            stargate_img = pygame.image.load(STARGATE_IMAGE_PATH)

            if pygame.display.get_init() and pygame.display.get_surface():
                robot_img = robot_img.convert_alpha()
                moonrock_img = moonrock_img.convert_alpha()
                stargate_img = stargate_img.convert_alpha()

            robot_img = pygame.transform.scale(robot_img, (CELL_SIZE, CELL_SIZE))
            moonrock_img = pygame.transform.scale(moonrock_img, (CELL_SIZE, CELL_SIZE))
            stargate_img = pygame.transform.scale(stargate_img, (CELL_SIZE * STARGATE_SIZE, CELL_SIZE * STARGATE_SIZE))

            return robot_img, moonrock_img, stargate_img
        except (pygame.error, FileNotFoundError) as e:
            print(f"Error loading images: {e}")
            # Fallback to colored surfaces if images fail to load
            robot_img = pygame.Surface((CELL_SIZE, CELL_SIZE))
            robot_img.fill((0, 0, 255))
            moonrock_img = pygame.Surface((CELL_SIZE, CELL_SIZE))
            moonrock_img.fill((255, 255, 0))
            stargate_img = pygame.Surface((CELL_SIZE * STARGATE_SIZE, CELL_SIZE * STARGATE_SIZE))
            stargate_img.fill((0, 255, 255))
            return robot_img, moonrock_img, stargate_img

    def generate_frame(self, game_state: Dict[str, Any]) -> pygame.Surface:
        """Generates a single game frame as a Pygame Surface."""
        grid_size = game_state["grid_size"]
        width = grid_size * CELL_SIZE
        height = grid_size * CELL_SIZE

        if self.screen is None or self.screen.get_width() != width or self.screen.get_height() != height:
            self.screen = pygame.Surface((width, height))

        self.screen.fill(BLACK)

        # Draw grid lines
        for x in range(0, width, CELL_SIZE):
            for y in range(0, height, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, GRAY, rect, 1)

        # Draw Stargate zone
        # The stargate_zone is a set of (x, y) tuples. To blit the 2x2 image once,
        # we find the minimum x and y.
        if game_state["stargate_zone"]:
            min_x = min(cell[0] for cell in game_state["stargate_zone"])
            min_y = min(cell[1] for cell in game_state["stargate_zone"])
            self.screen.blit(self.stargate_img, (min_x * CELL_SIZE, min_y * CELL_SIZE))

        # Draw moonrocks
        for rock in game_state["moonrocks"]:
            self.screen.blit(self.moonrock_img, (rock[0] * CELL_SIZE, rock[1] * CELL_SIZE))

        # Draw robot
        robot_pos = game_state["robot_position"]
        self.screen.blit(self.robot_img, (robot_pos[0] * CELL_SIZE, robot_pos[1] * CELL_SIZE))

        # UI Overlay
        score_text = self.font.render(f"Score: {game_state['score']}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        time_remaining = int(game_state["time_remaining"])
        time_text = self.font.render(f"Time: {time_remaining}", True, WHITE)
        self.screen.blit(time_text, (width - 120, 10))

        carrying = game_state["carrying_rock"]
        carrying_text = self.font.render(f"Carrying: {'Yes' if carrying else 'No'}", True, WHITE)
        self.screen.blit(carrying_text, (10, 40))

        return self.screen

def quit_pygame():
    """Quits Pygame."""
    pygame.quit()
