from random import randint
import numpy as np
from matplotlib import pyplot as plt


def roll(dice_size: int) -> int:
    return randint(1, dice_size)


def roll_6() -> int:
    return roll(6)


def roll_4() -> int:
    return roll(4)


def comp() -> str:
    four_sum = sum([roll_4() for _ in range(9)])
    six_sum = sum([roll_6() for _ in range(6)])

    return "SIX" if six_sum > four_sum else "FOUR" if four_sum > six_sum else "TIE"


def main():
    min_rep = 100
    max_rep = 10 ** 7
    jmp = 1
    rep_archive = []
    result_archive = []
    four_wins = 0
    four_loss = 0
    for i in range(min_rep, max_rep + 1, jmp):
        print(f"\r{str(i / max_rep * 100)[:5]} %\t[{'=' * int(i / max_rep * 20)}{' ' * int(20 - i / max_rep * 20)}]", end="")
        if i % 1000 == 0:
            rep_archive.append(i)
            result_archive.append(four_wins / (i))
        res = comp()
        if res == "FOUR":
            four_wins += 1
        else:
            four_loss += 1

    plt.scatter(rep_archive, result_archive)
    plt.show()


if __name__ == '__main__':
    main()
