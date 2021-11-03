import pyglet.resource
import os


class Settings:
    def __init__(self):
        self.level = 0
        self.level_info = [{"level": 1, "time": 100, "row": 10, "column": 15},
                           {"level": 2, "time": 120, "row": 11, "column": 16},
                           {"level": 3, "time": 140, "row": 12, "column": 17},
                           {"level": 4, "time": 160, "row": 13, "column": 18},
                           {"level": 5, "time": 180, "row": 14, "column": 19},
                           {"level": 6, "time": 200, "row": 15, "column": 20},
                           {"level": 7, "time": 220, "row": 16, "column": 20},
                           {"level": 8, "time": 240, "row": 17, "column": 21},
                           {"level": 9, "time": 260, "row": 18, "column": 22}]
        self.fruits = ["ananas", 'apple', 'banana', 'cherry', 'durian', 'grape', 'lemon', 'mangosteen', 'origin',
                       'pear', 'strawberry', 'watermelon']
        self.square_size = 32      # 贴图大小
        self.click_anime = pyglet.resource.animation("res/click2.gif")
        self.click_sound = pyglet.resource.media("res/click.wav", streaming=False)
        self.un_click_sound = pyglet.resource.media("res/unclick.wav", streaming=False)
        self.remove_sound = pyglet.resource.media("res/remove_block.wav", streaming=False)
        self.fruit_images = []
        self.menu_scene = None
        for x in self.fruits:
            image = pyglet.resource.image(f"res/fruit/{x}.png")
            self.fruit_images.append(image)


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
