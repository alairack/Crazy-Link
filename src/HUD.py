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
        self.remain_time_text = self.create_text(0, 11, 9)
        self.remain_reset_text = self.create_text(450, 11, 9)
        self.remain_reset_time = 3
        self.reset_button = self.create_reset_button()
        self.pause_button = self.create_pause_button()
        self.progress_bar = self.create_progress_bar()
        self.count_time()
        self.current_scene = scene
        self.scene_position = self.current_scene.position
        self.game_layer = self.current_scene.get_children()[0]
        self.is_run = True

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
        reset.position = (425, 25)
        reset.anchor = (0, 0)
        self.add(reset)
        return reset

    def create_pause_button(self):
        pause_button = Sprite(image=self.setting.pause_button_image)
        pause_button.position = (380, 25)
        pause_button.anchor = (0, 0)
        self.add(pause_button)
        return pause_button

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
            self.game_layer.reset()
            self.remain_reset_time = self.remain_reset_time - 1
        else:
            pass

    def press_pause_button(self):
        task_list = self.scheduled_interval_calls
        self.unschedule(task_list[0][0])
        self.unschedule(task_list[1][0])
        self.game_layer.visible = False
        self.pause_button.image = self.setting.resume_button_image
        self.is_run = False

    def press_resume_button(self):
        self.count_time()
        self.game_layer.visible = True
        self.pause_button.image = self.setting.pause_button_image
        self.is_run = True

    def on_mouse_press(self, x, y, dx, dy):
        if self.is_in_button_area(x, y, self.reset_button):
            self.press_reset_button()
        if self.is_in_button_area(x, y, self.pause_button):
            if self.is_run:
                self.press_pause_button()
            else:
                self.press_resume_button()

    def draw(self):
        self.remain_time_text.element.text = "剩余时间: " + str(self.remain_time)
        self.remain_reset_text.element.text = "重置机会: " + str(self.remain_reset_time)

    def create_progress_bar(self):
        progress_bar = Sprite(image=self.setting.progress_bar_image)
        progress_bar.position = (255, 26)
        progress_bar.anchor = (-105, 20)
        self.add(progress_bar)
        return progress_bar

    def is_in_button_area(self, x, y, button):
        """
        判断是否点击在按钮上
        :x 点击时的x坐标
        :y 点击时的y坐标
        :button需要判断的按钮
        :return 返回判断结果
        """
        current_window_size = director._get_window_size_no_autoscale()
        window_scale_x = current_window_size[0] / director.get_window_size()[0]
        window_scale_y = current_window_size[1] / director.get_window_size()[1]
        if x > (button.x - button.width / 2 + self.scene_position[0]) * window_scale_x:
            if x < (button.x + button.width / 2 + self.scene_position[0]) * window_scale_x:
                if y > (button.y - button.height / 2 + self.scene_position[1] + self.position[1]) * window_scale_y:
                    if y < (button.y + button.height / 2 + self.scene_position[1] + self.position[1]) * window_scale_y:
                        return True
        return False

