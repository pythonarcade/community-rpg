"""
Main game view
"""

import json
from functools import partial
from typing import Callable

import arcade
import arcade.gui
import rpg.constants as constants
from arcade.experimental.lights import Light
from pyglet.math import Vec2
from rpg.message_box import MessageBox
from rpg.sprites.player_sprite import PlayerSprite


class DebugMenu(arcade.gui.UIBorder, arcade.gui.UIWindowLikeMixin):
    def __init__(
        self,
        *,
        width: float,
        height: float,
        noclip_callback: Callable,
        hyper_callback: Callable,
    ):

        self.off_style = {
            "bg_color": arcade.color.BLACK,
        }

        self.on_style = {
            "bg_color": arcade.color.REDWOOD,
        }

        self.setup_noclip(noclip_callback)
        self.setup_hyper(hyper_callback)

        space = 10

        self._title = arcade.gui.UITextArea(
            text="DEBUG MENU",
            width=width - space,
            height=height - space,
            font_size=14,
            text_color=arcade.color.BLACK,
        )

        group = arcade.gui.UIPadding(
            bg_color=(255, 255, 255, 255),
            child=arcade.gui.UILayout(
                width=width,
                height=height,
                children=[
                    arcade.gui.UIAnchorWidget(
                        child=self._title,
                        anchor_x="left",
                        anchor_y="top",
                        align_x=10,
                        align_y=-10,
                    ),
                    arcade.gui.UIAnchorWidget(
                        child=arcade.gui.UIBoxLayout(
                            x=0,
                            y=0,
                            children=[
                                arcade.gui.UIPadding(
                                    child=self.noclip_button, pading=(5, 5, 5, 5)
                                ),
                                arcade.gui.UIPadding(
                                    child=self.hyper_button, padding=(5, 5, 5, 5)
                                ),
                            ],
                            vertical=False,
                        ),
                        anchor_x="left",
                        anchor_y="bottom",
                        align_x=5,
                    ),
                ],
            ),
        )

        # x and y don't seem to actually change where this is created. bug?
        # TODO: make this not appear at the complete bottom left (top left would be better?)
        super().__init__(border_width=5, child=group)

    def setup_noclip(self, callback: Callable):
        # disable player collision

        def toggle(*args):
            # toggle state on click
            self.noclip_status = True if not self.noclip_status else False
            self.noclip_button._style = (
                self.off_style if not self.noclip_status else self.on_style
            )
            self.noclip_button.clear()

            callback(status=self.noclip_status)

        self.noclip_status = False
        self.noclip_button = arcade.gui.UIFlatButton(
            text="noclip", style=self.off_style
        )
        self.noclip_button.on_click = toggle  # type: ignore

    def setup_hyper(self, callback: Callable):
        # increase player speed

        def toggle(*args):
            # toggle state on click
            self.hyper_status = True if not self.hyper_status else False
            self.hyper_button._style = (
                self.off_style if not self.hyper_status else self.on_style
            )
            self.hyper_button.clear()

            callback(status=self.hyper_status)

        self.hyper_status = False

        self.hyper_button = arcade.gui.UIFlatButton(text="hyper", style=self.off_style)
        self.hyper_button.on_click = toggle  # type: ignore


class GameView(arcade.View):
    """
    Main application class.
    """

    def __init__(self, map_list):
        super().__init__()

        arcade.set_background_color(arcade.color.AMAZON)

        self.setup_debug_menu()

        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager.enable()

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

        # Selected Items Hotbar
        self.hotbar_sprite_list = None
        self.selected_item = 1

        f = open("resources/data/item_dictionary.json")
        self.item_dictionary = json.load(f)

        f = open("resources/data/characters_dictionary.json")
        self.enemy_dictionary = json.load(f)

        # Cameras
        self.camera_sprites = arcade.Camera(self.window.width, self.window.height)
        self.camera_gui = arcade.Camera(self.window.width, self.window.height)

        # Create a small white light
        x = 100
        y = 200
        radius = 150
        mode = "soft"
        color = arcade.csscolor.WHITE
        self.player_light = Light(x, y, radius, color, mode)

    def switch_map(self, map_name, start_x, start_y):
        """
        Switch the current map
        :param map_name: Name of map to switch to
        :param start_x: Grid x location to spawn at
        :param start_y: Grid y location to spawn at
        """
        self.cur_map_name = map_name

        try:
            self.my_map = self.map_list[self.cur_map_name]
        except KeyError:
            raise KeyError(f"Unable to find map named '{map_name}'.")

        if self.my_map.background_color:
            arcade.set_background_color(self.my_map.background_color)

        map_height = self.my_map.map_size[1]
        self.player_sprite.center_x = (
            start_x * constants.SPRITE_SIZE + constants.SPRITE_SIZE / 2
        )
        self.player_sprite.center_y = (
            map_height - start_y
        ) * constants.SPRITE_SIZE - constants.SPRITE_SIZE / 2
        self.scroll_to_player(1.0)
        self.player_sprite_list = arcade.SpriteList()
        self.player_sprite_list.append(self.player_sprite)

        self.setup_physics()

        if self.my_map.light_layer:
            self.my_map.light_layer.resize(self.window.width, self.window.height)

    def setup_physics(self):
        if self.noclip_status:
            # make an empty spritelist so the character does not collide with anyting
            self.physics_engine = arcade.PhysicsEngineSimple(
                self.player_sprite, arcade.SpriteList()
            )
        else:
            # use the walls as normal
            self.physics_engine = arcade.PhysicsEngineSimple(
                self.player_sprite, self.my_map.scene["wall_list"]
            )

    def setup(self):
        """Set up the game variables. Call to re-start the game."""

        # Create the player character
        self.player_sprite = PlayerSprite(":characters:Female/Female 18-4.png")

        # Spawn the player
        start_x = constants.STARTING_X
        start_y = constants.STARTING_Y
        self.switch_map(constants.STARTING_MAP, start_x, start_y)
        self.cur_map_name = constants.STARTING_MAP

        # Set up the hotbar
        self.load_hotbar_sprites()

    def load_hotbar_sprites(self):
        """Load the sprites for the hotbar at the bottom of the screen.

        Loads the controls sprite tileset and selects only the number pad button sprites.
        These will be visual representations of number keypads (1️⃣, 2️⃣, 3️⃣, ..., 0️⃣)
        to clarify that the hotkey bar can be accessed through these keypresses.
        """

        first_number_pad_sprite_index = 51
        last_number_pad_sprite_index = 61

        self.hotbar_sprite_list = arcade.load_spritesheet(
            file_name="resources/tilesets/input_prompts_kenney.png",
            sprite_width=16,
            sprite_height=16,
            columns=34,
            count=816,
            margin=1,
        )[first_number_pad_sprite_index:last_number_pad_sprite_index]

    def setup_debug_menu(self):
        self.debug = False

        self.debug_menu = DebugMenu(
            width=450,
            height=200,
            noclip_callback=self.noclip,
            hyper_callback=self.hyper,
        )

        self.original_movement_speed = constants.MOVEMENT_SPEED
        self.noclip_status = False

    def enable_debug_menu(self):
        self.ui_manager.add(self.debug_menu)

    def disable_debug_menu(self):
        self.ui_manager.remove(self.debug_menu)

    def noclip(self, *args, status: bool):
        self.noclip_status = status

        self.setup_physics()

    def hyper(self, *args, status: bool):
        constants.MOVEMENT_SPEED = (
            int(self.original_movement_speed * 3.5)
            if status
            else self.original_movement_speed
        )

    def draw_inventory(self):
        capacity = 10
        vertical_hotbar_location = 40
        hotbar_height = 80
        sprite_height = 16

        field_width = self.window.width / (capacity + 1)

        x = self.window.width / 2
        y = vertical_hotbar_location

        arcade.draw_rectangle_filled(
            x, y, self.window.width, hotbar_height, arcade.color.ALMOND
        )
        for i in range(capacity):
            y = vertical_hotbar_location
            x = i * field_width + 5
            if i == self.selected_item - 1:
                arcade.draw_lrtb_rectangle_outline(
                    x - 6, x + field_width - 15, y + 25, y - 10, arcade.color.BLACK, 2
                )

            if len(self.player_sprite.inventory) > i:
                item_name = self.player_sprite.inventory[i]["short_name"]
            else:
                item_name = ""

            hotkey_sprite = self.hotbar_sprite_list[i]
            hotkey_sprite.draw_scaled(x + sprite_height / 2, y + sprite_height / 2, 2.0)
            # Add whitespace so the item text doesn't hide behind the number pad sprite
            text = f"     {item_name}"
            arcade.draw_text(text, x, y, arcade.color.ALLOY_ORANGE, 16)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()
        cur_map = self.map_list[self.cur_map_name]

        # --- Light related ---
        # Everything that should be affected by lights gets rendered inside this
        # 'with' statement. Nothing is rendered to the screen yet, just the light
        # layer.
        with cur_map.light_layer:
            arcade.set_background_color(cur_map.background_color)

            # Use the scrolling camera for sprites
            self.camera_sprites.use()

            # Grab each tile layer from the map
            map_layers = cur_map.map_layers

            # Draw scene
            cur_map.scene.draw()

            for item in map_layers.get("searchable", []):
                arcade.Sprite(
                    filename=":misc:shiny-stars.png",
                    center_x=item.center_x,
                    center_y=item.center_y,
                    scale=0.8,
                ).draw()

            # Draw the player
            self.player_sprite_list.draw()

        if cur_map.light_layer:
            # Draw the light layer to the screen.
            # This fills the entire screen with the lit version
            # of what we drew into the light layer above.
            if cur_map.properties and "ambient_color" in cur_map.properties:
                ambient_color = cur_map.properties["ambient_color"]
                # ambient_color = (ambient_color.green, ambient_color.blue, ambient_color.alpha, ambient_color.red)
            else:
                ambient_color = arcade.color.WHITE
            cur_map.light_layer.draw(ambient_color=ambient_color)

        # Use the non-scrolled GUI camera
        self.camera_gui.use()

        # Draw the inventory
        self.draw_inventory()

        # Draw any message boxes
        if self.message_box:
            self.message_box.on_draw()

        # draw GUI
        self.ui_manager.draw()

    def scroll_to_player(self, speed=constants.CAMERA_SPEED):
        """Manage Scrolling"""

        vector = Vec2(
            self.player_sprite.center_x - self.window.width / 2,
            self.player_sprite.center_y - self.window.height / 2,
        )
        self.camera_sprites.move_to(vector, speed)

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

        MOVING_UP = (
            self.up_pressed
            and not self.down_pressed
            and not self.right_pressed
            and not self.left_pressed
        )

        MOVING_DOWN = (
            self.down_pressed
            and not self.up_pressed
            and not self.right_pressed
            and not self.left_pressed
        )

        MOVING_RIGHT = (
            self.right_pressed
            and not self.left_pressed
            and not self.up_pressed
            and not self.down_pressed
        )

        MOVING_LEFT = (
            self.left_pressed
            and not self.right_pressed
            and not self.up_pressed
            and not self.down_pressed
        )

        MOVING_UP_LEFT = (
            self.up_pressed
            and self.left_pressed
            and not self.down_pressed
            and not self.right_pressed
        )

        MOVING_DOWN_LEFT = (
            self.down_pressed
            and self.left_pressed
            and not self.up_pressed
            and not self.right_pressed
        )

        MOVING_UP_RIGHT = (
            self.up_pressed
            and self.right_pressed
            and not self.down_pressed
            and not self.left_pressed
        )

        MOVING_DOWN_RIGHT = (
            self.down_pressed
            and self.right_pressed
            and not self.up_pressed
            and not self.left_pressed
        )

        if MOVING_UP:
            self.player_sprite.change_y = constants.MOVEMENT_SPEED

        if MOVING_DOWN:
            self.player_sprite.change_y = -constants.MOVEMENT_SPEED

        if MOVING_LEFT:
            self.player_sprite.change_x = -constants.MOVEMENT_SPEED

        if MOVING_RIGHT:
            self.player_sprite.change_x = constants.MOVEMENT_SPEED

        if MOVING_UP_LEFT:
            self.player_sprite.change_y = constants.MOVEMENT_SPEED / 1.5
            self.player_sprite.change_x = -constants.MOVEMENT_SPEED / 1.5

        if MOVING_UP_RIGHT:
            self.player_sprite.change_y = constants.MOVEMENT_SPEED / 1.5
            self.player_sprite.change_x = constants.MOVEMENT_SPEED / 1.5

        if MOVING_DOWN_LEFT:
            self.player_sprite.change_y = -constants.MOVEMENT_SPEED / 1.5
            self.player_sprite.change_x = -constants.MOVEMENT_SPEED / 1.5

        if MOVING_DOWN_RIGHT:
            self.player_sprite.change_y = -constants.MOVEMENT_SPEED / 1.5
            self.player_sprite.change_x = constants.MOVEMENT_SPEED / 1.5

        # Call update to move the sprite
        self.physics_engine.update()

        # Update player animation
        self.player_sprite_list.on_update(delta_time)

        self.player_light.position = self.player_sprite.position

        # Update the characters
        try:
            self.map_list[self.cur_map_name].scene["characters"].on_update(delta_time)
        except KeyError:
            # no characters on map
            pass

        # --- Manage doors ---
        map_layers = self.map_list[self.cur_map_name].map_layers

        # Is there as layer named 'doors'?
        if "doors" in map_layers:
            # Did we hit a door?
            doors_hit = arcade.check_for_collision_with_list(
                self.player_sprite, map_layers["doors"]
            )
            # We did!
            if len(doors_hit) > 0:
                try:
                    # Grab the info we need
                    map_name = doors_hit[0].properties["map_name"]
                    start_x = doors_hit[0].properties["start_x"]
                    start_y = doors_hit[0].properties["start_y"]
                except KeyError:
                    raise KeyError(
                        "Door objects must have 'map_name', 'start_x', and 'start_y' properties defined."
                    )

                # Swap to the new map
                self.switch_map(map_name, start_x, start_y)
            else:
                # We didn't hit a door, scroll normally
                self.scroll_to_player()
        else:
            # No doors, scroll normally
            self.scroll_to_player()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if self.message_box:
            self.message_box.on_key_press(key, modifiers)
            return

        if key in constants.KEY_UP:
            self.up_pressed = True
        elif key in constants.KEY_DOWN:
            self.down_pressed = True
        elif key in constants.KEY_LEFT:
            self.left_pressed = True
        elif key in constants.KEY_RIGHT:
            self.right_pressed = True
        elif key in constants.INVENTORY:
            self.window.show_view(self.window.views["inventory"])
        elif key == arcade.key.ESCAPE:
            self.window.show_view(self.window.views["main_menu"])
        elif key in constants.SEARCH:
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
        elif key == arcade.key.L:
            cur_map = self.map_list[self.cur_map_name]
            if self.player_light in cur_map.light_layer:
                cur_map.light_layer.remove(self.player_light)
            else:
                cur_map.light_layer.add(self.player_light)
        elif key == arcade.key.GRAVE:  # `
            # toggle debug
            self.debug = True if not self.debug else False
            if self.debug:
                self.enable_debug_menu()
            else:
                self.disable_debug_menu()

    def close_message_box(self):
        self.message_box = None

    def search(self):
        """Search for things"""
        map_layers = self.map_list[self.cur_map_name].map_layers
        if "searchable" not in map_layers:
            print(f"No searchable sprites on {self.cur_map_name} map layer.")
            return

        searchable_sprites = map_layers["searchable"]
        sprites_in_range = arcade.check_for_collision_with_list(
            self.player_sprite, searchable_sprites
        )
        print(f"Found {len(sprites_in_range)} searchable sprite(s) in range.")
        for sprite in sprites_in_range:
            if "item" in sprite.properties:
                self.message_box = MessageBox(
                    self, f"Found: {sprite.properties['item']}"
                )
                sprite.remove_from_sprite_lists()
                lookup_item = self.item_dictionary[sprite.properties["item"]]
                self.player_sprite.inventory.append(lookup_item)
            else:
                print(
                    "The 'item' property was not set for the sprite. Can't get any items from this."
                )

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key in constants.KEY_UP:
            self.up_pressed = False
        elif key in constants.KEY_DOWN:
            self.down_pressed = False
        elif key in constants.KEY_LEFT:
            self.left_pressed = False
        elif key in constants.KEY_RIGHT:
            self.right_pressed = False

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """Called whenever the mouse moves."""
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """Called when the user presses a mouse button."""
        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.player_sprite.destination_point = x, y

    def on_mouse_release(self, x, y, button, key_modifiers):
        """Called when a user releases a mouse button."""
        pass

    def on_resize(self, width, height):
        """
        Resize window
        Handle the user grabbing the edge and resizing the window.
        """
        self.camera_sprites.resize(width, height)
        self.camera_gui.resize(width, height)
        cur_map = self.map_list[self.cur_map_name]
        if cur_map.light_layer:
            cur_map.light_layer.resize(width, height)
