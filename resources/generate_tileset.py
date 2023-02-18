from PIL import Image
import json
from pathlib import Path

files = Path("resources/elizawy-lpc/Objects").glob("**/*.png")
for file in files:
    print(file.stem)

    tileset_file = file.parent / f"{file.stem}.tsj"

    im = Image.open(file)
    width, height = im.size

    columns = width / 32
    rows = height / 32
    tilecount = columns * rows

    data = {
        "columns": columns,
        "image": file.name,
        "imageheight": height,
        "imagewidth": width,
        "margin": 0,
        "name": file.stem,
        "spacing": 0,
        "tilecount": tilecount,
        "tiledversion": "1.9.2",
        "tileheight": 32,
        "tilewidth": 32,
        "type": "tileset",
        "version": "1.9"
    }

    with open(tileset_file, "w") as outfile:
        json.dump(data, outfile)

