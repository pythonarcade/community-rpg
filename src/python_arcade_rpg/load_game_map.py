"""
Load maps
"""
from collections import OrderedDict
import os
from os.path import isfile, join

import arcade
from constants import TILE_SCALING


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

    layer_options = {
        'trees_blocking': {
            "use_spatial_hash": True,
        },
        'misc_blocking': {
            "use_spatial_hash": True,
        },
        'bridges': {
            "use_spatial_hash": True,
        },
        'water_blocking': {
            "use_spatial_hash": True,
        },
    }

    # Read in the tiled map
    print(f"Loading map: {map_name}")
    my_map = arcade.tilemap.load_tilemap(map_name, scaling=TILE_SCALING, layer_options=layer_options)

    game_map.map_layers = my_map.sprite_lists

    game_map.map_size = my_map.width, my_map.height
    game_map.background_color = my_map.background_color

    # Any layer with '_blocking' in it, will be a wall
    for layer in game_map.map_layers:
        if '_blocking' in layer:
            game_map.wall_list.extend(game_map.map_layers[layer])

    return game_map


def load_maps():

    # Directory to pull maps from
    mypath = "maps"

    if load_maps.map_file_names is None:

        # Dictionary to hold all our maps
        load_maps.map_list = {}

        # Pull names of all json files in that path
        load_maps.map_file_names = \
            [f[:-5] for f in os.listdir(mypath) if isfile(join(mypath, f)) and f.endswith(".json")]
        load_maps.map_file_names.sort()
        load_maps.file_count = len(load_maps.map_file_names)

    # Loop and load each file
    map_name = load_maps.map_file_names.pop(0)
    load_maps.map_list[map_name] = load_map(f"maps/{map_name}.json")

    files_left = load_maps.file_count - len(load_maps.map_file_names)
    progress = 100 * files_left / load_maps.file_count

    done = len(load_maps.map_file_names) == 0
    return done, progress, load_maps.map_list


load_maps.map_file_names = None
load_maps.map_list = None
load_maps.file_count = None
