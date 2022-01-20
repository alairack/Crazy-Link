from cocos.director import director
from cocos.layer import Layer
from cocos.actions import Blink, Show, FadeIn, ScaleTo
from cocos.text import Label
from pyglet.window import key
from settings import setting


class WinLayer(Layer):
    is_event_handler = True

    def __init__(self):
        super().__init__()
        action = ScaleTo(2, 1.5) + Blink(10, 2) + Show()
        width, height = director.get_window_size()

        msg1 = self.create_text("恭喜！\n您通关了", 34, width // 2, height // 2)
        msg1.do(action)

        msg2 = self.create_text("press Enter back to menu", 32, width//2, height // 2 - 110)
        msg2.opacity = 0
        msg2.do(FadeIn(2))

    def create_text(self, msg, size, x, y):
        text = Label(msg,
                     font_name="Kristen ITC",
                     font_size=size,
                     color=(255, 64, 64, 255),
                     anchor_x="center",
                     anchor_y="center")

        text.position = (x, y)
        self.add(text)
        return text

    def on_key_press(self, k, _):
        if k == key.ENTER:
            setting.run(window_location=director.window.get_location(), exist_window=True)
