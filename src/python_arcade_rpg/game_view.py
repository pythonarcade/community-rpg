import arcade

from constants import *

from game_map import load_maps
from character import Character

class GameView(arcade.View):
    """
    Main application class.
    """

    def __init__(self, map_list):
        super().__init__()

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
        self.map_list = map_list

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
        self.player_sprite_list.on_update(delta_time)

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
