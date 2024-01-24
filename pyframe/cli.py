from __future__ import annotations

from pathlib import Path

import click

from .exceptions import *
from .frame import extract


@click.command()
@click.argument("videopath", type=str)
@click.option(
    "--force",
    "-f",
    is_flag=True,
    help="Force overwrite.",
)
@click.option(
    "--sec-from",
    "sec_from",
    type=float,
    help="Seconds of the first frame.",
)
@click.option(
    "--sec-to",
    "sec_to",
    type=float,
    help="Seconds of the last frame.",
)
def cli(
    videopath: str,
    force: bool = False,
    sec_from: float | None = None,
    sec_to: float | None = None,
) -> None:
    try:
        extract(
            fp=Path(videopath),
            sec_from=sec_from,
            sec_to=sec_to,
            overwrite=force,
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
    click.echo("Done.")


def main() -> None:
    cli()
