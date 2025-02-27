import streamlit as st
import pygame
import io
from PIL import Image
from game_logic import move_robot, pick_up_rock, drop_rock, get_game_state, GRID_SIZE
import main as game

# Set up Streamlit page
st.set_page_config(page_title="Moonrock Collection Game", page_icon="🤖")

def display_frame():
    """Fetches and displays the latest Pygame frame in Streamlit."""
    frame = game.generate_frame()
    img_byte_arr = io.BytesIO()
    pygame.image.save(frame, img_byte_arr, "PNG")
    image = Image.open(io.BytesIO(img_byte_arr.getvalue()))
    st.image(image, caption="Game View", use_column_width=True)

# Streamlit UI
st.title("Moonrock Collection Game")
st.write("Use the buttons below to control the robot:")

# Movement Controls
col1, col2, col3 = st.columns(3)
with col2:
    if st.button("↑ Up"):
        move_robot(0, -1)
with col1:
    if st.button("← Left"):
        move_robot(-1, 0)
with col3:
    if st.button("→ Right"):
        move_robot(1, 0)
col1, col2, col3 = st.columns(3)
with col2:
    if st.button("↓ Down"):
        move_robot(0, 1)

# Pickup and Drop Buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("Pick Up"):
        pick_up_rock()
with col2:
    if st.button("Drop"):
        drop_rock()

# Display the updated game frame
display_frame()

# Show score
game_state = get_game_state()
st.write(f"Score: {game_state['score']}")
st.write(f"Carrying Rock: {'Yes' if game_state['carrying_rock'] else 'No'}")