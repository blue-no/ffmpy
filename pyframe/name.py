import cv2


class FramenoNamer:
    def __init__(self, vc: cv2.VideoCapture) -> None:
        self._ndigits = len(str(int(vc.get(cv2.CAP_PROP_FRAME_COUNT))))

    def get(self, n: int) -> str:
        return f"{n:0>{self._ndigits}}"
