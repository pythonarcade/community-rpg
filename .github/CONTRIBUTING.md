# Contributing to the Python Arcade Community RPG

## Suggesting Improvements or Reporting Bugs

Open up issues:

https://github.com/pythonarcade/community-rpg/issues

## Fix Bugs or Implement Features

Before contributing code, please open an issue for what you are coding if one does not already exist,
and then check in code with that issue number (like "issue #146") as part of the commit message.

All code being contributed should be formatted with the [black](https://github.com/psf/black) and [isort](https://pycqa.github.io/isort/index.html) auto-formatters. As well as linted with [flake8](https://flake8.pycqa.org/en/latest/). These tools will be installed as part of the dev dependencies of the library when installing with:

```bash
pip install -e ".[dev]"
```

## Improve the Documentation

At present there is not stand-alone documentation for this project, while this is subject to change, documentation currently exists only in code comments. Any documentation improvements should follow the same guidelines as bug fixes or feature implementations

## Test and provide Feedback

The more people who can test the game, and on different hardware, the better! If you've played the game and had problems with it, please raise an issue as outlined above including your operating system and hardware details.
