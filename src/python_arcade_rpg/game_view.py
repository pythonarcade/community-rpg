"""
Main game view
"""

import json
from constants import *
from character_sprite import CharacterSprite
from message_box import MessageBox


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

        # Physics engine
        self.physics_engine = None

        # Maps
        self.map_list = map_list

        # Name of map we are on
        self.cur_map_name = None

        self.message_box = None
        self.selected_item = 1

        f = open("item_dictionary.json")
        self.item_dictionary = json.load(f)

        f = open("characters_dictionary.json")
        self.enemy_dictionary = json.load(f)

        # Cameras
        self.camera_sprites = arcade.Camera(self.window, self.window.width, self.window.height)
        self.camera_gui = arcade.Camera(self.window, self.window.width, self.window.height)

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

        map_height = my_map.map_size[1]
        self.player_sprite.center_x = start_x * SPRITE_SIZE + SPRITE_SIZE / 2
        self.player_sprite.center_y = (map_height - start_y) * SPRITE_SIZE - SPRITE_SIZE / 2
        self.scroll_to_player(1.0)
        self.player_sprite_list = arcade.SpriteList()
        self.player_sprite_list.append(self.player_sprite)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                         my_map.wall_list)

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """

        # Create the player character
        self.player_sprite = CharacterSprite("characters/Female/Female 18-4.png")

        # Spawn the player
        start_x = STARTING_X
        start_y = STARTING_Y
        self.switch_map(STARTING_MAP, start_x, start_y)
        self.cur_map_name = STARTING_MAP

    def draw_inventory(self):
        capacity = 10

        field_width = self.window.width / (capacity + 1)

        x = self.window.width / 2
        y = 40

        arcade.draw_rectangle_filled(x, y, self.window.width, 80, arcade.color.ALMOND)
        for i in range(capacity):
            y = 40
            x = i * field_width + 5
            if i == self.selected_item - 1:
                arcade.draw_lrtb_rectangle_outline(x - 3,
                                                   x + field_width - 5,
                                                   y + 20,
                                                   y - 5,
                                                   arcade.color.BLACK,
                                                   2)

            if len(self.player_sprite.inventory) > i:
                item_name = self.player_sprite.inventory[i]['short_name']
            else:
                item_name = ""

            text = f"{i + 1}: {item_name}"
            arcade.draw_text(text, x, y, arcade.color.ALLOY_ORANGE)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        # Use the scrolling camera for sprites
        self.camera_sprites.use()

        # Grab each tile layer from the map
        map_layers = self.map_list[self.cur_map_name].map_layers

        # Draw each tile layer from the map
        for map_layer_name in map_layers:
            map_layers[map_layer_name].draw()

        # Draw all the enemies
        self.map_list[self.cur_map_name].characters.draw()

        # Draw the player
        self.player_sprite_list.draw()
        # print(self.player_sprite.position)

        # Use the non-scrolled GUI camera
        self.camera_gui.use()

        # Draw the inventory
        self.draw_inventory()

        # Draw any message boxes
        if self.message_box:
            self.message_box.on_draw()

    def scroll_to_player(self, speed=CAMERA_SPEED):
        """ Manage Scrolling """

        position = self.player_sprite.center_x - self.window.width / 2, \
            self.player_sprite.center_y - self.window.height / 2
        self.camera_sprites.move_to(position, speed)

    def on_show_view(self):
        # Set background color
        my_map = self.map_list[self.cur_map_name]
        if my_map.background_color:
            arcade.set_background_color(my_map.background_color)

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

        # Update the characters
        self.map_list[self.cur_map_name].characters.on_update(delta_time)

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

        if self.message_box:
            self.message_box.on_key_press(key, modifiers)
            return

        if key in KEY_UP:
            self.up_pressed = True
        elif key in KEY_DOWN:
            self.down_pressed = True
        elif key in KEY_LEFT:
            self.left_pressed = True
        elif key in KEY_RIGHT:
            self.right_pressed = True
        elif key in INVENTORY:
            self.window.show_view(self.window.views['inventory'])
        elif key == arcade.key.ESCAPE:
            self.window.show_view(self.window.views['main_menu'])
        elif key in SEARCH:
            self.search()
        elif key == arcade.key.KEY_1:
            self.selected_item = 1
        elif key == arcade.key.KEY_2:
            self.selected_item = 2
        elif key == arcade.key.KEY_3:
            self.selected_item = 3
        elif key == arcade.key.KEY_4:
            self.selected_item = 4
        elif key == arcade.key.KEY_5:
            self.selected_item = 5
        elif key == arcade.key.KEY_6:
            self.selected_item = 6
        elif key == arcade.key.KEY_7:
            self.selected_item = 7
        elif key == arcade.key.KEY_8:
            self.selected_item = 8
        elif key == arcade.key.KEY_9:
            self.selected_item = 9
        elif key == arcade.key.KEY_0:
            self.selected_item = 10

    def close_message_box(self):
        self.message_box = None

    def search(self):
        """ Search for things """
        map_layers = self.map_list[self.cur_map_name].map_layers
        if 'searchable' not in map_layers:
            print(f"No searchable sprites on {self.cur_map_name} map layer.")
            return

        searchable_sprites = map_layers['searchable']
        sprites_in_range = arcade.check_for_collision_with_list(self.player_sprite, searchable_sprites)
        print(f"Found {len(sprites_in_range)} searchable sprite(s) in range.")
        for sprite in sprites_in_range:
            if 'item' in sprite.properties:
                self.message_box = MessageBox(self, f"Found: {sprite.properties['item']}")
                sprite.remove_from_sprite_lists()
                lookup_item = self.item_dictionary[sprite.properties['item']]
                self.player_sprite.inventory.append(lookup_item)
            else:
                print("The 'item' property was not set for the sprite. Can't get any items from this.")

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

    def on_resize(self, width, height):
        """
        Resize window
        Handle the user grabbing the edge and resizing the window.
        """
        self.camera_sprites.resize(width, height)
        self.camera_gui.resize(width, height)
