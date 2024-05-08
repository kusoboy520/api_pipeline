import random

def itemtoitme(itemid: int):
    '''
    Item to Itme Model.
    '''
    if itemid <50:
        return []
    else:
        output = [random.sample(range(1,100),3)]
        return output