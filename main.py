# A Python program to cheat at Scrabble. Unlike most Scrabble cheaters, this program looks not only at the letters in
# your hand but also the letters on the board.

unit_tests = True

sowpods = open('sowpods.txt')  # the official Scrabble dictionary. To use a different wordlist, just use a different file.
scrabble_list = []
for line in sowpods:
    scrabble_list.append(line.strip())
sowpods.close()

scrabble_list = scrabble_list[6:]  # cut out the first few lines because they're general info and not part of the dictionary

scrabble_board = []  # make an empty 15 by 15 board
for row in range(15):
    r = []
    for col in range(15):
        r.append(None)
    scrabble_board.append(r)

def getWordsByLetter(letter):
    """Returns all the words starting with a given letter"""
    words = []
    for idx in range(len(scrabble_list)):
        if scrabble_list[idx][0] == letter:
            words.append(scrabble_list[idx])
    return words


def getWordValue(word):
    """Function to calculate and return the point value of a scrabble word. Does not account for letter or word bonuses."""
    letter_values = {'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1,
                     'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8,
                     'y': 4, 'z': 10}
    result = 0
    for letter in word:
        result += letter_values[letter]
    return result

points_dict = {}  # a dictionary to keep track of the point value of every word
for word in scrabble_list:
    points_dict[word] = getWordValue(word)

def anagramFunction(letters):
    """Finds all the words that can be made with the given letters"""
    available_words = []
    for letter in letters:
        words = getWordsByLetter(letter)
        for word in words:
            letters_copy = list(letters)
            for l in word:
                if l in letters_copy:
                    letters_copy.remove(l)  # ensures that each letter is only counted once
                elif "." in letters_copy:
                    letters_copy.remove(".")  # "." represents a blank tile
                else:
                    break
            else:
                available_words.append(word)
    return available_words


def getWordsWithWord(word, space_before=None, space_after=None):
    """Finds all the words that include the given word. Doesn't count the word itself."""
    available_words = []
    for item in scrabble_list:
        if word in item and len(item) > len(word):
            if space_before is not None and space_after is not None:
                split_word = item.split(word)
                if not (len(split_word[0]) <= space_before and len(split_word[1]) <= space_after):
                    continue
            available_words.append(item)
    return available_words


def getAnagramDict(letters):
    """Get anagrams and their point values."""
    anagram_dict = {}
    words = anagramFunction(letters)
    for word in words:
        anagram_dict[word] = getWordValue(word)
    return anagram_dict


def findRowWords():
    """Get a list of the words in each row (and the column number at which each word starts)"""
    row_words = []  # a 2d list to hold the list of words in each row
    for i in range(15):
        row_words.append([])
    for row_idx in range(15):
        word = ""
        for col_idx in range(15):
            letter = lookAtBoard(row_idx, col_idx)
            if letter is None:
                if len(word) > 1:
                    row_words[row_idx].append((word, col_idx - len(word)))
                word = ""
            else:
                word += letter
    return row_words


def findColWords():
    """Get a list of the words in each column (and the row number at which each word starts)"""
    col_words = []
    for i in range(15):
        col_words.append([])
    for col_idx in range(15):
        word = ""
        for row_idx in range(15):
            letter = lookAtBoard(row_idx, col_idx)
            if letter is None:
                if len(word) > 1:
                    col_words[col_idx].append((word, row_idx - len(word)))
                word = ""
            else:
                word += letter
    return col_words


def addWordToBoard(word, row, column, orient):
    """Add a word to the board at the given location, letter by letter"""
    scrabble_board[row][column] = word[0]
    if orient == 'horizontal':
        for i in range(1, len(word)):
            scrabble_board[row][column + i] = word[i]
    elif orient == 'vertical':
        for i in range(1, len(word)):
            scrabble_board[row + i][column] = word[i]


def lookAtBoard(row, column):
    """Returns the item at the given position"""
    return scrabble_board[row][column]


def findWordsAndSpace():
    """Find all the row and column words and the space before and after each word. If a space is right next to a different
    word, that doesn't count as a blank space."""
    col_word_space = []
    for i in range(15):
        col_word_space.append([])
    col_words = findColWords()
    last_pos = 0
    for n in range(15):
        for idx in range(len(col_words[n])):
            end_pos = col_words[n][idx][1] + len(col_words[n][idx][0]) - 1  # the position of the last letter of the word
            blank_before = col_words[n][idx][1] - last_pos
            if idx != 0:
                blank_before -= 1  # if this isn't the first word, then you need to leave extra space so as not to touch others
            if idx == len(col_words[n]) - 1:  # if this is the last item
                blank_after = 15 - end_pos
            else:
                blank_after = col_words[n][idx + 1][1] - end_pos - 1
            col_word_space[n].append([blank_before, col_words[n][idx][0], blank_after])
    row_word_space = []
    for i in range(15):
        row_word_space.append([])
    row_words = findRowWords()
    last_pos = 0
    for n in range(15):
        for idx in range(len(row_words[n])):
            end_pos = row_words[n][idx][1] + len(row_words[n][idx][0]) - 1  # the position of the last letter of the word
            blank_before = row_words[n][idx][1] - last_pos
            if idx != 0:
                blank_before -= 1  # if this isn't the first word, then you need to leave extra space so as not to touch others
            if idx == len(row_words[n]) - 1:  # if this is the last item
                blank_after = 15 - end_pos
            else:
                blank_after = row_words[n][idx + 1][1] - end_pos - 1
            row_word_space[n].append([blank_before, row_words[n][idx][0], blank_after])
    return {'row': row_word_space, 'column': col_word_space}


def makeWords(letters):
    """Find all the words that can be made with the letters in the player's hand and the letters on the board"""
    row_words = findWordsAndSpace()['row']
    col_words = findWordsAndSpace()['column']
    new_row_words = []
    new_col_words = []
    for row in row_words:
        for triple in row:
            word = triple[1]
            possible_row_words = getWordsWithWord(word, triple[0], triple[2])
            for possible_word in possible_row_words:
                remaining_letters = possible_word.replace(word, "")
                owned_letters = list(letters)
                for letter in remaining_letters:
                    if letter in owned_letters:
                        owned_letters.remove(letter)
                    elif "." in owned_letters:  # "." represents a blank tile
                        owned_letters.remove(".")
                    else:
                        break
                else:
                    new_row_words.append((possible_word, points_dict[possible_word]))
    for col in col_words:
        for triple in col:
            word = triple[1]
            possible_col_words = getWordsWithWord(word, triple[0], triple[2])
            for possible_word in possible_col_words:
                remaining_letters = possible_word.replace(word, "")
                owned_letters = list(letters)
                for letter in remaining_letters:
                    if letter in owned_letters:
                        owned_letters.remove(letter)
                    elif "." in owned_letters:
                        owned_letters.remove(".")
                    else:
                        break
                else:
                    new_col_words.append((possible_word, points_dict[possible_word]))
    return {'row': sorted(new_row_words, key=lambda x: x[1], reverse=True), 'column': sorted(new_col_words, key=lambda x: x[1], reverse=True)}


# main code
#addWordToBoard('running', 0, 2, 'vertical')
#print(findColWords())
# mode = input("Enter a mode (text or visual): ")
# turn_mult = input("Multiple rounds? Answer 'y' or 'n': ")
if unit_tests:
    addWordToBoard('run', 1, 2, 'vertical')
    assert ('run', 1) in findColWords()[2]
    addWordToBoard('animal', 0, 3, 'horizontal')
    assert ('animal', 3) in findRowWords()[0]
    print(findColWords())
    print(findRowWords())
    print(makeWords('nnigstrskpe'))
