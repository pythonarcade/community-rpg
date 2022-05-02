import math

import arcade

from rpg.sprites.character_sprite import CharacterSprite


class PathFollowingSprite(CharacterSprite):
    """
    Simple character that follows a pre-defined path of points
    """

    def __init__(self, sheet_name):
        super().__init__(sheet_name)
        self.path = []
        self.cur_point = 0
        self.speed = 1

    def on_update(self, delta_time):
        super().on_update(delta_time)

        # Do we have a path?
        if not self.path or len(self.path) == 0:
            print("No path for path following sprite")
            return

        # Grab the current point, and the point we are headed to
        x1 = self.center_x
        y1 = self.center_y
        x2 = self.path[self.cur_point][0]
        y2 = self.path[self.cur_point][1]

        # The distance between
        distance = arcade.get_distance(x1, y1, x2, y2)

        # Are we close to the destination point? If so, advance to the next point.
        if distance <= self.speed:
            self.cur_point += 1
            if self.cur_point >= len(self.path):
                self.cur_point = 0
            return

        # Figure out the angle between
        angle = math.atan2(y2 - y1, x2 - x1)

        # Figure out our vector given the speed
        self.change_x = math.cos(angle) * self.speed
        self.change_y = math.sin(angle) * self.speed

        # Move the character
        self.center_x += self.change_x
        self.center_y += self.change_y
