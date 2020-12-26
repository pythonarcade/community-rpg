import arcade

from constants import MESSAGE_BOX_FONT_SIZE
from constants import MESSAGE_BOX_MARGIN


class MessageBox:
    def __init__(self, view, message):
        self.message = message
        self.view = view

        cx = self.view.window.width / 2 + self.view.view_left
        cy = self.view.window.height / 2 + self.view.view_bottom
        self.text_sprite = arcade.draw_text(self.message,
                                            cx,
                                            cy,
                                            arcade.color.ALLOY_ORANGE,
                                            MESSAGE_BOX_FONT_SIZE,
                                            anchor_x="center", anchor_y="center", align="center")

    def on_draw(self):
        arcade.draw_rectangle_filled(self.text_sprite.center_x,
                                     self.text_sprite.center_y,
                                     self.text_sprite.width + MESSAGE_BOX_MARGIN * 2,
                                     self.text_sprite.height + MESSAGE_BOX_MARGIN * 2,
                                     arcade.color.ALMOND)
        arcade.draw_rectangle_outline(self.text_sprite.center_x,
                                      self.text_sprite.center_y,
                                      self.text_sprite.width + MESSAGE_BOX_MARGIN * 2,
                                      self.text_sprite.height + MESSAGE_BOX_MARGIN * 2,
                                      arcade.color.ALLOY_ORANGE,
                                      4)

        self.text_sprite.draw()

    def on_key_press(self, _key, _modifiers):
        self.view.close_message_box()
