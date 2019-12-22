def initial_deck(size):
    return list(range(size))

def deal_into_new_stack(deck):
    return list(reversed(deck))

def cut(deck, n):
    return deck[n:] + deck[:n]

def deal_with_increment(deck, n):
    ret = [None]*len(deck)
    i = 0
    remaining_nones = len(deck)
    deck_it = iter(deck)
    while remaining_nones > 0:
        if ret[i] == None:
            ret[i] = next(deck_it)
            remaining_nones -= 1
        i = (i+n) % len(deck)
    return ret

def test():
    test_deck = initial_deck(10)
    assert deal_into_new_stack(test_deck) == list(range(9,-1,-1))
    assert cut(test_deck, 3) == [3,4,5,6,7,8,9,0,1,2]
    assert cut(test_deck, -4) == [6,7,8,9,0,1,2,3,4,5]
    assert deal_with_increment(test_deck, 3) == [0,7,4,1,8,5,2,9,6,3]

test()

deck = initial_deck(10007)
for line in open('input.txt'):
    s = line.rstrip()
    if s.startswith('deal into new stack'):
        deck = deal_into_new_stack(deck)
    else:
        v = int(line.split()[-1])
        if s.startswith('deal with increment'):
            deck = deal_with_increment(deck, v)
        elif s.startswith('cut'):
            deck = cut(deck, v)
        else:
            assert False
print(deck.index(2019))
