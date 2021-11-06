import cocos.director
import pyglet.resource
from cocos.scene import Scene
from cocos.menu import *
from pyglet.app import exit
from pyglet.gl import *
from cocos.layer import Layer
from game_scene import create_game_scene, setting
from settings import Logs


class MainMenu(Menu):
    def __init__(self):
        super().__init__('Crazy Link')

        self.font_title['font_size'] = 58
        self.font_title['color'] = (65, 105, 225, 255)
        self.font_title['bold'] = True

        self.font_item['font_size'] = 38
        self.font_item['bold'] = True
        self.font_item['color'] = (128, 128, 128, 255)

        self.font_item_selected['font_size'] = 28
        self.font_item_selected['color'] = (0, 0, 0, 255)

        items = []
        items.append(MenuItem('play', self.on_play))
        items.append(MenuItem('QUit', self.on_quit))

        self.create_menu(items, zoom_in(), zoom_out())

    def on_play(self):
        game_scene = create_game_scene()
        setting.menu_scene = create_menu()
        cocos.director.director.replace(game_scene)

    def on_quit(self):
        Logs().log_file.close()
        exit()


class BackgroundLayer(Layer):
    def __init__(self):
        super().__init__()
        self.background_image = pyglet.resource.image("res/menu.jpeg")

    def draw(self):
        glPushMatrix()
        self.transform()
        self.background_image.blit(0, 0)
        glPopMatrix()


def create_menu():
    menu_scene = Scene()
    menu_scene.add(MainMenu(), z=1)
    menu_scene.add(BackgroundLayer(), z=0)
    return menu_scene
