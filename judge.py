import time
from settings import Logs


def logs(file):
    def decorator(func):
        def wrapper(sprite1_position, sprite2_position, array):
            file.write(
                f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}  position :{sprite1_position}  {sprite2_position}\n")
            return func(sprite1_position, sprite2_position, array)
        return wrapper
    return decorator


@ logs(Logs().log_file)
def a_straight_line(sprite1_position, sprite2_position, array):
    if sprite1_position[0] == sprite2_position[0]:
        if sprite1_position[1] > sprite2_position[1]:
            i = 1
            while sprite1_position[1] - i > sprite2_position[1]:
                if array[sprite1_position[0]][sprite1_position[1] - i] != 0:
                    return False
                i = i + 1
            return True
        else:
            i = 1
            while sprite1_position[1] + i < sprite2_position[1]:
                if array[sprite1_position[0]][sprite1_position[1] + i] != 0:
                    return False
                i = i + 1
            return True
    elif sprite1_position[1] == sprite2_position[1]:
        if sprite1_position[0] > sprite2_position[0]:
            i = 1
            while sprite1_position[0] - i > sprite2_position[0]:
                if array[sprite1_position[0] - i][sprite1_position[1]] != 0:
                    return False
                i = i + 1
            return True
        else:
            i = 1
            while sprite1_position[0] + i < sprite2_position[0]:
                if array[sprite1_position[0] + i][sprite1_position[1]] != 0:
                    return False
                i = i + 1
            return True
    else:
        return False


def one_turn(sprite1_position, sprite2_position, array):
    print(sprite1_position, sprite2_position)
    if sprite1_position[0] < sprite2_position[0] and sprite1_position[1] < sprite2_position[1]:
        print(1)
        corner_1 = [max(sprite1_position[0], sprite2_position[0]), min(sprite2_position[1], sprite1_position[1])]
        corner_2 = [min(sprite1_position[0], sprite2_position[0]), max(sprite2_position[1], sprite1_position[1])]
    elif sprite2_position[0] < sprite1_position[0] and sprite2_position[1] < sprite1_position[1]:
        print(2)
        corner_1 = [max(sprite1_position[0], sprite2_position[0]), min(sprite2_position[1], sprite1_position[1])]
        corner_2 = [min(sprite1_position[0], sprite2_position[0]), max(sprite2_position[1], sprite1_position[1])]
    else:
        print(3)
        corner_1 = [max(sprite1_position[0], sprite2_position[0]), max(sprite2_position[1], sprite1_position[1])]
        corner_2 = [min(sprite1_position[0], sprite2_position[0]), min(sprite2_position[1], sprite1_position[1])]
    print(corner_1)
    print(corner_2)
    if array[corner_1[0]][corner_1[1]] == 0:
        if a_straight_line(sprite1_position, corner_1, array):
            print(4)
            if a_straight_line(sprite2_position, corner_1, array):
                print(5)
                return True
    if array[corner_2[0]][corner_2[1]] == 0:
        print(6)
        if a_straight_line(sprite1_position, corner_2, array):
            print(7)
            if a_straight_line(sprite2_position, corner_2, array):
                print(8)
                return True
            else:
                return False
        else:
            return False
    else:
        return False


def two_turn(sprite1_position, sprite2_position, array):
    i = 1
    array.insert(0, [0 for x in range(15)])
    try:
        while array[sprite1_position[0] - i + 1][sprite1_position[1]] == 0 and sprite1_position[0] - i + 1 > -1:
            if one_turn([sprite1_position[0] - i + 1, sprite1_position[1]], [sprite2_position[0] + 1, sprite2_position[1]], array):
                array.pop(0)
                return True
            i = i + 1
    except IndexError:
        pass
    array.pop(0)

    i = 1
    array.append([0 for x in range(15)])
    try:
        while array[sprite1_position[0] + i][sprite1_position[1]] == 0 and sprite1_position[0] + i < 11:
            if one_turn([sprite1_position[0] + i, sprite1_position[1]], sprite2_position, array):
                array.pop(10)
                return True
            i = i + 1
    except IndexError:
        pass
    array.pop(10)

    i = 1
    for x in array:
        x.insert(0, 0)
    try:
        while array[sprite1_position[0]][sprite1_position[1] - i + 1] == 0 and sprite1_position[1] - i + 1 > -1:
            if one_turn([sprite1_position[0], sprite1_position[1] - i + 1], [sprite2_position[0], sprite2_position[1] + 1], array):
                for x in array:
                    x.pop(0)
                return True
            i = i + 1
    except IndexError:
        pass
    for x in array:
        x.pop(0)

    i = 1
    for x in array:
        x.append(0)
    try:
        while array[sprite1_position[0]][sprite1_position[1] + i] == 0 and sprite1_position[1] + i < 16:
            if one_turn([sprite1_position[0], sprite1_position[1] + i], sprite2_position, array):
                for y in array:
                    y.pop(15)
                return True
            i = i + 1
    except IndexError:
        pass
    for y in array:
        y.pop(15)
    return False


def judge_remove(sprite1_position, sprite2_position, array):

    if array[sprite1_position[0]][sprite1_position[1]] == array[sprite2_position[0]][sprite2_position[1]]:  # 判断两个图标是否相等
        if a_straight_line(sprite1_position, sprite2_position, array):
            return True
        else:
            if one_turn(sprite1_position, sprite2_position, array):
                return True
            if two_turn(sprite1_position, sprite2_position, array):
                return True
            return False
    else:
        return False





