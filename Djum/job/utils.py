from random import choice, shuffle
from .data import skillist


def skill_maker(x):
    shuffle(skillist)
    xx = list(range(x - 1, x + 1))
    return ' • '.join(skillist[:choice(xx)])


def user_maker(x):
    return 'username' + str(x), 'email' + str(x) + '@mail.fake', 'pass' + str(x) + 'word'
