# so replit recgonizes objects from cmu_graphics
import random

randrange = random.randrange


class app:
    background: str


class cmu_graphics:
    def run():
        ...


class Rect:
    def __init__(
        self,
        left,
        top,
        width,
        height,
        fill="black",
        border=None,
        borderWidth=2,
        opacity=100,
        rotateAngle=0,
        dashes=False,
        align="left-top",
        visible=True,
    ):
        ...


class Label:
    def __init__(
        self,
        value,
        centerX,
        centerY,
        size=12,
        font="arial",
        bold=False,
        italic=False,
        fill="black",
        border=None,
        borderWidth=2,
        opacity=100,
        rotateAngle=0,
        align="center",
        visible=True,
    ):
        ...


class Image:
    health: int
    food: int

    def __init__(self, url, left, top):
        ...


class Group:
    def __init__(self, *args):
        ...


class Star:
    def __init__(
        centerX,
        centerY,
        radius,
        points,
        fill="black",
        border=None,
        borderWidth=2,
        roundness=None,
        opacity=100,
        rotateAngle=0,
        dashes=False,
        align="center",
        visible=True,
    ):
        ...


pythonRound = round
