"""
Python Arcade Community RPG

An open-source RPG
"""
import arcade

from rpg.constants import SCREEN_HEIGHT, SCREEN_TITLE, SCREEN_WIDTH
from rpg.views import ViewMainMenu


class MyWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)
        self.views = {}

        arcade.resources.add_resource_handle("assets", "resources")


def main():
    """Main method"""
    window = MyWindow()
    window.center_window()
    start_view = ViewMainMenu()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
