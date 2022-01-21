import pyglet.resource
from cocos.director import director
from cocos.particle_systems import Explosion
import logging
from pyglet.gl import *
import sys

logger = logging.getLogger("main.setting")


class Settings:
    def __init__(self):
        self.level = 0
        self.level_info = [{"level": 1, "time": 250, "row": 10, "column": 15},
                           {"level": 2, "time": 310, "row": 11, "column": 16},
                           {"level": 3, "time": 370, "row": 12, "column": 17},
                           {"level": 4, "time": 430, "row": 13, "column": 18},
                           {"level": 5, "time": 490, "row": 14, "column": 19},
                           {"level": 6, "time": 550, "row": 15, "column": 20},
                           {"level": 7, "time": 610, "row": 16, "column": 20},
                           {"level": 8, "time": 670, "row": 17, "column": 21},
                           {"level": 9, "time": 730, "row": 18, "column": 22}]
        self.fruits = ["ananas", 'apple', 'banana', 'cherry', 'durian', 'grape', 'lemon', 'mangosteen', 'orange',
                       'pear', 'strawberry', 'watermelon', 'bird', 'kiwi']
        self.square_size = 40      # 贴图大小
        self.click_anime = pyglet.resource.animation("res/click.gif")
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
        self.create_menu_method = None
        for x in self.fruits:
            image = pyglet.resource.image(f"res/test/{x}.png")
            image.width = self.square_size
            image.height = self.square_size
            self.fruit_images.append(image)

        """
            启用mipmap和材质:
            image = pyglet.image.load(f"res/test/{x}.png")
            texture = image.get_mipmapped_texture()
            glBindTexture(GL_TEXTURE_2D, texture.id)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
            texture.width = 40
            texture.height = 40
            self.fruit_images.append(texture)
        """

    def load_fonts(self):
        pyglet.resource.path.append('res/fonts')
        pyglet.resource.reindex()
        pyglet.resource.add_font('Lato-Regular.ttf')
        pyglet.resource.add_font('GenJyuuGothic-Normal-2.ttf')
        pyglet.resource.add_font('pcsenior.ttf')
        pyglet.resource.add_font("Cyberpunk-Regular.ttf")

    def run(self, window_location=None, exist_window=False, scene=None):
        if display_setting.select_value["msaa"] != 0:
            config = pyglet.gl.Config(sample_buffers=1,
                       samples=int(display_setting.config_dict["msaa"][display_setting.select_value["msaa"]].replace("X", "")))  # 去除字符串中的X
        else:
            config = None
        if exist_window:
            director.window.close()
        def run_game():
            director.init(caption="Crazy Link", style=pyglet.window.Window.WINDOW_STYLE_DEFAULT,
                          width=setting.level_info[setting.level]["column"] * (setting.square_size + 2) + 30,
                          height=setting.level_info[setting.level]["row"] * (setting.square_size + 2) + 65,
                          resizable=True,
                          vsync=display_setting.select_value["vsync"], config=config, fullscreen=display_setting.select_value["fullscreen"])

            if window_location is not None:
                director.window.set_location(window_location[0], window_location[1])
            logger.info(f"game start on {sys.platform}")
            logger.info(f"audio driver : {pyglet.media.get_audio_driver()}")  # 此代码理论上仅打印声音驱动名称，但可以使初次播放声音速度明显提升

            director.window.set_icon(setting.logo)
            director.show_FPS = display_setting.select_value["show_fps"]
            if scene is None:
                menu_scene = self.create_menu_method()
                director.run(menu_scene)
            else:
                director.run(scene)

        try:
            run_game()
        except Exception:
            logger.error("game is failed", exc_info=True)


class DisplaySetting(object):
    def __init__(self):
        self.current_window_location = None
        self.init_select_value()
        self.config_dict = {"msaa": ['disable', '2X', '4X', '8X', '16X'], "vsync": ['disable', 'enable'],
                            "show_fps": ['disable', 'enable'], "fullscreen": ['disable', 'enable'],
                            "particle": ["disable", 'enable']}
        self.config_path = "./crazy_link/config.inf"
        self.get_config()

    def init_select_value(self):
        self.select_value = {}
        self.select_value["msaa"] = 4
        self.select_value["vsync"] = 1
        self.select_value["show_fps"] = 0
        self.select_value["fullscreen"] = 0
        self.select_value["particle"] = 1

    def get_config(self):

        def get_config_file():
            """
            此方法必须置于 main.init_log 方法后
            :return:config文件指针
            """

            try:
                file = open(self.config_path, "r")
            except FileNotFoundError:
                file = self.export_config("w+")
            return file

        self.config_file = get_config_file()
        file_content = self.config_file.read()
        file_content = file_content.replace(" ", '')    # 去掉空格
        self.config_file.close()
        for line in file_content.splitlines():
            x = line.split(":")
            key = x[0]
            value = x[1]
            self.select_value[key] = self.config_dict[key].index(value)

    def export_config(self, mode):
        f = open(self.config_path, mode)
        for key, value in self.config_dict.items():
            f.write(f"{key}:{value[self.select_value[key]]}\n")
        return f


class GameParticle(Explosion):
    duration = 2
    angle = 0.0
    blend_additive = True
    size = 3.0


setting = Settings()
display_setting = DisplaySetting()