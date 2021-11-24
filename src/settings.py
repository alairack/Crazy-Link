import pyglet.resource
import os
from cocos.director import director


class Settings:
    def __init__(self):
        self.level = 0
        self.level_info = [{"level": 1, "time": 160, "row": 10, "column": 15},
                           {"level": 2, "time": 200, "row": 11, "column": 16},
                           {"level": 3, "time": 240, "row": 12, "column": 17},
                           {"level": 4, "time": 280, "row": 13, "column": 18},
                           {"level": 5, "time": 300, "row": 14, "column": 19},
                           {"level": 6, "time": 340, "row": 15, "column": 20},
                           {"level": 7, "time": 360, "row": 16, "column": 20},
                           {"level": 8, "time": 380, "row": 17, "column": 21},
                           {"level": 9, "time": 410, "row": 18, "column": 22}]
        self.fruits = ["ananas", 'apple', 'banana', 'cherry', 'durian', 'grape', 'lemon', 'mangosteen', 'orange',
                       'pear', 'strawberry', 'watermelon', 'bird']
        self.square_size = 35      # 贴图大小
        self.click_anime = pyglet.resource.animation("res/click2.gif")
        self.click_sound = pyglet.resource.media("res/click.wav", streaming=False)
        self.un_click_sound = pyglet.resource.media("res/unclick.wav", streaming=False)
        self.remove_sound = pyglet.resource.media("res/remove_block.wav", streaming=False)
        self.logo = pyglet.resource.image("res/logo.ico")
        self.reset_button_image = pyglet.resource.image("res/reset.png")
        self.progress_bar_image = pyglet.resource.animation('res/progress.gif')
        self.pause_button_image = pyglet.resource.image("res/pause_button.png")
        self.resume_button_image = pyglet.resource.image("res/resume_button.png")
        self.load_fonts()
        self.fruit_images = []
        self.menu_scene = None
        for x in self.fruits:
            image = pyglet.resource.image(f"res/new_fruit/{x}.png")
            self.fruit_images.append(image)

    def create_new_window(self, scene):
        window_location = director.window.get_location()
        director.window.close()
        director.init(caption="Crazy Link",
                      width=self.level_info[self.level]["column"] * (self.square_size + 2) + 30,
                      height=self.level_info[self.level]["row"] * (self.square_size + 2) + 65,
                      resizable=True)
        director.window.set_location(window_location[0], window_location[1])
        director.window.set_icon(self.logo)
        director.run(scene)

    def load_fonts(self):
        pyglet.resource.path.append('res/fonts')
        pyglet.resource.reindex()
        pyglet.resource.add_font('GenJyuuGothic-Normal-2.ttf')
        pyglet.resource.add_font('pcsenior.ttf')
        pyglet.resource.add_font("Cyberpunk-Regular.ttf")


class Logs(object):
    def __init__(self):
        self.log_file = None
        self.open_log_file()

    def open_log_file(self):
        log_path = "./logs"
        if not os.path.exists(log_path):
            os.mkdir(os.getcwd() + r"\logs")
        log_file = open(f"{log_path}/game_logs.txt", "a")
        self.log_file = log_file
