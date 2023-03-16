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
from random import choice
from typing import NamedTuple
from os import listdir
import pygame
import time


# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)


# Named Tuple
class TimeArray(NamedTuple):
    days: int
    hours: int
    minutes: int
    seconds: int


class UnixEpochEndCountdown:
    # Constructor
    def __init__(self):
        # Initializes pygame and sets the name of window
        pygame.init()
        pygame.display.set_caption("Unix Epoch End Countdown")

        # Sets the window dimensions and clock
        self.__window = pygame.display.set_mode((800, 200))
        self.__clock = pygame.time.Clock()

        # Initializes the font for the HUD
        self.__primary_font = pygame.font.Font("data/fonts/digital-7 mono.ttf", 100)

        # Music (all songs in this list are made my Pogo)
        self.__music_dir = "data/music/"
        self.__musicboard = tuple(
            song for song in listdir(self.__music_dir) if song.endswith(".ogg")
        )

        # A song will be randomly chosen from the musicboard and loaded.
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.load(self.__music_dir + choice(self.__musicboard))

        # Set the initial time difference.
        delta = 2147483648 - int(time.time())
        self.__time_array = self.__convert_seconds_to_time(delta)

    # Main loop
    def run(self):
        # Initially, a song will be ready to play.
        next_song_ready = True

        # Closing the window or clicking the ESC key terminates the program.
        while not self.__user_terminates_program():
            # Sets the FPS to 30
            self.__clock.tick(30)

            # Converts the difference between the end of the Unix 32-bit timestamp (2 ** 31)
            # and the current time into days, hours, minutes, and seconds.
            delta = 2147483648 - int(time.time())
            self.__time_array = self.__convert_seconds_to_time(delta)

            # A song will be randomly chosen and played every 5 minutes.
            if self.__time_array.minutes % 5 == 0:
                if self.__time_array.seconds == 0:
                    if next_song_ready:
                        pygame.mixer.music.play()
                        next_song_ready = False
                elif not next_song_ready:
                    pygame.mixer.music.load(self.__music_dir + choice(self.__musicboard))
                    next_song_ready = True

            # Draws the timer
            self.__draw_timer()

    # Draws the timer
    def __draw_timer(self):
        # Clears the window with a grey canvas
        self.__window.fill(BLACK)

        # Renders the timer
        time_string_days = self.__primary_font.render(f"{self.__time_array[0]:04}", True, RED)
        time_string_hours = self.__primary_font.render(f"{self.__time_array[1]:02}", True, RED)
        time_string_minutes = self.__primary_font.render(f"{self.__time_array[2]:02}", True, RED)
        time_string_seconds = self.__primary_font.render(f"{self.__time_array[3]:02}", True, RED)

        # This variable will be used to help vertically position the timer on the window.
        timer_height = 185 - time_string_days.get_height()

        # Draws the timer
        self.__window.blit(time_string_days, (242 - time_string_days.get_width(), timer_height))
        self.__window.blit(time_string_hours, (310, timer_height))
        self.__window.blit(time_string_minutes, (480, timer_height))
        self.__window.blit(time_string_seconds, (650, timer_height))

        # Draws the colons if permitted.
        if self.__time_array[3] % 2 == 0:
            colon = self.__primary_font.render(":", True, RED)
            self.__window.blit(colon, ((552 - colon.get_width()) // 2, timer_height))
            self.__window.blit(colon, ((882 - colon.get_width()) // 2, timer_height))
            self.__window.blit(colon, ((1222 - colon.get_width()) // 2, timer_height))

        # Displays text and a line that divides the text and timer
        title = self.__primary_font.render("The Epochalypse", True, RED)
        self.__window.blit(title, ((800 - title.get_width()) // 2, 10))
        pygame.draw.line(self.__window, RED, (0, 100), (800, 100), 5)

        # Updates the window
        pygame.display.update()

    # Checks if the user presses the escape key or closes the window
    @staticmethod
    def __user_terminates_program():
        to_be_terminated = False

        for event in pygame.event.get():
            # Pressing the ESC key or closing the window terminates the program
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                to_be_terminated = True

        return to_be_terminated

    # The returned array contains the numbers in order of total days, hours, minutes, and seconds.
    @staticmethod
    def __convert_seconds_to_time(seconds: int):
        days, r1 = divmod(seconds, 86400)
        hours, r2 = divmod(r1, 3600)
        minutes, _seconds = divmod(r2, 60)
        return TimeArray(days, hours, minutes, _seconds)


# Executes the program.
if __name__ == "__main__":
    app = UnixEpochEndCountdown()
    app.run()
