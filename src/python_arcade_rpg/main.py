"""
Python Arcade Community RPG

An open-source RPG
"""

import arcade

from game_view import GameView
from constants import SCREEN_WIDTH
from constants import SCREEN_HEIGHT
from constants import SCREEN_TITLE


def main():
    """ Main method """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)
    window.center_window()
    start_view = GameView()
    start_view.setup()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
