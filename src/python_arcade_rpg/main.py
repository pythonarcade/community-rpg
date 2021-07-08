"""
Python Arcade Community RPG

An open-source RPG
"""

import arcade

from loading_view import LoadingView
from constants import SCREEN_WIDTH
from constants import SCREEN_HEIGHT
from constants import SCREEN_TITLE


class MyWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)
        self.views = {}


def main():
    """ Main method """
    window = MyWindow()
    window.center_window()
    start_view = LoadingView()
    start_view.setup()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
