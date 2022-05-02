"""
Python Arcade Community RPG

An open-source RPG
"""

import arcade

from rpg.constants import SCREEN_HEIGHT, SCREEN_TITLE, SCREEN_WIDTH
from rpg.views import LoadingView
from rpg.views.main_menu_view import MainMenuView


class MyWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)
        self.views = {}

        arcade.resources.add_resource_handle("characters", "resources/characters")
        arcade.resources.add_resource_handle("maps", "resources/maps")
        arcade.resources.add_resource_handle("data", "resources/data")
        arcade.resources.add_resource_handle("sounds", "resources/sounds")


def main():
    """Main method"""
    window = MyWindow()
    window.center_window()
    start_view = MainMenuView()
    start_view.setup()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
