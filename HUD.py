from cocos.layer import Layer
from cocos.text import Label
from game_over import GameOverLayer
from cocos.sprite import Sprite
from cocos.director import director


class HUDLayer(Layer):
    is_event_handler = True

    def __init__(self, setting, scene):
        super().__init__()
        self.setting = setting
        self.position = (0, (setting.level_info[setting.level]["row"]) * (setting.square_size+2))
        self.time = self.setting.level_info[setting.level]["time"]
        self.remain_time = self.create_text(80, 5, 10)
        self.remain_reset_text = self.create_text(380, 9, 7)
        self.remain_reset_time = 3
        self.reset_button = self.create_reset_button()
        self.count_time()
        self.current_scene = scene
        self.scene_position = self.current_scene.position

    def create_text(self, x, y, size):
        text = Label("",
                     font_name="SimSun",
                     font_size=size,
                     color=(255, 99, 71, 255),
                     anchor_x="left",
                     anchor_y="bottom",
                     dpi=180)

        text.position = (x, y)
        self.add(text)
        return text

    def create_reset_button(self):
        reset = Sprite(image=self.setting.reset_button_image, position=(80, 10))
        reset.position = (320, 20)
        reset.anchor = (0, 0)
        self.add(reset)
        return reset

    def count_time(self):
        def update_time(dt):
            self.time = self.time - 1
            if self.time <= 0:
                game_over_layer = GameOverLayer(self.setting)
                layer = self.current_scene.get_children()[0]
                layer.disable_input()
                self.setting.level = 0
                self.current_scene.add(game_over_layer, z=2)
                self.unschedule(update_time)

        self.schedule_interval(update_time, 1)

    def press_reset_button(self):
        if self.remain_reset_time-1 >= 0:
            game_layer = self.current_scene.get_children()[0]
            game_layer.reset()
            self.remain_reset_time = self.remain_reset_time - 1
        else:
            pass

    def on_mouse_press(self, x, y, dx, dy):
        current_window_size = director._get_window_size_no_autoscale()
        window_scale_x = current_window_size[0] / director.get_window_size()[0]
        window_scale_y = current_window_size[1] / director.get_window_size()[1]
        if x > (self.reset_button.x - self.reset_button.width/2 + self.scene_position[0]) * window_scale_x:          # 判断是否在按钮的边界值内
            if x < (self.reset_button.x + self.reset_button.width/2 + self.scene_position[0]) * window_scale_x:
                if y > (self.reset_button.y + self.reset_button.height/2 - self.scene_position[1] + self.position[1]) * window_scale_y:
                    if y < (self.reset_button.y + self.reset_button.height/2 + self.scene_position[1] + self.position[1]) * window_scale_y:
                        self.press_reset_button()

    def draw(self):
        self.remain_time.element.text = "剩余时间: " + str(self.time)
        self.remain_reset_text.element.text = "剩余重置次数: " + str(self.remain_reset_time)
