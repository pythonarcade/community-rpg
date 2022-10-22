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
* [Kenney Input Prompts Pixel 16x16](https://kenney.nl/assets/input-prompts-pixel-16)

## Gameplay

The game is in extremely early stages. For discussion on future direction, see:
* [the github discussion board](https://github.com/pythonarcade/community-rpg/discussions).
* [the #community-ideas channel on Arcade's discord server](https://discord.com/channels/458662222697070613/704736572603629589)

### Controls
- **Movement:** Arrow Keys / WASD
- **Toggle Light/Torch:** L
- **Pick Up Items:** E
- **Open Inventory:** I *(This screen doesn't do anything yet)*
- **Select Current Item in Hotbar:** 1-0 *(Number keys)*
- **Open Menu:** ESC

## Installation

If you already have a compatible version of Python and poetry installed, you can get started right away.

The recommended installation is with `asdf` on Linux, Mac, and Windows (through WSL). For Windows native, see the recommended solutions further below

### Mac, Linux, and Windows-Subsystem-for-Llinux (WSL)

`asdf` is a general purpose version manager and we use it to ensure consistency between setups. To install `asdf`, follow the [installation guide](https://asdf-vm.com/guide/getting-started.html)

Once you have installed `asdf`, there are a few additional steps

```sh
asdf plugin-add python https://github.com/asdf-community/asdf-python.git
asdf plugin-add poetry https://github.com/asdf-community/asdf-poetry.git

# Make sure you are within the project directory and then run:
cd community-rpg
asdf install

# Then install the project to check that setup worked
poetry install
```

### Windows Native

1. There are multiple ways to install Python on Windows if you don't have it already. Our recommend approach is to install Chocolatey and run `choco install python` ([link](https://community.chocolatey.org/packages/python)). See the [guide for installing and configuring chocolatey here](https://chocolatey.org/install).
1. Next, install `poetry` following the [official poetry installation guide](https://python-poetry.org/docs/#installing-with-the-official-installer). We recommend using `pipx` ([pipx guide](https://pypa.github.io/pipx/installation/)), but installing method with powershell is the fastest way to get started.
1. To test that installation succeeded, run `poetry install` in the game directory before proceeding.

## Game Play

### Quick Start

Let's launch the game UI and make the first code changes! 

```sh
> poetry shell
(shell) doit play

# # FYI: this is the proposed way to interact, you can't currently use doit, so run for now:
# poetry run python -m rpg
````

This will open the game window where you can walk around using the keys `W`, `A`, `S`, and `D`

To make the first code change, try editing the file in **TBD/TBD/TBD.py** and changing the **TBD** to **TBD**

Note: you may have seen it above, but we will use the convention of `>` to indicate a normal shell prompt and `(shell)` to indicate when the command must be run after running `poetry shell` at least once. Alternatively, you could use `poetry run doit play`, but using `poetry shell` first is more convenient

```sh
doit play
```

Great, you've made your first code change!

Now the first task code is very limited and needs your help to refactor and extend it, but first lets take a look at the baseline functionality:

```sh
# Run all of the default tasks
(shell) doit --continue
# Tasks can also be run one-by-one
(shell) doit inspect
# Or you can use a watcher utility that will re-run on changes
(shell) doit watch_changes
```

**TBD** ... (These docs are WIP and a proposed way to interact, but heve not yet been implemented!)

(TODO: how to switch tasks? Maybe `doit start task2`? Maybe this would pull the necessary sample code and README? Then the full test suite would be run against all pulled tasks?)
