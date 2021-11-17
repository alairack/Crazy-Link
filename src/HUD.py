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
        self.remain_time = self.setting.level_info[setting.level]["time"]           # 剩余时间
        self.level_time = self.setting.level_info[setting.level]["time"]            # 关卡设定时间
        self.remain_time_text = self.create_text(0, 5, 9)
        self.remain_reset_text = self.create_text(445, 5, 9)
        self.remain_reset_time = 3
        self.reset_button = self.create_reset_button()
        self.progress_bar = self.create_progress_bar()
        self.count_time()
        self.current_scene = scene
        self.scene_position = self.current_scene.position

    def create_text(self, x, y, size):
        text = Label("",
                     font_name="Gen Jyuu Gothic Normal",
                     font_size=size,
                     color=(255, 99, 71, 255),
                     anchor_x="left",
                     anchor_y="bottom",
                     bold=True,
                     dpi=180)

        text.position = (x, y)
        self.add(text)
        return text

    def create_reset_button(self):
        reset = Sprite(image=self.setting.reset_button_image)
        reset.position = (400, 20)
        reset.anchor = (0, 0)
        self.add(reset)
        return reset

    def count_time(self):
        """
        计算剩余时间，控制进度条与文本显示
        """
        def update_time(dt):
            self.remain_time = self.remain_time - 1
            if self.remain_time <= 0:
                game_over()

        def update_progress_bar(dt):
            self.progress_bar.scale_x = self.remain_time / self.level_time

        def game_over():
            game_over_layer = GameOverLayer(self.setting)
            layer = self.current_scene.get_children()[0]
            layer.disable_input()
            self.setting.level = 0
            self.current_scene.add(game_over_layer, z=2)
            self.unschedule(update_time)
            self.unschedule(update_progress_bar)
            self.progress_bar.scale_x = 0           # 避免进度条残留显示在屏幕上

        self.schedule_interval(update_time, 1)
        self.schedule_interval(update_progress_bar, 1)

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
        self.remain_time_text.element.text = "剩余时间: " + str(self.remain_time)
        self.remain_reset_text.element.text = "重置机会: " + str(self.remain_reset_time)

    def create_progress_bar(self):
        progress_bar = Sprite(image=self.setting.progress_bar_image)
        progress_bar.position = (255, 20)
        progress_bar.anchor = (-105, 20)
        self.add(progress_bar)
        return progress_bar
