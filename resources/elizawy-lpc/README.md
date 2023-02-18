# LPC Revised

https://github.com/ElizaWy/LPC

This is a rework of the Liberated Pixel Cup pixel art asset kit. LPC uses a bright 128 color palette and a 32x32 tile resolution. I aim to curate and add pieces to this set to expand it while remaining consistent in style and tone.

Licensing is OGA-by 3.0; OGA-BY is a license based on CC-BY 3.0 that removes that license's restriction on technical measures that prevent redistribution of a work. This, essentially, means this assets can be used in commercial games on platforms like iOS, so long as the source is credited.

New work will be added to this repository as I complete it, so anyone can come here to get the latest, most complete collection to date, with detailed credit files supplied. If this kit is missing an element anyone very much wants to see, I take suggestions and commisions at my Patreon: https://www.patreon.com/DeathsDarling

Happy gaming!

## Community RPG Spcific Changes

A number of changes have been made to this collection. In doing so, every effort has been made to maintain all credits.

### Spritesheet Packing

Many of the spritesheets have been packed into larger sheets to reduce the number of seperate tilesheets we had to deal with. The following is an example of a command that was used to do so:

```bash
convert *.png -append packed_$(basename $PWD).png
```

We should **not** remove any of the assets from the repo that have been packed into the larger sets, in case we need to make modifications later. The tilesets that have gone into the larger sets have been retained and assigned digits to help maintain their order, so in the future if modifications are done, we can re-assemble the larger sets without trouble.
