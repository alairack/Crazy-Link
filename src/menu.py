import cocos.director
from cocos.sprite import Sprite
from cocos.scene import Scene
from cocos.menu import *
from cocos.text import Label
from cocos.actions import *
from pyglet.app import exit
from cocos.layer import ColorLayer, Layer
from game_scene import create_game_scene, setting
from settings import Logs
from pyglet import resource


def create_menu():
    menu_scene = Scene()
    menu_scene.add(MainMenu(), z=2)
    menu_scene.add(BackgroundLayer(), z=-1)
    menu_scene.add(SpriteLayer(), z=1)
    menu_scene.add(TitleLayer(), z=3)
    menu_scene.add(SpriteLayer1(), z=4)
    return menu_scene


class MainMenu(Menu):

    def __init__(self):
        super().__init__()
        self.position = (0, -100)

        self.font_title['font_size'] = 58
        self.font_title['color'] = (65, 105, 225, 255)
        self.font_title['bold'] = True

        self.font_item['font_size'] = 45
        self.font_item['bold'] = True
        self.font_item['color'] = (128, 128, 128, 255)

        self.font_item_selected['font_size'] = 50
        self.font_item_selected['color'] = (255, 193, 37, 255)

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


class BackgroundLayer(ColorLayer):
    def __init__(self):
        super().__init__(190, 190, 190, 255)


class SpriteLayer(Layer):
    def __init__(self):
        super().__init__()

        self.sprite_list = []
        for fruit in setting.fruit_images[:-1]:
            sprite = Sprite(fruit)
            self.add(sprite)
            self.sprite_list.append(sprite)
        self.do(Repeat(CallFunc(self.start_event) + Delay(9.8)))

    def start_event(self):
        self.sprite_list[0].position = (400, 150)
        self.sprite_list[0].do(FadeIn(2))

        self.sprite_list[1].position = (325, 500)
        self.sprite_list[1].do((MoveTo((325, 265), 3)) + JumpTo((208, 119), 200, 5, 5))

        self.sprite_list[2].position = (354, 600)
        self.sprite_list[2].do(MoveTo((354, 265), 3) | (RotateBy(360, 1)) * 3)

        self.sprite_list[3].position = (500, 600)
        self.sprite_list[3].do(MoveTo((500, 120), 3) | RotateBy(360, 1) * 3)

        self.sprite_list[4].position = (0, 236)
        self.sprite_list[4].do(MoveTo((600, 236), 4) | (ScaleTo(3, 2) + Reverse(ScaleBy(3, 2))))

        self.sprite_list[5].position = (150, 0)
        self.sprite_list[5].do(MoveTo((150, 380), 3) | (RotateBy(360, 1)) * 3 | (ScaleTo(3, 2) + Reverse(ScaleBy(3, 2))))

        self.sprite_list[6].position = (30, 500)
        self.sprite_list[6].do(JumpTo((30, 90), 200, 5, 5) + Blink(4, 3))

        self.sprite_list[7].position = (-20, 300)
        self.sprite_list[7].do(MoveTo((700, 400), 4) | (RotateBy(360, 1) * 3))

        self.sprite_list[8].position = (-20, 100)
        self.sprite_list[8].do(MoveTo((700, 100), 5) | Blink(11, 5))

        self.sprite_list[9].position = (700, 200)
        self.sprite_list[9].do(MoveTo((40, 200), 5))

        self.sprite_list[11].position = (400, 500)
        self.sprite_list[11].do(JumpTo((500, 100), 150, 9, 9))

        def sprite10_sport():
            self.sprite_list[10].position = (80, 600)
            self.sprite_list[10].do(MoveTo((88, -50), 3))

        def sprite10_stop():
            """
            给callfunc函数调用，清除掉sprite10的运动状态，防止出错
            :return:None
            """
            self.sprite_list[10].stop()

        self.sprite_list[10].do(Repeat(CallFunc(sprite10_sport) + Delay(3)))
        self.do(Delay(7) + FadeOutBLTiles(grid=(16, 12), duration=3) + StopGrid() + CallFunc(sprite10_stop))


class SpriteLayer1(Layer):
    def __init__(self):
        super().__init__()
        self.eye_durian = Sprite(resource.image("res/durian_eye.png"))
        self.add(self.eye_durian)
        self.eye_durian.position = (600, 236)
        self.eye_durian.rotation = -20
        self.eye_durian.visible = False
        self.eye_durian.do(Delay(4.6) + Repeat(CallFunc(self.eye_durian_sport) + Delay(19) + JumpTo((600, 236), 200, 5, 4) + Delay(2)))

    def eye_durian_sport(self):
        self.eye_durian.visible = True
        self.eye_durian.do(MoveTo((578, 236), 1) + RotateTo(0, 1) + Delay(2) + MoveTo((600, 236), 1) + Delay(0.6) + CallFunc(self.eye_durian_change_position, (250, -16)))
        self.eye_durian.do(Delay(6) + MoveTo((250, 8), 1) + Delay(3) + MoveTo((250, -16), 1) + Delay(0.8) + CallFunc(self.eye_durian_change_position, (-15, 240)))
        self.eye_durian.do(Delay(13) + RotateTo(98, 1) + Delay(0.8) + MoveTo((5, 240), 1) + Delay(1.6) + MoveTo((-15, 240), 1))

    def eye_durian_change_position(self, position):
        self.eye_durian.position = position


class TitleLayer(Layer):
    def __init__(self):
        super().__init__()
        self.title_1 = self.create_title("Crazy", "Pc Senior", 50, (210, 380))
        self.title_2 = self.create_title("Link", "Cyberpunk", 68, (400, 310))

    def create_title(self, text, font_name, size, position):
        title = Label(text,
                      font_name=font_name,
                      font_size=size,
                      color=(255, 64, 64, 255),
                      anchor_x="center",
                      anchor_y="center")

        title.position = position
        title.bold = True
        self.add(title)
        return title
