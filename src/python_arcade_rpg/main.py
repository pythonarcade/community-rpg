"""
Python Arcade Community RPG

An open-source RPG
"""
from collections import OrderedDict
import os
from os.path import isfile, join
import arcade

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Python Community RPG"
TILE_SCALING = 1.0
SPRITE_SIZE = 32

# How fast does the player move
MOVEMENT_SPEED = 3

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 300
RIGHT_VIEWPORT_MARGIN = 300
BOTTOM_VIEWPORT_MARGIN = 300
TOP_VIEWPORT_MARGIN = 300

# What map, and what position we start at
STARTING_MAP = "main_map"
STARTING_X = 33
STARTING_Y = 16

# Key mappings
KEY_UP = [arcade.key.UP, arcade.key.W]
KEY_DOWN = [arcade.key.DOWN, arcade.key.S]
KEY_LEFT = [arcade.key.LEFT, arcade.key.A]
KEY_RIGHT = [arcade.key.RIGHT, arcade.key.D]


class GameMap:
    name = None
    map_layers = None
    wall_list = None
    map_size = None
    background_color = arcade.color.AMAZON


def load_map(map_name):

    game_map = GameMap()
    game_map.map_layers = OrderedDict()

    # List of blocking sprites
    game_map.wall_list = arcade.SpriteList()

    # Read in the tiled map
    print(f"Loading map: {map_name}")
    my_map = arcade.tilemap.read_tmx(map_name)

    for layer in my_map.layers:

        print(f"  Loading layer: {layer.name}")
        game_map.map_layers[layer.name] = arcade.tilemap.process_layer(map_object=my_map,
                                                                       layer_name=layer.name,
                                                                       scaling=TILE_SCALING,
                                                                       use_spatial_hash=True)

        game_map.map_size = my_map.map_size
        game_map.background_color = my_map.background_color

        # Any layer with '_blocking' in it, will be a wall
        if '_blocking' in layer.name:
            game_map.wall_list.extend(game_map.map_layers[layer.name])

    return game_map


class Character(arcade.Sprite):
    def __init__(self, sheet_name):
        super().__init__()
        self.textures = arcade.load_spritesheet(sheet_name,
                                                sprite_width=SPRITE_SIZE,
                                                sprite_height=SPRITE_SIZE,
                                                columns=3,
                                                count=12)
        self.cur_texture_index = 0
        self.texture = self.textures[self.cur_texture_index]

    def update(self):
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


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)

        arcade.set_background_color(arcade.color.AMAZON)

        # Player sprite
        self.player_sprite = None
        self.player_sprite_list = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # Used in scrolling
        self.view_left = 0
        self.view_bottom = 0

        # Physics engine
        self.physics_engine = None

        # Maps
        self.map_list = None

        # Name of map we are on
        self.cur_map_name = None

    def switch_map(self, map_name, start_x, start_y):
        """
        Switch the current map
        :param map_name: Name of map to switch to
        :param start_x: Grid x location to spawn at
        :param start_y: Grid y location to spawn at
        """
        self.cur_map_name = map_name

        try:
            my_map = self.map_list[self.cur_map_name]
        except KeyError:
            raise KeyError(f"Unable to find map named '{map_name}'.")

        if my_map.background_color:
            arcade.set_background_color(my_map.background_color)

        map_height = my_map.map_size.height
        self.player_sprite.center_x = start_x * SPRITE_SIZE + SPRITE_SIZE / 2
        self.player_sprite.center_y = (map_height - start_y) * SPRITE_SIZE - SPRITE_SIZE / 2
        self.player_sprite_list = arcade.SpriteList()
        self.player_sprite_list.append(self.player_sprite)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                         my_map.wall_list)

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """

        # Create the player character
        self.player_sprite = Character("characters/Female/Female 18-4.png")

        # Dictionary to hold all our maps
        self.map_list = {}

        # Directory to pull maps from
        mypath = "maps"

        # Pull names of all tmx files in that path
        map_file_names = [f[:-4] for f in os.listdir(mypath) if isfile(join(mypath, f)) and f.endswith(".tmx")]

        # Loop and load each file
        for map_name in map_file_names:
            self.map_list[map_name] = load_map(f"maps/{map_name}.tmx")

        # Spawn the player
        start_x = STARTING_X
        start_y = STARTING_Y
        self.switch_map(STARTING_MAP, start_x, start_y)
        self.cur_map_name = STARTING_MAP

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        # Call draw() on all your sprite lists below
        map_layers = self.map_list[self.cur_map_name].map_layers

        for map_layer_name in map_layers:
            map_layers[map_layer_name].draw()
            # print(f"draw {map_layer_name}")

        self.player_sprite_list.draw()

    def scroll_to_player(self):
        """ Manage Scrolling """

        changed_viewport = False

        # Scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed_viewport = True

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed_viewport = True

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed_viewport = True

        # Scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed_viewport = True

        if changed_viewport:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        """

        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = MOVEMENT_SPEED

        # Call update to move the sprite
        self.physics_engine.update()

        # Update player animation
        self.player_sprite_list.update()

        # --- Manage doors ---
        map_layers = self.map_list[self.cur_map_name].map_layers

        # Is there as layer named 'doors'?
        if 'doors' in map_layers:
            # Did we hit a door?
            doors_hit = arcade.check_for_collision_with_list(self.player_sprite,
                                                             map_layers['doors'])
            # We did!
            if len(doors_hit) > 0:
                try:
                    # Grab the info we need
                    map_name = doors_hit[0].properties['map_name']
                    start_x = doors_hit[0].properties['start_x']
                    start_y = doors_hit[0].properties['start_y']
                except KeyError:
                    raise KeyError("Door objects must have 'map_name', 'start_x', and 'start_y' properties defined.")

                # Swap to the new map
                self.switch_map(map_name, start_x, start_y)

        # Scroll the window to the player
        self.scroll_to_player()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key in KEY_UP:
            self.up_pressed = True
        elif key in KEY_DOWN:
            self.down_pressed = True
        elif key in KEY_LEFT:
            self.left_pressed = True
        elif key in KEY_RIGHT:
            self.right_pressed = True

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key in KEY_UP:
            self.up_pressed = False
        elif key in KEY_DOWN:
            self.down_pressed = False
        elif key in KEY_LEFT:
            self.left_pressed = False
        elif key in KEY_RIGHT:
            self.right_pressed = False

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """ Called whenever the mouse moves. """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """ Called when the user presses a mouse button. """
        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.player_sprite.destination_point = x, y

    def on_mouse_release(self, x, y, button, key_modifiers):
        """ Called when a user releases a mouse button. """
        pass


def main():
    """ Main method """
    game = MyGame()
    game.center_window()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
