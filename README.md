# FFmpy

## Usage

Extract all frames from a video:

```
python -m ffmpy extract "{path-to-video}"
```

Extract frames from a video for a specific second:

```
# specify end time
python -m ffmpy extract "{path-to-video}" -ts 3.50 -te 25.50

# specify duration time
python -m ffmpy extract "{path-to-video}" -ts 3.50 -d 22.0
```

If you want to overwrite existing frames, use `-f` or `--force` option.

Get video information:

```
python -m ffmpy info "{path-to-video}"
```
