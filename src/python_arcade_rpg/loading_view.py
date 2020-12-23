import arcade
from game_map import load_maps
from game_view import GameView

class LoadingView(arcade.View):
    def __init__(self):
        super().__init__()
        self.started = False
        arcade.set_background_color(arcade.color.ALMOND)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Loading...",
                         self.window.width / 2,
                         self.window.height / 2,
                         arcade.color.ALLOY_ORANGE,
                         44,
                         anchor_x="center", anchor_y="center", align="center")
        self.started = True

    def setup(self):
        pass

    def on_update(self, delta_time: float):
        # Dictionary to hold all our maps
        if self.started:
            self.map_list = load_maps()
            start_view = GameView(self.map_list)
            start_view.setup()
            self.window.show_view(start_view)
