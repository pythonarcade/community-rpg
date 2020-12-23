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

def load_maps():
    # Dictionary to hold all our maps
    map_list = {}

    # Directory to pull maps from
    mypath = "maps"

    # Pull names of all tmx files in that path
    map_file_names = [f[:-4] for f in os.listdir(mypath) if isfile(join(mypath, f)) and f.endswith(".tmx")]

    # Loop and load each file
    for map_name in map_file_names:
        map_list[map_name] = load_map(f"maps/{map_name}.tmx")

    return map_list