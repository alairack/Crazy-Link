def a_straight_line(sprite1_position, sprite2_position, array):
    print(sprite1_position)
    print(sprite2_position)
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



def judge_remove(sprite1_position, sprite2_position, array):

    def one_turn():
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
            print(sprite2_position[1])
            print(sprite1_position[1])
            corner_1 = [max(sprite1_position[0], sprite2_position[0]), max(sprite2_position[1], sprite1_position[1])]
            corner_2 = [min(sprite1_position[0], sprite2_position[0]), min(sprite2_position[1], sprite1_position[1])]
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


    if array[sprite1_position[0]][sprite1_position[1]] == array[sprite2_position[0]][sprite2_position[1]]:  # 判断两个图标是否相等
        if a_straight_line(sprite1_position, sprite2_position, array):
            return True
        else:
            if one_turn():
                return True
            else:
                return False
    else:
        return False