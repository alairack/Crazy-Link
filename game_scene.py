import pyglet.resource
from cocos.scene import Scene
from cocos.layer import ColorLayer
import random


def create_game_scene():
    scene = Scene()
    scene.add(GameBackgroundLayer(), z=1)
    return scene


class GameBackgroundLayer(ColorLayer):
    def __init__(self):
        super().__init__(112, 128, 144, 255)
        self.width = 15 * 32 + 40
        self.height = 10 * 32 + 40
        self.board = Board()

    def draw(self):
        super().draw()
        self.board.draw(self.position)


class Board:
    def __init__(self):
        self.array = [[0 for col in range(15)] for row in range(10)]
        self.pair_position = [[] for k in range(12)]
        self.init_fruit()
        self.fruits = ["ananas", 'apple', 'banana', 'cherry', 'durian', 'grape', 'lemon', 'mangosteen', 'origin',
                       'pear', 'strawberry', 'watermelon']
        self.fruit_images = []
        for x in self.fruits:
            image = pyglet.resource.image(f"res/fruit/{x}.png")
            self.fruit_images.append(image)

    def draw(self, pos):
        left = pos[0]
        bottom = pos[1]

        for i in range(10):
            for j in range(15):
                fruit = self.array[i][j]
                if fruit != 0:
                    self.fruit_images[fruit-1].blit(j * 32+left + j, i * 32 + bottom + i)

    def init_fruit(self):
        def pair_fruit_generator(pair_num):
            random_row = random.randint(0, len(empty_position_list) - 1)
            while len(empty_position_list[random_row]) == 0:
                empty_position_list.pop(random_row)
                random_row = random.randint(0, len(empty_position_list) - 1)
            random_col = random.randint(0, len(empty_position_list[random_row]) - 1)
            add_position_row = empty_position_list[random_row][random_col][0]
            add_position_col = empty_position_list[random_row][random_col][1]
            self.array[add_position_row][add_position_col] = pair_num
            empty_position_list[random_row].pop(random_col)
            self.pair_position[pair_num - 1].append([add_position_row, add_position_col])

        k = 0
        i = 0
        empty_position_list = [[0 for col in range(15)] for row in range(10)]
        while k < 10:
            empty_position_list[k][i] = [k, i]
            i = i + 1
            if i == 15:
                i = 0
                k = k + 1
        i = 0
        while i < 75:
            random_num = random.randint(1, 12)
            pair_fruit_generator(random_num)
            pair_fruit_generator(random_num)
            i = i + 1



