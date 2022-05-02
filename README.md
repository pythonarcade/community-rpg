# Welcome to The Python Arcade Community RPG

![Pull Requests Welcome](https://img.shields.io/badge/PRs-welcome-success)
![First Timer Friendly](https://img.shields.io/badge/First%20Timer-friendly-informational)
![License MIT](https://img.shields.io/badge/license-MIT-success)

![Screenshot](/screenshot.png)

This is an open-source RPG game.

* Everything is open-source, under the permissive MIT license.
* Libraries Used:
  * [Arcade](https://github.com/pythonarcade/arcade)
  * [Pyglet](https://github.com/pyglet/pyglet)
  * [pytiled_parser](https://github.com/pythonarcade/pytiled_parser)
* Maps are created with the [Tiled Map Editor](https://mapeditor.org)
* All code is written in Python

Graphics Assets From:

* [Pipoya Free RPG Tileset 32x32](https://pipoya.itch.io/pipoya-rpg-tileset-32x32)
* [Pipoya Free RPG Character Sprites 32x32](https://pipoya.itch.io/pipoya-free-rpg-character-sprites-32x32)

## Gameplay

The game is in extremely early stages. For discussion on future direction, see: #31

### Controls
**Arrow Keys / WASD**: Movement
**L**: Toggle Light/Torch
**E**: Pick Up Items
**I**: Open Inventory (non-functional)
**1-0 (number keys)**: Select Item in Hotbar
**ESC**: Open Menu

## Development

This project targets Python 3.7 or greater.

To install the project and all development dependencies run the following command, this should ideally be done in a [virtual environment](https://docs.python.org/3/tutorial/venv.html):

```bash
pip install -e ".[dev]"
```

The game can then be ran with:

```bash
python -m rpg
```

## Contact The Maintainer

paul@cravenfamily.com
