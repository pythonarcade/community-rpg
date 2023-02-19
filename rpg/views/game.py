import arcade


class ViewGame(arcade.View):
    def __init__(self):
        super().__init__()

        self.tile_map = arcade.load_tilemap(":assets:world.tmj")

        self.scene = arcade.Scene.from_tilemap(self.tile_map)

    def on_draw(self):
        self.clear()
        self.scene.draw()
