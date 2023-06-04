from typing import TYPE_CHECKING

from cmu_graphics import *

if TYPE_CHECKING:
    from cmu_types import Label


class Button:
    """
    example

    def button_callback():
        print('pressed')

    Button(Rect(0, 0, 100, 100, fill='blue'), Label('click me', 50, 50), button_callback)
    """

    buttons = set()

    def __init__(self, text, rect, callback):
        self.rect = rect
        self.label = Label(
            text, rect.left + rect.width / 2, rect.top + rect.height / 2, size=25
        )
        self.callback = callback
        self.buttons.add(self)

    @classmethod
    def process(cls, x, y):
        for button in cls.buttons:
            if button.rect.hits(x, y):
                button.callback()
