'''
Justin Farnsworth
Unix Epoch End Countdown
October 20, 2020

This program will render the time in days, hours, minutes, and seconds
until the Unix epoch expires. Once the timer reaches 0 in 2038, many 
systems will not be able to represent time in 32 bits.

Every 5 minutes, a song will be randomly selected and played.
All songs in this module are created by Pogo.

'''

# Imported modules
import pygame
import time
import numpy as np
from random import choice


# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)


# Constants
MUSIC_FOLDER = "data/music/"
MUSICBOARD = (
    "Bite Size Candies.ogg",
    "Boy & Bear.ogg",
    "Data & Picard.ogg",
    "Grow Fonder.ogg",
    "Jaaam.ogg",
    "Kaleidogorgon.ogg",
    "Lead Breakfast.ogg",
    "Toyz Noize.ogg"
) # All songs in this list are made my Pogo.


# Draws the timer
def draw_timer(window, time_array, primary_font, draw_colons):
    # Clears the window with a grey canvas
    window.fill(BLACK)

    # Renders the timer
    time_string_days = primary_font.render(f"{time_array[0]:04}", True, RED)
    time_string_hours = primary_font.render(f"{time_array[1]:02}", True, RED)
    time_string_minutes = primary_font.render(f"{time_array[2]:02}", True, RED)
    time_string_seconds = primary_font.render(f"{time_array[3]:02}", True, RED)

    # This variable will be used to help vertically position the timer on the window.
    timer_height = 185 - time_string_days.get_height()

    # Draws the timer
    window.blit(time_string_days, (242 - time_string_days.get_width(), timer_height))
    window.blit(time_string_hours, (310, timer_height))
    window.blit(time_string_minutes, (480, timer_height))
    window.blit(time_string_seconds, (650, timer_height))
    
    # Draws the colons if permitted.
    if draw_colons:
        colon = primary_font.render(":", True, RED)
        window.blit(colon, ((552 - colon.get_width()) // 2, timer_height))
        window.blit(colon, ((882 - colon.get_width()) // 2, timer_height))
        window.blit(colon, ((1222 - colon.get_width()) // 2, timer_height))
    
    # Displays text and a line that divides the text and timer
    title = primary_font.render("The Epochalypse", True, RED)
    window.blit(title, ((800 - title.get_width()) // 2, 10))
    pygame.draw.line(window, RED, (0, 100), (800, 100), 5)

    # Updates the window
    pygame.display.update()


# Checks if the user presses the escape key or closes the window
def user_terminates_program():
    to_be_terminated = False
    for event in pygame.event.get():
        # Pressing the ESC key or closing the window terminates the program
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            to_be_terminated = True
    return to_be_terminated


# The returned array contains the numbers in order of total days, hours, minutes, and seconds. 
def convert_seconds_to_time(seconds):
    return np.array(
        [seconds // 86400, (seconds // 3600) % 24, (seconds // 60) % 60, seconds % 60],
        dtype="int32"
    )


# Main function
def main():
    # Initializes pygame and sets the name of window
    pygame.init()
    pygame.display.set_caption("Unix Epoch End Countdown")

    # Sets the window dimensions and clock
    window = pygame.display.set_mode((800, 200))
    clock = pygame.time.Clock()

    # Initializes the font for the HUD
    primary_font = pygame.font.Font("data/fonts/digital-7 mono.ttf", 100)

    # A song will be randomly chosen from the musicboard and loaded.
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.load(MUSIC_FOLDER + choice(MUSICBOARD))
    next_song_ready = True

    # Closing the window or clicking the ESC key terminates the program.
    while not user_terminates_program():
        # Sets the FPS to 30
        clock.tick(30)

        # Converts the difference between the end of the Unix 32-bit timestamp (2 ** 31)
        # and the current time into days, hours, minutes, and seconds.
        time_array = convert_seconds_to_time(2147483648 - int(time.time()))

        # A song will be randomly chosen and played every 5 minutes.
        if time_array[2] % 5 == 0:
            if time_array[3] == 0:
                if next_song_ready:
                    pygame.mixer.music.play()
                    next_song_ready = False
            elif not next_song_ready:
                pygame.mixer.music.load(MUSIC_FOLDER + choice(MUSICBOARD))
                next_song_ready = True
        
        # Draws the timer
        include_colons = time_array[3] % 2 == 0 # Draws colons only if the number of seconds is even
        draw_timer(window, time_array, primary_font, include_colons)


# Executes the program.
if __name__ == "__main__":
    main()
