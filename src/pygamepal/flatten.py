#
# pygamepal, by Rik Cross
#  -- homepage: github.com/rik-cross/pygamepal
#  -- MIT licenced, free to use, modify and distribute
#  -- run 'pip install pygamepal' to use
#

def flatten(list):

    '''
    Flatten a multi-dimensional list into a single list.

    :param list(list(any)) list: the multi-dimensional list to flatten.
    :return list(any) newList: the flattened, single list.
    '''

    newList = []
    for i in list:
        for j in i:
            newList.append(j)
    return newList