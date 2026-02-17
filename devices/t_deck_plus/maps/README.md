# T-Deck Plus — Maps

Map datasets for the T-Deck live here. **Immutable:** do not delete, compress, reorganize, deduplicate, or convert formats without explicit approval. Datasets may exceed 100 GB.

## Layout

```
maps/
└── osm_tiles/   # OSM / generated tiles (e.g. from tdeck-maps)
```

## Map tile generator

Use [JustDr00py/tdeck-maps](https://github.com/JustDr00py/tdeck-maps) to generate Meshtastic map tiles for the T-Deck. Place output in `osm_tiles/` or as documented by that repo.
