## GasMan
## Feb 26, 2025

# main.py
import pygame
from game_logic import move_robot, pick_up_rock, drop_rock, get_game_state, GRID_SIZE
import time  # Import the time module

pygame.init()

# Screen and grid settings
CELL_SIZE = 80  # Each grid cell is 80x80 pixels
WIDTH, HEIGHT = GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moonrock Collection Game")

# Load and scale images
try:
    robot_img = pygame.image.load("img/robot.png")
    robot_img = pygame.transform.scale(robot_img, (CELL_SIZE, CELL_SIZE))

    moonrock_img = pygame.image.load("img/moonrock.png")
    moonrock_img = pygame.transform.scale(moonrock_img, (CELL_SIZE, CELL_SIZE))

    stargate_img = pygame.image.load("img/stargate.png")
    stargate_img = pygame.transform.scale(stargate_img, (CELL_SIZE * 2, CELL_SIZE * 2))
except pygame.error as e:
    print(f"Error loading image: {e}")
    pygame.quit()
    exit()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
GREEN = (0, 200, 0)
GOLD = (255, 215, 0)  # For the winning screen

# Font setup
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)  # For the winning text
title_font = pygame.font.Font(None, 60) # For the title
instruction_font = pygame.font.Font(None, 30) # For instruction screen

# Load Sounds
try:
    pickup_sound = pygame.mixer.Sound("aud/a_robot_beeping.wav")
    drop_sound = pygame.mixer.Sound("aud/a_robot_beeping-2.wav")
except pygame.error as e:
    print(f"Error loading sound: {e}")
    pickup_sound = None  # Disable pickup sound if load fails
    drop_sound = None    # Disable drop sound if load fails

# Game state
game_won = False  # Add a game won flag
TOTAL_ROCKS = 5  # Defining the total number of rocks
start_time = 0  # Initialize the start time
end_time = 0
game_started = False # Game hasn't started yet
instructions_displayed = False # Instruction hasn't been displayed yet

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Function to display text with word wrapping
def draw_text_with_wrapping(surface, text, font, color, rect):
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = ' '.join(current_line + [word])
        test_rect = font.render(test_line, True, color).get_rect()
        if test_rect.width <= rect.width:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    lines.append(' '.join(current_line))

    y_offset = rect.top
    for line in lines:
        text_surface = font.render(line, True, color)
        text_rect = text_surface.get_rect(center=(rect.centerx, y_offset + text_surface.get_height() // 2))
        surface.blit(text_surface, text_rect)
        y_offset += text_surface.get_height()


# Main game loop
running = True
while running:
    # --- EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if not game_started and not instructions_displayed:
                instructions_displayed = True # Move to instructions screen
            elif not game_started and instructions_displayed:
                game_started = True # Start the Game!
                start_time = time.time() # Start the timer!
            elif game_started and not game_won:
                if event.key == pygame.K_SPACE:
                    if pick_up_rock() and pickup_sound:  # Pickup a rock
                        pygame.mixer.Sound.play(pickup_sound)
                elif event.key == pygame.K_RETURN:
                    if drop_rock() and drop_sound:  # Drop a rock
                        pygame.mixer.Sound.play(drop_sound)

                # Move robot based on key press
                if event.key == pygame.K_w:
                    move_robot(0, -1)  # Move up
                elif event.key == pygame.K_s:
                    move_robot(0, 1)  # Move down
                elif event.key == pygame.K_a:
                    move_robot(-1, 0)  # Move left
                elif event.key == pygame.K_d:
                    move_robot(1, 0)  # Move right

    # --- GAME STATE UPDATE (Get the latest info!)
    if game_started and not game_won:
        game_state = get_game_state()
        robot_position = game_state["robot_position"]
        moonrocks = game_state["moonrocks"]
        score = game_state["score"]
        carrying_rock = game_state["carrying_rock"]

        # Debugging information
        print(f"Moonrocks remaining: {len(moonrocks)}, Score: {score}, Carrying: {carrying_rock}, Game Won: {game_won}")

        # Check for win condition (all rocks delivered)
        if len(moonrocks) == 0 and score == TOTAL_ROCKS and not carrying_rock:  # ALL conditions must be met!
            game_won = True
            end_time = time.time() # Capture the end time
            print("WINNING CONDITION MET!")  # Confirm the condition is met

    # --- DRAWING
    screen.fill(BLACK)  # Set background color to black

    if not game_started and not instructions_displayed:
        # Draw the start screen
        title_text = title_font.render("Welcome to StarGate!", True, WHITE)
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(title_text, title_rect)

        # Instructions with word wrapping
        instructions_text = "Press any key to continue to Instructions"
        instructions_rect = pygame.Rect(WIDTH // 6, HEIGHT // 2, WIDTH * 2 // 3, HEIGHT // 2)
        draw_text_with_wrapping(screen, instructions_text, font, WHITE, instructions_rect)

    elif not game_started and instructions_displayed:
        # Draw instructions screen
        instructions_title = font.render("Instructions", True, WHITE)
        instructions_title_rect = instructions_title.get_rect(center=(WIDTH // 2, HEIGHT // 6))
        screen.blit(instructions_title, instructions_title_rect)

        instructions_text = "Can you help Bobot pick up the moon rocks and deliver them safely to Stargate? Use W, A, S, D to move around. Press SPACE to pick up a rock and ENTER to drop it off."
        instructions_rect = pygame.Rect(WIDTH // 6, HEIGHT // 3, WIDTH * 2 // 3, HEIGHT * 2 // 3)
        draw_text_with_wrapping(screen, instructions_text, instruction_font, WHITE, instructions_rect)

        continue_text = font.render("Press any key to start!", True, WHITE)
        continue_rect = continue_text.get_rect(center=(WIDTH // 2, HEIGHT * 5 // 6))
        screen.blit(continue_text, continue_rect)

    elif game_started and not game_won:
        # Draw the game normally if not won
        # Draw grid lines
        for x in range(0, WIDTH, CELL_SIZE):
            for y in range(0, HEIGHT, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, GRAY, rect, 1)

        # Draw Stargate zone as a 2x2 area
        stargate_top_left = (6, 6)
        screen.blit(stargate_img, (stargate_top_left[0] * CELL_SIZE, stargate_top_left[1] * CELL_SIZE))

        # Draw moonrocks from the global set
        for rock in moonrocks:
            screen.blit(moonrock_img, (rock[0] * CELL_SIZE, rock[1] * CELL_SIZE))

        # Draw robot (based on robot_position)
        screen.blit(robot_img, (robot_position[0] * CELL_SIZE, robot_position[1] * CELL_SIZE))

        # Display Score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Display Carrying Status
        carrying_text = font.render(f"Carrying: {'Yes' if carrying_rock else 'No'}", True, WHITE)
        screen.blit(carrying_text, (10, 40))

        # Display Timer
        elapsed_time = time.time() - start_time
        timer_text = font.render(f"Time: {elapsed_time:.1f}s", True, WHITE)
        screen.blit(timer_text, (10, 70))
    else:
        # Draw the winning screen
        screen.fill(GOLD)  # Gold background for victory!
        win_text = large_font.render("You Won!", True, BLACK)
        win_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))  # Centered at the top
        screen.blit(win_text, win_rect)

        # Display time taken
        total_time = end_time - start_time
        time_text = font.render(f"Time Taken: {total_time:.1f}s", True, BLACK)
        time_rect = time_text.get_rect(center=(WIDTH // 2, HEIGHT * 2 // 4))
        screen.blit(time_text, time_rect)

        stay_tuned_text = font.render("Stay tuned for more levels!", True, BLACK)
        stay_tuned_rect = stay_tuned_text.get_rect(center=(WIDTH // 2, HEIGHT * 3 // 4))  # Centered lower
        screen.blit(stay_tuned_text, stay_tuned_rect)

    pygame.display.flip()  # Update display

    clock.tick(30)  # Control the frame rate

pygame.quit()
 