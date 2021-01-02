"""
Animated sprite for characters that walk around.
"""


import arcade
from constants import SPRITE_SIZE


class CharacterSprite(arcade.Sprite):
    def __init__(self, sheet_name):
        super().__init__()
        self.textures = arcade.load_spritesheet(sheet_name,
                                                sprite_width=SPRITE_SIZE,
                                                sprite_height=SPRITE_SIZE,
                                                columns=3,
                                                count=12)
        self.cur_texture_index = 0
        self.texture = self.textures[self.cur_texture_index]
        self.inventory = []

    def on_update(self, delta_time):
        if not self.change_x and not self.change_y:
            return

        # self.center_x += self.change_x
        # self.center_y += self.change_y

        self.cur_texture_index += 1
        if self.change_x > 0:
            if self.cur_texture_index < 6:
                self.cur_texture_index = 6
            elif self.cur_texture_index > 8:
                self.cur_texture_index = 6
        elif self.change_x < 0:
            if self.cur_texture_index < 3:
                self.cur_texture_index = 3
            elif self.cur_texture_index > 5:
                self.cur_texture_index = 3
        elif self.change_y > 0:
            if self.cur_texture_index < 9:
                self.cur_texture_index = 9
            elif self.cur_texture_index > 11:
                self.cur_texture_index = 9
        else:
            if self.cur_texture_index < 0:
                self.cur_texture_index = 0
            elif self.cur_texture_index > 2:
                self.cur_texture_index = 0

        self.texture = self.textures[self.cur_texture_index]
