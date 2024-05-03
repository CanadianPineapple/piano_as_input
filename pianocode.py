import mido
import time
import pydirectinput
# import tkinter as tk
# from tkinter import messagebox

# My MIDI device is CASIO USB-MIDI 0 btw
# Define the mapping between piano keys and keyboard keys
key_mapping = {
    60: {'keyboard': 'ctrl'},
    61: {'keyboard': 'shift'},
    62: {'keyboard': 'w'},
    63: {'keyboard': 'e'},
    64: {'keyboard': 'a'},
    65: {'keyboard': 'q'},
    66: {'keyboard': 's'},
    67: {'keyboard': 'd'},
    68: {'keyboard': 'space'},
    # Add more mappings as needed
}

# Define the mapping between piano keys and mouse movements
mouse_mapping = {
    76: {'mouse_movement': (-50, 0), 'duration': 0.5},  # Move the mouse left
    77: {'mouse_movement': (50, 0), 'duration': 0.5},   # Move the mouse right
    78: {'mouse_movement': (0, -50), 'duration': 0.5},  # Move the mouse up
    79: {'mouse_movement': (0, 50), 'duration': 0.5}    # Move the mouse down
}

# Define the mapping between piano keys and mouse clicks
mouse_click_mapping = {
    80: {'mouse_click': 'right'},  # Right mouse click
    81: {'mouse_click': 'left'},   # Left mouse click
    82: {'mouse_click': 'middle'}  # Middle mouse click
    # Add more mappings as needed
}

# Function to handle MIDI messages for keyboard events
def handle_keyboard_midi_message(message):
    try:
        if message.type == 'note_on':
            note = message.note
            print(note)
            if note in key_mapping:
                key = key_mapping[note]['keyboard']
                print(key)
                pydirectinput.keyDown(key)
        elif message.type == 'note_off':
            note = message.note
            if note in key_mapping:
                key = key_mapping[note]['keyboard']
                pydirectinput.keyUp(key)  # Release the key
    except Exception as e:
        print("Error handling keyboard MIDI message:", e)

# Function to handle MIDI messages for mouse movements
def handle_mouse_midi_message(message):
    try:
        if message.type == 'note_on':
            note = message.note
            if note in mouse_mapping:
                mouse_movement_data = mouse_mapping[note]['mouse_movement']
                if isinstance(mouse_movement_data, tuple) and len(mouse_movement_data) == 2:
                    (dx, dy) = mouse_movement_data
                    duration = mouse_mapping[note]['duration']
                    start_time = time.time()
                    end_time = start_time + duration
                    while time.time() < end_time:
                        progress = (time.time() - start_time) / duration
                        current_dx = int(dx * progress)
                        current_dy = int(dy * progress)
                        pydirectinput.moveRel(current_dx, current_dy)
                        time.sleep(0.01)  # Adjust the sleep duration as needed for smoother movement
    except Exception as e:
        print("Error handling mouse MIDI message:", e)

# Function to handle MIDI messages for mouse clicks
def handle_mouse_click_midi_message(message):
    try:
        if message.type == 'note_on':
            note = message.note
            if note in mouse_click_mapping:
                print('mouse_click')
                click_type = mouse_click_mapping[note]['mouse_click']
                pydirectinput.mouseDown(button=click_type)
        elif message.type == 'note_off':
            note = message.note
            if note in mouse_click_mapping:
                click_type = mouse_click_mapping[note]['mouse_click']
                pydirectinput.mouseUp(button=click_type)
    except Exception as e:
        print("Error handling mouse click MIDI message:", e)

# Main function to listen for MIDI messages
def main(midi_device):
    try:
        with mido.open_input(midi_device) as port:
            print(f"Listening for MIDI input from device: {midi_device}")
            for message in port:
                print(message)
                handle_keyboard_midi_message(message)
                handle_mouse_midi_message(message)
                handle_mouse_click_midi_message(message)
    except IOError as e:
        print("Error: MIDI device not found.")
    except Exception as e:
        print("Unexpected error:", e)

# Function to handle button click event
def start_listening():
    midi_device = 'CASIO USB-MIDI 0' #midi_device_entry.get()
    if midi_device:
        main(midi_device)
    else:
        print("Warning", "Please enter a MIDI device name.")

start_listening()
