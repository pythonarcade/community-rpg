import sys

import arcade
import arcade.hitbox
from pyglet.math import Vec2

from rpg import debug_tools
from constants import MOVEMENT_SPEED


class ViewGame(arcade.View):
    def __init__(self):
        super().__init__()

        # Player
        self.player_sprite = debug_tools.TestPlayer()
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # Map And Scene
        self.tile_map = arcade.load_tilemap(
            ":assets:world.tmj", hit_box_algorithm=arcade.hitbox.algo_simple
        )
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Physics
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, [self.scene["cliffs"], self.scene["forest"]]
        )

        # Cameras
        self.camera_sprites = arcade.Camera()
        self.camera_gui = arcade.Camera()

    def set_player_movement_state(self, key, value):
        if key == arcade.key.UP:
            self.up_pressed = value
        elif key == arcade.key.DOWN:
            self.down_pressed = value
        elif key == arcade.key.LEFT:
            self.left_pressed = value
        elif key == arcade.key.RIGHT:
            self.right_pressed = value

    def player_movement(self):
        self.player_sprite.change_x, self.player_sprite.change_y = 0, 0

        if self.up_pressed:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif self.down_pressed:
            self.player_sprite.change_y = -MOVEMENT_SPEED

        if self.left_pressed:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif self.right_pressed:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def scroll_to_player(self, speed=1):
        vector = Vec2(
            self.player_sprite.center_x - self.window.width / 2,
            self.player_sprite.center_y - self.window.height / 2,
        )
        self.camera_sprites.move_to(vector, speed)

    def on_draw(self):
        self.clear()
        self.camera_sprites.use()
        self.scene.draw()
        self.player_sprite.draw()
        debug_tools.draw_hitboxes(self.player_sprite, self.physics_engine)

        # GUI
        self.camera_gui.use()

    def on_update(self, delta_time):
        self.player_sprite.update()
        self.physics_engine.update()
        self.scroll_to_player()

    def on_key_press(self, key, modifiers):
        self.set_player_movement_state(key, True)
        self.player_movement()

    def on_key_release(self, key, modifiers):
        self.set_player_movement_state(key, False)
        self.player_movement()

    def on_resize(self, width, height):
        self.camera_sprites.resize(int(width), int(height))
        self.camera_gui.resize(int(width), int(height))
