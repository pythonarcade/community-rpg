import arcade
from pyglet.media.codecs import have_ffmpeg, registry

from rpg.character_sprite import CharacterSprite
from rpg.constants import SPRITE_SIZE


class PlayerSprite(CharacterSprite):
    def __init__(self, sheet_name):
        super().__init__(sheet_name)
        self.sound_update = 0
        self.footstep_sound = arcade.load_sound(":sounds:footstep00.wav")

    def on_update(self, delta_time):
        if not self.change_x and not self.change_y:
            return

        # self.center_x += self.change_x
        # self.center_y += self.change_y

        if self.should_update <= 3:
            self.should_update += 1
        else:
            self.should_update = 0
            self.cur_texture_index += 1
            self.sound_update += 1
            if self.sound_update >= 7:
                arcade.play_sound(self.footstep_sound)
                self.sound_update = 0

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
