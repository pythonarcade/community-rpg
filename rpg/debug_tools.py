import arcade


class TestPlayer(arcade.Sprite):
    def __init__(
        self,
        path_or_texture=":resources:images/animated_characters/female_person/femalePerson_idle.png",
        scale=0.3,
        center_x=50,
        center_y=50,
    ):
        super().__init__(path_or_texture, scale, center_x, center_y)

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y


def draw_hitboxes(
    player_sprite=None,
    physics_engine=None,
    player_color=arcade.color.BLUE,
    wall_color=arcade.color.RED,
):
    player_sprite.draw_hit_box(player_color)
    for wall in physics_engine.walls:
        wall.draw_hit_boxes(wall_color)
