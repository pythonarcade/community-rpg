"""
Load maps
"""
import json
import os
from collections import OrderedDict
from os.path import isfile, join

import arcade
from arcade.experimental.lights import Light, LightLayer

from rpg.character_sprite import CharacterSprite
from rpg.constants import TILE_SCALING
from rpg.path_following_sprite import PathFollowingSprite


class GameMap:
    name = None
    scene = None
    map_layers = None
    light_layer = None
    map_size = None
    properties = None
    background_color = arcade.color.AMAZON


def load_map(map_name):
    """
    Load a map
    """

    game_map = GameMap()
    game_map.map_layers = OrderedDict()

    game_map.light_layer = LightLayer(100, 100)

    # List of blocking sprites

    layer_options = {
        "trees_blocking": {
            "use_spatial_hash": True,
        },
        "misc_blocking": {
            "use_spatial_hash": True,
        },
        "bridges": {
            "use_spatial_hash": True,
        },
        "water_blocking": {
            "use_spatial_hash": True,
        },
    }

    # Read in the tiled map
    print(f"Loading map: {map_name}")
    my_map = arcade.tilemap.load_tilemap(
        map_name, scaling=TILE_SCALING, layer_options=layer_options
    )

    game_map.scene = arcade.Scene.from_tilemap(my_map)

    if "characters" in my_map.object_lists:
        f = open("resources/data/characters_dictionary.json")
        character_dictionary = json.load(f)
        character_object_list = my_map.object_lists["characters"]

        for character_object in character_object_list:

            if "type" not in character_object.properties:
                print(
                    f"No 'type' field for character in map {map_name}. {character_object.properties}"
                )
                continue

            character_type = character_object.properties["type"]
            if character_type not in character_dictionary:
                print(
                    f"Unable to find '{character_type}' in characters_dictionary.json."
                )
                continue

            character_data = character_dictionary[character_type]
            shape = character_object.shape

            if isinstance(shape, list) and len(shape) == 2:
                # Point
                character_sprite = CharacterSprite(
                    f":characters:{character_data['images']}"
                )
                character_sprite.position = shape
            elif isinstance(shape, list) and len(shape[0]) == 2:
                # Rect or polygon.
                location = [shape[0][0], shape[0][1]]
                character_sprite = PathFollowingSprite(
                    f":characters:{character_data['images']}"
                )
                character_sprite.position = location
                path = []
                for point in shape:
                    location = [point[0], point[1]]
                    path.append(location)
                character_sprite.path = path
            else:
                print(
                    f"Unknown shape type for character with shape '{shape}' in map {map_name}."
                )
                continue

            print(f"Adding character {character_type} at {character_sprite.position}")
            game_map.scene.add_sprite("characters", character_sprite)

    if "lights" in my_map.object_lists:
        lights_object_list = my_map.object_lists["lights"]

        for light_object in lights_object_list:
            if "color" not in light_object.properties:
                print(f"No color for light in map {map_name}.")
                continue

            shape = light_object.shape

            if isinstance(shape, list) and len(shape) == 2:
                # Point
                if "radius" in light_object.properties:
                    radius = light_object.properties["radius"]
                else:
                    radius = 150
                mode = "soft"
                color = light_object.properties["color"]
                color = (color.red, color.green, color.blue)
                light = Light(shape[0], shape[1], radius, color, mode)
                game_map.light_layer.add(light)
                print("Added light", color, "radius", radius)
            else:
                print("Failed to add light")
    else:
        # Hack
        x = 0
        y = 0
        radius = 1
        mode = "soft"
        color = arcade.csscolor.WHITE
        dummy_light = Light(x, y, radius, color, mode)
        game_map.light_layer.add(dummy_light)
        print("Added default light")

    # Get all the tiled sprite lists
    # Get all the tiled sprite lists
    game_map.map_layers = my_map.sprite_lists

    # Define the size of the map, in tiles
    game_map.map_size = my_map.width, my_map.height

    # Set the background color
    game_map.background_color = my_map.background_color

    game_map.properties = my_map.properties

    # Any layer with '_blocking' in it, will be a wall
    game_map.scene.add_sprite_list("wall_list", use_spatial_hash=True)
    for layer, sprite_list in game_map.map_layers.items():
        if "_blocking" in layer:
            game_map.scene.remove_sprite_list_by_object(sprite_list)

            game_map.scene["wall_list"].extend(sprite_list)

    return game_map


def load_maps():
    """
    Load all the Tiled maps from a directory.
    (Must use the .json extension.)
    """

    # Directory to pull maps from
    mypath = "resources/maps"

    if load_maps.map_file_names is None:

        # Dictionary to hold all our maps
        load_maps.map_list = {}

        # Pull names of all json files in that path
        load_maps.map_file_names = [
            f[:-5]
            for f in os.listdir(mypath)
            if isfile(join(mypath, f)) and f.endswith(".json")
        ]
        load_maps.map_file_names.sort()
        load_maps.file_count = len(load_maps.map_file_names)

    # Loop and load each file
    map_name = load_maps.map_file_names.pop(0)
    load_maps.map_list[map_name] = load_map(f"resources/maps/{map_name}.json")

    files_left = load_maps.file_count - len(load_maps.map_file_names)
    progress = 100 * files_left / load_maps.file_count

    done = len(load_maps.map_file_names) == 0
    return done, progress, load_maps.map_list


load_maps.map_file_names = None
load_maps.map_list = None
load_maps.file_count = None
