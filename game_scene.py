import cocos.batch
from cocos.scene import Scene
from cocos.layer import ColorLayer
from cocos.batch import BatchNode
import random
from settings import Settings
import math
from cocos.director import director
from cocos.actions import *
from judge import *

setting = Settings()


def create_game_scene():
    scene = Scene()
    scene.add(GameBackgroundLayer(), z=1)
    return scene


class GameBackgroundLayer(ColorLayer):
    is_event_handler = True

    def __init__(self):
        super().__init__(0, 0, 0, 255)
        self.selected_block = []

        self.board = Board()
        self.batch = cocos.batch.BatchNode()
        self.batch.position = setting.square_size/2, setting.square_size/2          # 因为sprite 的position为中心点
        self.add(self.batch)
        self.width = setting.level_info[0]["column"] * setting.square_size + 40
        self.height = setting.level_info[0]["row"] * setting.square_size + 40
        self.board.draw(self.position, self.batch)
        self.click_anime = []

    def draw(self):
        super().draw()

    def on_mouse_press(self, x, y, dx, dy):
        current_window_size = director._get_window_size_no_autoscale()
        window_scale_x = current_window_size[0] / director.get_window_size()[0]
        window_scale_y = current_window_size[1] / director.get_window_size()[1]
        sprite_x = math.floor((x - self.position[0])/(setting.square_size + 2) / window_scale_x)     # 取整
        sprite_y = math.floor((y - self.position[1])/(setting.square_size + 2) / window_scale_y)
        try:
            click_sprite = self.batch.get(f"{sprite_y, sprite_x}")
        except Exception:
            pass
        else:
            if self.board.array[sprite_y][sprite_x] != 0:
                if len(self.selected_block) % 2 == 0:
                    click_sprite.click(self.click_anime)
                    self.selected_block.append([click_sprite, sprite_x, sprite_y])
                else:
                    if sprite_x == self.selected_block[-1][1] and sprite_y == self.selected_block[-1][2]:
                        pass  # 如果选取的方块和上一次选取的方块相同，则略过
                    else:
                        if judge_remove([self.selected_block[0][2], self.selected_block[0][1]], [sprite_y, sprite_x],
                                        self.board.array):
                            click_sprite.un_click(self.selected_block[0][0], self.click_anime[0])
                            self.batch.remove(self.selected_block[0][0])
                            self.batch.remove(click_sprite)
                            self.board.array[sprite_y][sprite_x] = 0
                            self.board.array[self.selected_block[0][2]][self.selected_block[0][1]] = 0
                            self.selected_block.pop(0)
                            self.click_anime.pop(0)
                        else:
                            click_sprite.click(self.click_anime)
                            self.selected_block.append([click_sprite, sprite_x, sprite_y])
                            click_sprite.do(Delay(0.7) + CallFunc(self.un_click_block, click_sprite) * 2)
            else:
                pass

    def un_click_block(self, click_sprite):
        click_sprite.un_click(self.selected_block[0][0], self.click_anime[0])
        self.click_anime.pop(0)
        self.selected_block.pop(0)


class Board:
    def __init__(self):
        self.column = setting.level_info[0]["column"]
        self.row = setting.level_info[0]["row"]
        self.array = [[0 for col in range(self.column)] for row in range(self.row)]
        self.sort_position = [[] for k in range(len(setting.fruits))]              # 分别存储每一类方块位置
        self.init_block()

    def draw(self, pos, batch):
        left = pos[0]
        bottom = pos[1]

        for i in range(self.row):
            for j in range(self.column):
                fruit = self.array[i][j]
                if fruit != 0:
                    sprite = Block(fruit)
                    sprite.position = j * setting.square_size + left + j*2, i * setting.square_size + bottom + i*2     # *2为空隙宽度
                    batch.add(sprite, z=3, name=f"{i, j}")

    def init_block(self):
        """
        为每个方块随机赋值，empty_position_list存储还未写入值的位置
        """
        def pair_fruit_generator(block_value):
            random_row = random.randint(0, len(empty_position_list) - 1)
            while len(empty_position_list[random_row]) == 0:                # 如果抽中的行没有空的位置，删除此行并重新生成
                empty_position_list.pop(random_row)
                random_row = random.randint(0, len(empty_position_list) - 1)
            random_col = random.randint(0, len(empty_position_list[random_row]) - 1)
            add_position_row = empty_position_list[random_row][random_col][0]
            add_position_col = empty_position_list[random_row][random_col][1]
            self.array[add_position_row][add_position_col] = block_value
            empty_position_list[random_row].pop(random_col)
            self.sort_position[block_value - 1].append([add_position_row, add_position_col])

        k = 0
        i = 0
        empty_position_list = [[0 for col in range(self.column)] for row in range(self.row)]
        while k < self.row:
            empty_position_list[k][i] = [k, i]
            i = i + 1
            if i == self.column:
                i = 0
                k = k + 1
        i = 0
        while i < (self.column * self.row)/2:
            random_num = random.randint(1, len(setting.fruits))
            pair_fruit_generator(random_num)
            pair_fruit_generator(random_num)
            i = i + 1


class Block(cocos.sprite.Sprite):
    def __init__(self, fruit):
        super().__init__(setting.fruit_images[fruit-1], scale=1)

    def click(self, anime_list):
        x = self._get_x()
        y = self._get_y()
        self.do(ScaleTo(0.85, 0.09))
        batch = self.get_ancestor(BatchNode)
        sprite = cocos.sprite.Sprite(setting.click_anime)
        sprite.position = x, y
        batch.add(sprite, z=2)
        anime_list.append(sprite)

    def un_click(self, selected_sprite, click_anime):
        batch = self.get_ancestor(BatchNode)
        batch.remove(click_anime)
        selected_sprite.do(ScaleTo(1, 0.09))
        self.do(ScaleTo(1, 0.09))

