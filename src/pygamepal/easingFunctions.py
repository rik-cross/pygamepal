#
# pygamepal, by Rik Cross
#  -- homepage: github.com/rik-cross/pygamepal
#  -- MIT licenced, free to use, modify and distribute
#  -- run 'pip install pygamepal' to use
#

def easeLinear(x):
    return x

def easeBounceOut(x):
    x = x/100
    if x < 4 / 11:
        return (121 * x * x / 16) * 100
    elif x < 8 / 11:
        return ((363 / 40.0 * x * x) - (99 / 10.0 * x) + 17 / 5.0) * 100
    elif x < 9 / 10:
        return ((4356 / 361.0 * x * x) - (35442 / 1805.0 * x) + 16061 / 1805.0) * 100
    return ((54 / 5.0 * x * x) - (513 / 25.0 * x) + 268 / 25.0) * 100