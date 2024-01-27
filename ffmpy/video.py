from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import cv2
import numpy as np
from tqdm import tqdm

from .exceptions import *
from .name import FramenoNamer


def load_video(fp: Path) -> cv2.VideoCapture:
    if not fp.exists():
        raise FileNotFoundError
    return cv2.VideoCapture(fp.as_posix())


def iter_frames(
    vc: cv2.VideoCapture,
    sec_from: float | None,
    sec_to: float | None,
) -> Iterator[tuple[int, np.ndarray]]:
    if not vc.isOpened():
        raise VideoOpenError

    fps = vc.get(cv2.CAP_PROP_FPS)
    fn_max = int(vc.get(cv2.CAP_PROP_FRAME_COUNT))

    if sec_from is not None:
        fn_from = int(np.floor(fps * sec_from))
        if fn_from > fn_max:
            raise VideoTimeError
        vc.set(cv2.CAP_PROP_POS_FRAMES, fn_from)
    else:
        fn_from = 0

    if sec_to is not None:
        fn_to = min(int(np.ceil(fps * sec_to)), fn_max)
    else:
        fn_to = fn_max

    for fn in tqdm(range(fn_from, fn_to)):
        success, frame = vc.read()
        if not success:
            raise VideoReadError
        yield fn, frame
    return


def save_frame(frame: np.ndarray, fp: Path) -> None:
    success = cv2.imwrite(fp.as_posix(), frame)
    if not success:
        raise FrameWriteError


def extract(
    fp: Path,
    sec_from: float | None,
    sec_to: float | None,
    overwrite: bool = False,
    parent_dir: Path | None = None,
) -> None:
    if parent_dir is None:
        folder = fp.parent / fp.stem
    else:
        folder = parent_dir / fp.stem

    if folder.exists() and not overwrite:
        raise PathExistsError

    folder.mkdir(parents=True, exist_ok=True)

    video = load_video(fp=fp)
    namer = FramenoNamer(vc=video)

    for fn, frame in iter_frames(vc=video, sec_from=sec_from, sec_to=sec_to):
        stem = namer.get(n=fn)
        sp = (folder / stem).with_suffix(".jpg")
        save_frame(frame, sp)
