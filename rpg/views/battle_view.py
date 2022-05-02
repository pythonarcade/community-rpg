"""
Battle View
"""

import arcade
import rpg.constants as constants

class BattleView(arcade.View):
    def __init__(self):
        super().__init__()
        self.started = False
        arcade.set_background_color(arcade.color.BLUE)
    def setup(self):
        pass
    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLUE)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):#makes text apear on screen. The blue background will not draw w/o this
        arcade.start_render()
        arcade.draw_text(
            "BATTLE(WIP)",
            self.window.width / 2,
            self.window.height - 50,
            arcade.color.WHITE,
            44,
            anchor_x="center",
            anchor_y="center",
            align="center",
            width=self.window.width,
        )
        arcade.draw_text(
            "[-----------------------------------------------------------------------------------------------------------------------------]",
            self.window.width / 2,
            self.window.height - 500,
            arcade.color.WHITE,
            22,
            anchor_x="center",
            anchor_y="center",
            align="center",
            width=self.window.width,
        )
        arcade.draw_text(
            "ATTACK [A]                                  ITEMS [I]",
            self.window.width / 2,
            self.window.height - 550,
            arcade.color.WHITE,
            44,
            anchor_x="center",
            anchor_y="center",
            align="center",
            width=self.window.width,
        )
        arcade.draw_text(
            "MAGIC [M]                                  FLEE [F]",
            self.window.width / 2,
            self.window.height - 650,
            arcade.color.WHITE,
            44,
            anchor_x="center",
            anchor_y="center",
            align="center",
            width=self.window.width,
        )
    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            self.window.show_view(self.window.views["main_menu"])