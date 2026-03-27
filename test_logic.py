import os
import pygame
from game_logic import GameState
from config import GRID_SIZE, INITIAL_MOONROCK_COUNT

def test_game_logic():
    # Set SDL_VIDEODRIVER to dummy for headless environment
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    pygame.init()

    gs = GameState(grid_size=GRID_SIZE, time_limit=60)

    print(f"Initial robot position: {gs.robot_position}")
    assert gs.robot_position == (0, 0)

    print(f"Initial moonrocks: {len(gs.moonrocks)}")
    assert len(gs.moonrocks) == INITIAL_MOONROCK_COUNT

    # Test movement
    gs.move_robot(1, 0)
    print(f"Robot position after move(1, 0): {gs.robot_position}")
    assert gs.robot_position == (1, 0)

    # Test picking up rock (if robot happens to be on one, or we move it to one)
    rock_pos = list(gs.moonrocks)[0]
    gs.robot_position = rock_pos
    success = gs.pick_up_rock()
    print(f"Picking up rock at {rock_pos}: {success}")
    assert success is True
    assert gs.carrying_rock is True
    assert len(gs.moonrocks) == INITIAL_MOONROCK_COUNT - 1

    # Test dropping rock in stargate
    stargate_pos = list(gs.stargate_zone)[0]
    gs.robot_position = stargate_pos
    success = gs.drop_rock()
    print(f"Dropping rock at {stargate_pos}: {success}")
    assert success is True
    assert gs.carrying_rock is False
    assert gs.score == 1

    print("All logic tests passed!")

if __name__ == "__main__":
    test_game_logic()
