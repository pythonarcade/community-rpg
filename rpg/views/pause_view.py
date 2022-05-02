"""
Pause Menu
"""
import arcade
import arcade.gui
from rpg.views import *

"""
Same approach as the MainMenuView
"""

# For now it does not do anything
class SettingsButton(arcade.gui.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        pass

class PauseView(arcade.View):
    def __init__(self):
        super().__init__()
        self.started = False
        # We create the buttons here
        self.createButtons()
        arcade.set_background_color(arcade.color.ALMOND)

    def createButtons(self):
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.v_box = arcade.gui.UIBoxLayout()

        # Continue Button
        continue_button = arcade.gui.UIFlatButton(text="Continue", width=200)
        self.v_box.add(continue_button.with_space_around(bottom=20))
        # It continues the game
        @continue_button.event("on_click")
        def on_click_continue(event):
            self.window.show_view(self.window.views["game"])
        # Settings Button
        settings_button = SettingsButton(text="Settings", width=200)
        self.v_box.add(settings_button.with_space_around(bottom=20))
        # Quit Button
        quit_button = arcade.gui.UIFlatButton(text="Quit", width=200)
        self.v_box.add(quit_button.with_space_around(bottom=20))
        # It closes the game
        @quit_button.event("on_click")
        def on_click_quit(event):
            arcade.exit()

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(
            "Pause Menu",
            self.window.width / 2,
            self.window.height - 100,
            arcade.color.ALLOY_ORANGE,
            font_size=44,
            anchor_x="center",
            anchor_y="center",
            align="center",
            width=self.window.width,
        )
        self.manager.draw()

    def setup(self):
        pass

    def on_show_view(self):
        arcade.set_background_color(arcade.color.ALMOND)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_key_press(self, symbol: int, modifiers: int):
        # It continues the game if you press escape
        if symbol == arcade.key.ESCAPE:
            self.window.show_view(self.window.views["game"])