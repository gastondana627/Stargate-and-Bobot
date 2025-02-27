# streamlit_app.py
import streamlit as st
import pygame
import io
from PIL import Image
from game_logic import GameState
import main
import json
import time
import random
import streamlit.components.v1 as components

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

# Initialize session state
if 'player_name' not in st.session_state:
    st.session_state['player_name'] = ""
if 'game_started' not in st.session_state:
    st.session_state['game_started'] = False
if 'game_state' not in st.session_state:
    st.session_state['game_state'] = None
if 'high_scores' not in st.session_state:
    st.session_state['high_scores'] = load_high_scores()
if 'game_over' not in st.session_state:
    st.session_state['game_over'] = False
if 'high_score_saved' not in st.session_state:
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
       st.image(st.session_state['welcome_image'], caption="Welcome! Help Bobot collect the moonrocks!", use_container_width=True)
    else:
        st.write("You can't load this image - welcome.")

    st.write("Enter your name to start:")
    player_name_input = st.text_input("Your Name", key="player_name_input")
    time_limit_input = st.number_input("Game Time Limit (seconds)", min_value=30, max_value=300, value=60, step=10)

    if st.button("Start Game"):
        if player_name_input:
            st.session_state['player_name'] = player_name_input
            st.session_state['time_limit'] = time_limit_input
            st.session_state['game_state'] = GameState(time_limit=time_limit_input)
            st.session_state['game_started'] = True
            st.session_state['game_over'] = False
            st.session_state['high_score_saved'] = False
            st.rerun()
        else:
            st.warning("Please enter your name to start the game.")
else:
    # Game Play Area
    if not st.session_state['game_over']:
        st.title(f"Moonrock Collection Game - Player: {st.session_state['player_name']}")
        st.write("Use the buttons below to control the robot:")

        # Timer display
        time_remaining = int(st.session_state['game_state'].time_remaining)
        st.metric("Time Remaining", f"{time_remaining} seconds")

        # Movement Buttons
        col1, col2, col3 = st.columns(3)
        with col2:
            if st.button("↑ Up"):
                st.session_state['game_state'].move_robot(0, -1)
        with col1:
            if st.button("← Left"):
                st.session_state['game_state'].move_robot(-1, 0)
        with col3:
            if st.button("→ Right"):
                st.session_state['game_state'].move_robot(1, 0)
        with col2:
            if st.button("↓ Down"):
                st.session_state['game_state'].move_robot(0, 1)

        # Action Buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Pick Up"):
                st.session_state['game_state'].pick_up_rock()
        with col2:
            if st.button("Drop"):
                st.session_state['game_state'].drop_rock()

        # Generate and display the frame
        frame = main.generate_frame(st.session_state['game_state'].get_game_state())
        display_frame(frame)

        # Game Over Check
        if st.session_state['game_state'].all_rocks_collected() or st.session_state['game_state'].time_remaining <= 0:
            st.session_state['game_over'] = True

        # Refresh the app to update the timer if the game is running
        time.sleep(1)
        st.rerun()

    else:  # if st.session_state['game_over']:
        # Game Over Screen
        time_up = False

        if st.session_state['game_state'].time_remaining <= 0:
            st.error("TIME'S UP! You ran out of time. Game Over.")
            time_up = True
        else:
            st.success("Congratulations! You collected all the moonrocks!")
            time_up = False

        # Conditionally display the congratulations image
        if not time_up and st.session_state['congrats_image'] is not None:
            st.image(st.session_state['congrats_image'], caption="Congratulations!", use_container_width=True)
        elif not time_up:
            st.write("You can't load this image - congratulations.")

        if not time_up:
            time_taken = st.session_state['time_limit'] - int(st.session_state['game_state'].time_remaining)
            st.write(f"Time Taken: {time_taken} seconds")
        else:
            time_taken = 0

        # Save High Score Logic - DISABLE IF TIME IS UP
        if not st.session_state['high_score_saved']:
            if not time_up and st.button("Save High Score"):
                st.session_state['high_scores'].append((st.session_state['player_name'], time_taken))
                st.session_state['high_scores'] = sorted(st.session_state['high_scores'], key=lambda item: item[1])[:5]
                save_high_scores(st.session_state['high_scores'])
                st.session_state['high_score_saved'] = True
                st.rerun()
            elif time_up:
                st.write("You cannot save your high score because time ran out.")
        else:
            st.write("High score saved!")

        # Display High Scores
        st.subheader("High Scores")
        # Load new high scores.
        high_scores = load_high_scores()

        for name, score in high_scores:
            st.write(f"{name}: {score} seconds")

