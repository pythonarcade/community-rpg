import math
import random

import arcade

from rpg.sprites.character_sprite import CharacterSprite


class RandomWalkingSprite(CharacterSprite):
    """
    Simple character that walks randomly around the map
    """

    MAX_PATH_DISTANCE = 350

    def __init__(self, sheet_name, scene, speed=1):
        super().__init__(sheet_name)
        self.speed = speed
        self.scene = scene
        self.destination = None
        self.wall_list = None

    def on_update(self, delta_time):
        super().on_update(delta_time)

        # Don't start until we have a wall_list available
        if not self.wall_list:
            if self.scene.get_sprite_list("wall_list"):
                self.wall_list = self.scene.get_sprite_list("wall_list")
            else:
                return

        x1 = self.center_x
        y1 = self.center_y

        # Decide a new random destination if we don't have one
        if not self.destination:
            x2 = x1 + random.randint(-self.MAX_PATH_DISTANCE, self.MAX_PATH_DISTANCE)
            y2 = y1 + random.randint(-self.MAX_PATH_DISTANCE, self.MAX_PATH_DISTANCE)
            self.destination = (x2, y2)
        else:
            x2 = self.destination[0]
            y2 = self.destination[1]

        distance = arcade.get_distance(x1, y1, x2, y2)
        if distance < self.speed:
            self.destination = None

        # Figure out the angle between
        angle = math.atan2(y2 - y1, x2 - x1)

        # Figure out the vector at the given speed
        self.change_x = math.cos(angle) * self.speed
        self.change_y = math.sin(angle) * self.speed

        # Move the character
        self.center_x += self.change_x
        walls_hit_x = arcade.check_for_collision_with_list(self, self.wall_list)
        for wall in walls_hit_x:
            if self.change_x > 0:
                self.right = wall.left
            elif self.change_y < 0:
                self.left = wall.right

        self.center_y += self.change_y
        walls_hit_y = arcade.check_for_collision_with_list(self, self.wall_list)
        for wall in walls_hit_y:
            if self.change_y > 0:
                self.top = wall.bottom
            elif self.change_y < 0:
                self.bottom = wall.top

        # Find a new destination if we hit a wall
        if walls_hit_x or walls_hit_y:
            self.destination = None
