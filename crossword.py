from collections import defaultdict

TEST_WORDS = """AARDVARK
HAMMER
HELLO
TOMORROW
TODAY
PYTHON
DOJO
LONDON
PIZZA
BEER
""".split()

VERTICAL = 1
HORIZONTAL = 2


class KeyExists(Exception):
    pass


class nicedict(dict):
    def __repr__(self):
        return repr([(k, self[k]) for k in sorted(self.keys())])

    def __setitem__(self, key, value):
        if key in self.keys():
            raise KeyExists(key)
        super(nicedict, self).__setitem__(key, value)


class Grid(object):
    """
    >>> g = Grid()
    >>> g.put_word('BEER', 0, 0, HORIZONTAL)
    >>> g.draw()
    BEER
    >>> g.put_word('PIZZA', 5, 0, VERTICAL)
    >>> g.grid
    >>> g.draw()
    BEERP
        I
        Z
        Z
        A
    >>> g.put_word('HELLO', 1, -1, VERTICAL)
    >>> g.draw()
    B E E R   P 
              I 
              Z 
              Z 
              A 
    >>> g.crossword('DOJO', 'HELLO')
    >>> g.draw()
    """

    def __init__(self):
        self.grid = nicedict()
        self.words = dict()

    def put_word(self, word, x, y, orientation=VERTICAL):
        grid = nicedict(self.grid)
        self.words[word] = (x, y, orientation)
        try:
            for i, letter in enumerate(word):
                if orientation is VERTICAL:
                    grid[(x, y+i)] = letter
                else:
                    grid[(x+i, y)] = letter
            self.grid = grid
            return True
        except KeyExists:
            return False

    def crossword(self, word, crossword):
        x, y, o = self.words[crossword]

        for letter in word:
            if letter in crossword:
                if o is HORIZONTAL:
                    x += crossword.index(letter)
                else:
                    y += crossword.index(letter)
                break
        else:
            assert False, 'Letter not found in crossword'

        o = VERTICAL if o is HORIZONTAL else HORIZONTAL

        if o is HORIZONTAL:
            x -= word.index(letter)
        else:
            y -= word.index(letter)

        return self.put_word(word, x, y, o)

    def draw(self):
        minx = min(x for x, y in self.grid.keys())
        miny = min(y for x, y in self.grid.keys())
        maxx = max(x for x, y in self.grid.keys())
        maxy = max(y for x, y in self.grid.keys())

        for y in range(miny, maxy+1):
            for x in range(minx, maxx+1):
                print self.grid.get((x, y), ' '),
            print ''


def get_next_word(words, letters=None):
    if letters:
        words = filter(lambda word: any(n for n in letters if n in word), words)
    return sorted(words, key=lambda k: len(k))[0]


def main():
    grid = Grid()

    words = list(TEST_WORDS)

    word = get_next_word(words)
    words.remove(word)

    grid.put_word(word, 0, 0, VERTICAL)

    for i in range(9999):
        if not words:
            break

        nextword = get_next_word(words, word)

        if grid.crossword(nextword, word):
            words.remove(nextword)
            word = nextword
        else:
            words.remove(nextword)
            words.append(nextword)


        words.remove(word)

    return word

