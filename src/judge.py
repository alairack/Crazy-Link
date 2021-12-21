

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
        corner_1 = [max(sprite1_position[0], sprite2_position[0]), min(sprite2_position[1], sprite1_position[1])]
        corner_2 = [min(sprite1_position[0], sprite2_position[0]), max(sprite2_position[1], sprite1_position[1])]
    elif sprite2_position[0] < sprite1_position[0] and sprite2_position[1] < sprite1_position[1]:
        corner_1 = [max(sprite1_position[0], sprite2_position[0]), min(sprite2_position[1], sprite1_position[1])]
        corner_2 = [min(sprite1_position[0], sprite2_position[0]), max(sprite2_position[1], sprite1_position[1])]
    else:
        corner_1 = [max(sprite1_position[0], sprite2_position[0]), max(sprite2_position[1], sprite1_position[1])]
        corner_2 = [min(sprite1_position[0], sprite2_position[0]), min(sprite2_position[1], sprite1_position[1])]
    if array[corner_1[0]][corner_1[1]] == 0:
        if a_straight_line(sprite1_position, corner_1, array):
            if a_straight_line(sprite2_position, corner_1, array):
                return True
    if array[corner_2[0]][corner_2[1]] == 0:
        if a_straight_line(sprite1_position, corner_2, array):
            if a_straight_line(sprite2_position, corner_2, array):
                return True
            else:
                return False
        else:
            return False
    else:
        return False


def two_turn(sprite1_position, sprite2_position, array):
    i = 1
    array.insert(0, [0 for x in range(len(array[0]))])
    try:
        while array[sprite1_position[0] - i + 1][sprite1_position[1]] == 0 and sprite1_position[0] - i + 1 > -1:
            if one_turn([sprite1_position[0] - i + 1, sprite1_position[1]], [sprite2_position[0] + 1, sprite2_position[1]], array):
                array.pop(0)                 # +1是在前面插入空行后，索引值依次+1
                return True
            i = i + 1
    except IndexError:
        pass
    array.pop(0)

    i = 1
    array.append([0 for x in range(len(array[0]))])                         # 通过检测array 的长度来确定行和列的长度
    try:
        while array[sprite1_position[0] + i][sprite1_position[1]] == 0 and sprite1_position[0] + i < len(array):
            if one_turn([sprite1_position[0] + i, sprite1_position[1]], sprite2_position, array):
                array.pop()
                return True
            i = i + 1
    except IndexError:
        pass
    array.pop()

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
        while array[sprite1_position[0]][sprite1_position[1] + i] == 0 and sprite1_position[1] + i < len(array[0]):
            if one_turn([sprite1_position[0], sprite1_position[1] + i], sprite2_position, array):
                for y in array:
                    y.pop()
                return True
            i = i + 1
    except IndexError:
        pass
    for y in array:
        y.pop()
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
