import json
import os
import sys
from pathlib import Path

from PIL import Image

FILE = Path(sys.argv[1])


def main():
    assert FILE.is_file()

    tileset_FILE = FILE.parent / f"{FILE.stem}.tsj"

    im = Image.open(FILE)
    width, height = im.size

    columns = width / 32
    rows = height / 32
    tilecount = columns * rows

    data = {
        "columns": columns,
        "image": FILE.name,
        "imageheight": height,
        "imagewidth": width,
        "margin": 0,
        "name": FILE.stem,
        "spacing": 0,
        "tilecount": tilecount,
        "tiledversion": "1.9.2",
        "tileheight": 32,
        "tilewidth": 32,
        "type": "tileset",
        "version": "1.9"
    }

    with open(tileset_FILE, "w") as outfile:
        json.dump(data, outfile)

if __name__ == "__main__":
    main()
