import pyglet.resource


class Settings:
    def __init__(self):
        self.level_info = [{"level": 1, "time": 100, "row": 10, "column": 15},
                           {"level": 2, "time": 120, "row": 15, "column": 15},
                           {"level": 3, "time": 140, "row": 18, "column": 15},
                           {"level": 4, "time": 160, "row": 19, "column": 18},
                           {"level": 5, "time": 180, "row": 22, "column": 20},
                           {"level": 6, "time": 200, "row": 24, "column": 20},
                           {"level": 7, "time": 220, "row": 24, "column": 23},
                           {"level": 8, "time": 240, "row": 25, "column": 24},
                           {"level": 9, "time": 260, "row": 28, "column": 25}]
        self.fruits = ["ananas", 'apple', 'banana', 'cherry', 'durian', 'grape', 'lemon', 'mangosteen', 'origin',
                       'pear', 'strawberry', 'watermelon']
        self.square_size = 32      # 贴图大小
        self.click_anime = pyglet.resource.animation("res/click2.gif")
        self.fruit_images = []
        for x in self.fruits:
            image = pyglet.resource.image(f"res/fruit/{x}.png")
            self.fruit_images.append(image)