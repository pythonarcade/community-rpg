import sys

import arcade
import arcade.hitbox

from rpg import debug_tools

MOVEMENT_SPEED = 3


class ViewGame(arcade.View):
    def __init__(self):
        super().__init__()

        self.player_sprite = debug_tools.TestPlayer()

        self.tile_map = arcade.load_tilemap(
            ":assets:world.tmj", hit_box_algorithm=arcade.hitbox.algo_bounding_box
        )

        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, [self.scene["cliffs"], self.scene["forest"]]
        )

    def on_draw(self):
        self.clear()
        self.scene.draw()
        self.player_sprite.draw()
        debug_tools.draw_hitboxes(self.player_sprite, self.physics_engine)

    def on_update(self, delta_time):
        self.player_sprite.update()
        self.physics_engine.update()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if key in [arcade.key.UP, arcade.key.DOWN]:
            self.player_sprite.change_y = 0
        elif key in [arcade.key.LEFT, arcade.key.RIGHT]:
            self.player_sprite.change_x = 0
