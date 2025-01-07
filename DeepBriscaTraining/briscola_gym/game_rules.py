values_points = {1: 11, 2: 0, 3: 10, 4: 0, 5: 0, 6: 0, 7: 0, 8: 2, 9: 3, 10: 4}


def select_winner(table: list, briscola):
    first = table[0]
    second = table[1]
    first_points = values_points[first.value]
    second_points = values_points[second.value]
    first_briscola = first.seed == briscola.seed
    second_briscola = second.seed == briscola.seed
    if second.seed == first.seed:
        if first_points == 0 and second_points == 0:
            return second.value > first.value
        else:
            return second_points > first_points
    elif first_briscola:
        return 0
    elif second_briscola:
        return 1
    else:
        return 0