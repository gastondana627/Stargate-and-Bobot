import streamlit as st
import pygame
import io
from PIL import Image  # Importing the image
from game_logic import move_robot, pick_up_rock, drop_rock, get_game_state, GameState
import main
import json
import time
import random # For randomness on image choice.
import streamlit.components.v1 as components #Streamlined

# Set up page configuration
st.set_page_config(page_title="Moonrock Collection Game", page_icon="🤖")

# Load high scores from JSON file (or initialize if file doesn't exist)
def load_high_scores():
    try:
        with open("high_scores.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_high_scores(high_scores):
    with open("high_scores.json", "w") as f:
        json.dump(high_scores, f)

# Initialize session state (do this at the top!)
if 'player_name' not in st.session_state:
    st.session_state['player_name'] = ""
if 'game_started' not in st.session_state:
    st.session_state['game_started'] = False
if 'game_state' not in st.session_state:
    st.session_state['game_state'] = None  # To hold the instance
if 'high_scores' not in st.session_state:
    st.session_state['high_scores'] = load_high_scores()
if 'game_over' not in st.session_state:
    st.session_state['game_over'] = False
if 'high_score_saved' not in st.session_state: # Boolean to check if a highscore exists.
    st.session_state['high_score_saved'] = False
if 'welcome_image' not in st.session_state:
    st.session_state['welcome_image'] = None
if 'congrats_image' not in st.session_state:
    st.session_state['congrats_image'] = None

def display_frame(frame):
    """Displays a Pygame frame in Streamlit."""
    if frame:
        img_byte_arr = io.BytesIO()
        pygame.image.save(frame, img_byte_arr, "PNG")
        img_byte_arr = img_byte_arr.getvalue()
        image = Image.open(io.BytesIO(img_byte_arr))
        st.image(image, caption="Game View", use_container_width=True)

# Load the welcome image and congratulations image
if st.session_state['welcome_image'] is None or st.session_state['congrats_image'] is None:
    try:
        import random
        image_options = [
            "Graphics_Audio/img/robot.png",
            "Graphics_Audio/img/moonrock.png",
            "Graphics_Audio/img/Stargate.png",
            "Graphics_Audio/img/Stargate1.jpg",
        ]
        random_img_path = random.choice(image_options)
        st.session_state['welcome_image'] = Image.open(random_img_path)
        st.session_state['congrats_image'] = Image.open(random_img_path)
    except FileNotFoundError:
       st.session_state['welcome_image'] = None
       st.session_state['congrats_image'] = None

# Welcome Screen
if not st.session_state['game_started']:
    st.title("Moonrock Collection Game")

    if st.session_state['welcome_image'] is not None:
       st.image(st.session_state['welcome_image'], caption="Welcome! Help Bobot collect the moonrocks!", use_container_width=True)  # Display a welcome message
    else:
        st.write("You can't load this image - welcome.")

    st.write("Enter your name to start:")
    player_name_input = st.text_input("Your Name", key="player_name_input")
    time_limit_input = st.number_input("Game Time Limit (seconds)", min_value=30, max_value=300, value=60, step=10) # Time limit for the users

    # Added Start Game with condition
    if st.button("Start Game"):
        if player_name_input:
            st.session_state['player_name'] = player_name_input
            st.session_state['time_limit'] = time_limit_input
            # Load everything.
            st.session_state['game_state'] = GameState(time_limit=time_limit_input)  # Create a new game state.
            st.session_state['game_started'] = True
            st.session_state['game_over'] = False
            st.session_state['high_score_saved'] = False # Setting state, that a high score has not been saved, so we can put it there
            st.rerun()
        else:
            st.warning("Please enter your name to start the game.")
else:
    # Streamlit UI
    st.title(f"Moonrock Collection Game - Player: {st.session_state['player_name']}")
    st.write("Use the buttons below to control the robot:")

    #Get the key
    if st.session_state['game_state'].time_remaining > 0 and not st.session_state['game_over']: # Timer
        st.write(f"Time Remaining: {int(st.session_state['game_state'].time_remaining)} seconds")
        #Check if Game Over Conditions

       # Check if game has loaded by setting key input before buttons
        key_input = st.session_state.get("key", None)

        #This is the list of keys used and functions they call.
        col1, col2, col3 = st.columns(3)
        with col2:
            if key_input == "ArrowUp" or st.button("↑ Up"):
                st.session_state['game_state'].move_robot(0, -1) #move robot
        with col1:
            if key_input == "ArrowLeft" or st.button("← Left"):
                st.session_state['game_state'].move_robot(-1, 0) #move robot
        with col3:
            if  key_input == "ArrowRight" or st.button("→ Right"):
                st.session_state['game_state'].move_robot(1, 0) #move robot

        with col2:
            if key_input == "ArrowDown" or st.button("↓ Down"):
                st.session_state['game_state'].move_robot(0, 1) #move robot

        #Second Layout with Pick Up or Drops
        col1, col2 = st.columns(2) #New Layout for new rows, or buttons for the streamlit app.
        with col1:
            if st.button("Pick Up"):
                st.session_state['game_state'].pick_up_rock() #Pick Up
        with col2:
            if st.button("Drop"):
                st.session_state['game_state'].drop_rock() #Drop the rock to the zone

        # Get the game state.
        frame = main.generate_frame(st.session_state['game_state'].get_game_state())
        display_frame(frame)

        #Check if Game Over Conditions
        if st.session_state['game_state'].all_rocks_collected() or st.session_state['game_state'].time_remaining <= 0:
            st.session_state['game_over'] = True

    else: # If all the checks failed, we have game over.
        st.session_state['game_over'] = True

    if st.session_state['game_over']:  # Game Over Screen, if game_over == true.
        if st.session_state['game_state'].time_remaining <= 0: # If timer runs out.
            st.write("Time's up! Game Over.")
        else: # The person won!
            st.success("Congratulations! You collected all the moonrocks!")

        if st.session_state['congrats_image'] is not None: # Only load if there is a valid picture.
            st.image(st.session_state['congrats_image'], caption="Congratulations!", use_container_width=True)
        else:
            st.write("You can't load this image - congratulations.")

        score = st.session_state['game_state'].score # Setting variable to check highscore.
        st.write(f"Your Score: {score}") # Setting the score.

        # Save High Score Logic
        if not st.session_state['high_score_saved']:
            if st.button("Save High Score"): # Button to save

                st.session_state['high_scores'].append((st.session_state['player_name'], score)) # Set variable to save names
                st.session_state['high_scores'] = sorted(st.session_state['high_scores'], key=lambda item: item[1], reverse=True)[:5]  # Keep only top 5
                save_high_scores(st.session_state['high_scores'])
                st.session_state['high_score_saved'] = True
                st.rerun()
        else:
            st.write("High score saved!")

        # Display High Scores
        st.subheader("High Scores")
        for name, score in st.session_state['high_scores']: # Looping for each name and score.
            st.write(f"{name}: {score}") # Setting high scores and names.



