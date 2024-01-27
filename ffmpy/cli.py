from __future__ import annotations

from pathlib import Path

import click

from . import video
from .exceptions import *


def timestr_to_sec(time_: str) -> float:
    ts = time_.split(":")
    sec = float(ts[-1])
    sec += 60 * int(ts[-2]) if len(ts) > 2 else 0
    sec += 3600 * int(ts[-3]) if len(ts) > 3 else 0
    return sec


@click.group()
def cli() -> None:
    pass


@cli.command()
@click.argument("videopath", type=str)
@click.option(
    "--force",
    "-f",
    is_flag=True,
    help="Force overwrite or not.",
)
@click.option(
    "--time-start",
    "-ts",
    "time_start",
    help="Time of the first frame (H:M:S).",
)
@click.option(
    "--time-end",
    "-te",
    "time_end",
    help="Time of the last frame (H:M:S).",
)
@click.option(
    "--duration",
    "-d",
    help="Time length (H:M:S).",
)
@click.option(
    "--save-dir",
    "-s",
    "save_dir",
    help="Directory where frames are saved.",
)
def extract(
    videopath: str,
    force: bool = False,
    time_start: str | None = None,
    time_end: str | None = None,
    duration: str | None = None,
    save_dir: str | None = None,
) -> None:
    if time_end is not None and duration is not None:
        raise click.BadOptionUsage(
            "duration",
            '"--time-end" and "--duration" cannot be specified at the same'
            " time.",
        )

    videopath = Path(videopath)
    if time_start is not None:
        time_start = timestr_to_sec(time_start)
    if time_end is not None:
        time_end = timestr_to_sec(time_end)
    elif duration is not None:
        time_end = timestr_to_sec(duration)
        if time_start is not None:
            time_end += time_start
    if save_dir is not None:
        save_dir = Path(save_dir)

    try:
        video.extract(
            fp=videopath,
            sec_from=time_start,
            sec_to=time_end,
            overwrite=force,
            parent_dir=save_dir,
        )
    except PathExistsError:
        raise click.BadParameter(
            'Save folder already exists. If you want to overwrite, use "-f"'
            " option"
        )
    except FileNotFoundError:
        raise click.BadParameter("Video does not exist.")
    except VideoOpenError:
        raise click.BadParameter("Cannot open video.")
    except VideoReadError:
        raise click.BadParameter("Cannot read video.")
    except FrameWriteError:
        raise click.BadParameter("Cannot save frames.")
    except VideoTimeError:
        raise click.BadParameter("Time is invalid.")
    click.echo("Done.")


@cli.command()
@click.argument("videopath", type=str)
def info(videopath: str) -> None:
    videopath = Path(videopath)
    try:
        d = video.info(fp=videopath)
    except FileNotFoundError:
        raise click.BadParameter("Video does not exist.")
    except VideoOpenError:
        raise click.BadParameter("Cannot open video.")

    click.echo(
        f"Codec\t\t: {int(d['codec']).to_bytes(4, 'little').decode('utf-8')}"
    )
    click.echo(f"FPS\t\t: {d['fps']}")
    click.echo(f"Frame Size\t: {int(d['width'])} x {int(d['height'])}")
    click.echo(f"Frame Count\t: {int(d['count'])}")


def main() -> None:
    cli()
