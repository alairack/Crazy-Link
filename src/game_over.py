from cocos.director import director
from cocos.layer import Layer
from cocos.actions import MoveTo, FadeIn
from cocos.text import Label
from pyglet.window import key


class GameOverLayer(Layer):
    is_event_handler = True

    def __init__(self, setting):
        super().__init__()
        width, height = director.get_window_size()

        msg1 = self.create_text("Game Over", 54, width // 2, height)
        self.setting = setting
        msg1.do(MoveTo((width//2, height//2), 1))

        msg2 = self.create_text("press Enter back to menu", 30, width//2, height//2 - 66)
        msg2.do(FadeIn(2))

    def create_text(self, msg, size, x, y):
        text = Label(msg,
                     font_name="Kristen ITC",
                     font_size=size,
                     color=(0, 0, 255, 255),
                     anchor_x="center",
                     anchor_y="bottom")

        text.position = (x, y)
        self.add(text)
        return text

    def on_key_press(self, k, _):
        if k == key.ENTER:
            self.setting.create_new_window(self.setting.menu_scene)
