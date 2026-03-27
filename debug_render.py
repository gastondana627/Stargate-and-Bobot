import pygame
from main import GameRenderer
from game_logic import GameState
import os

def capture_frame():
    # Set SDL to use dummy video driver for headless environment
    os.environ["SDL_VIDEODRIVER"] = "dummy"

    renderer = GameRenderer()
    # Create a dummy display surface to avoid the "No video mode" error if possible,
    # though GameRenderer.screen is a Surface, some operations might need a display.
    pygame.display.set_mode((800, 600))

    # Initialize game state
    state = GameState()
    # Mock some data
    game_state = {
        "robot_position": state.robot_position,
        "moonrocks": state.moonrocks,
        "stargate_zone": state.stargate_zone,
        "score": state.score,
        "time_remaining": state.time_remaining,
        "carrying_rock": state.carrying_rock,
        "grid_size": state.grid_size
    }

    surface = renderer.generate_frame(game_state)
    pygame.image.save(surface, "debug_frame.png")
    print("Saved debug_frame.png")

if __name__ == "__main__":
    capture_frame()
