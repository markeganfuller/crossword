TEST_WORDS = """AARDVARK
HAMMER
HELLO
TOMORROW
TODAY
PYTHON
DOJO
LONDON
PIZZA
BEAR
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
            if self[key] != value:
                raise KeyExists(key)
        super(nicedict, self).__setitem__(key, value)


class Grid(object):
    def __init__(self):
        self.grid = nicedict()
        self.words = dict()

    def put_word(self, word, x, y, orientation=VERTICAL):
        grid = nicedict(self.grid)
        try:
            for i, letter in enumerate(word):
                if orientation is VERTICAL:
                    grid[(x, y + i)] = letter
                else:
                    grid[(x + i, y)] = letter
            self.grid = grid
            self.words[word] = (x, y, orientation)
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

    def crosswordplus(self, word):
        for w in self.words.keys():
            try:
                if self.crossword(word, w):
                    return w
            except AssertionError:
                pass

    def draw(self):
        min_x = min(x for x, y in self.grid.keys())
        min_y = min(y for x, y in self.grid.keys())
        max_x = max(x for x, y in self.grid.keys())
        max_y = max(y for x, y in self.grid.keys())

        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                print self.grid.get((x, y), ' '),
            print ''


def get_next_word(words, letters=None):
    letters = set(letters)
    for word in words:
        for letter in set(word):
            if letter in letters:
                return word


def main():
    grid = Grid()

    words = list(TEST_WORDS)
    words = sorted(words, key=lambda k: len(k))
    word = words.pop()

    grid.put_word(word, 0, 0, VERTICAL)

    for _ in range(9999):
        if not words:
            break

        for nextword in list(words):
            if grid.crosswordplus(nextword):
                word = nextword
                words.remove(nextword)
                break

    else:
        print "Could not place", words

    grid.draw()

    return word


if __name__ == '__main__':
    main()
