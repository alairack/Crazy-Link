from cocos.layer import Layer
from cocos.text import Label
from game_over import GameOverLayer
from cocos.scene import Scene


class HUDLayer(Layer):
    def __init__(self, setting):
        super().__init__()
        self.setting = setting
        self.position = (0, (setting.level_info[setting.level]["row"]) * (setting.square_size+2))
        self.time = self.setting.level_info[setting.level]["time"]
        self.remain_time = self.create_text(80, 5)
        self.count_time()

    def create_text(self, x, y):
        text = Label("",
                     font_size=10,
                     color=(255, 99, 71, 255),
                     anchor_x="left",
                     anchor_y="bottom",
                     dpi=180)

        text.position = (x, y)
        self.add(text)
        return text

    def count_time(self):
        def update_time(dt):
            self.time = self.time - 1
            if self.time <= 0:
                game_over_layer = GameOverLayer(self.setting)
                current_scene = self.get_ancestor(Scene)
                layer = current_scene.get_children()[0]
                layer.disable_input()
                self.setting.level = 0
                current_scene.add(game_over_layer, z=2)
                self.unschedule(update_time)

        self.schedule_interval(update_time, 1)

    def draw(self):
        self.remain_time.element.text = "剩余时间: " + str(self.time)