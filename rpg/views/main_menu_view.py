"""
Main Menu
"""
import arcade


class MainMenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.started = False
        arcade.set_background_color(arcade.color.ALMOND)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(
            "Main Menu",
            self.window.width / 2,
            self.window.height - 50,
            arcade.color.ALLOY_ORANGE,
            44,
            anchor_x="center",
            anchor_y="center",
            align="center",
            width=self.window.width,
        )

        arcade.draw_text(
            "Settings (Y)",
            self.window.width / 2,
            self.window.height - 150,
            arcade.color.AMAZON,
            32,
            anchor_x="center",
            anchor_y="center",
            align="center",
            width=self.window.width,
        )

        arcade.draw_text(
            "Close Game (Q)",
            self.window.width / 2,
            self.window.height - 250,
            arcade.color.AMAZON,
            32,
            anchor_x="center",
            anchor_y="center",
            align="center",
            width=self.window.width,
        )

        arcade.draw_text(
            "Resume Game (ESC)",
            self.window.width / 2,
            self.window.height - 350,
            arcade.color.AMAZON,
            32,
            anchor_x="center",
            anchor_y="center",
            align="center",
            width=self.window.width,
        )

        arcade.draw_text(
            "New Game (N)",
            self.window.width / 2,
            self.window.height - 450,
            arcade.color.AMAZON,
            32,
            anchor_x="center",
            anchor_y="center",
            align="center",
            width=self.window.width,
        )
        arcade.draw_text(
            "Battle Screen (B)",
            self.window.width / 2,
            self.window.height - 550,
            arcade.color.AMAZON,
            32,
            anchor_x="center",
            anchor_y="center",
            align="center",
            width=self.window.width,
        )

    def setup(self):
        pass

    def on_show_view(self):
        arcade.set_background_color(arcade.color.ALMOND)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            self.window.show_view(self.window.views["game"])
        elif symbol == arcade.key.Y:
            self.window.show_view(self.window.views["settings"])
        elif symbol == arcade.key.Q:
            self.window.close()
        elif symbol == arcade.key.N:
            self.window.views["game"].setup()
            self.window.show_view(self.window.views["game"])
        elif symbol == arcade.key.B:
            self.window.views["battle"].setup()
            self.window.show_view(self.window.views["battle"])
