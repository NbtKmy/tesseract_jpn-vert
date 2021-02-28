import glob
import random
import sys
import textwrap
from collections import Counter

def read_chars(filename):
    # Wie oft tauchen die einzelnen Zeichen?
    count = Counter()
    with open(filename) as chars:
        for line in chars:
            count[int(line.split(',')[0],base=16)] = 0
    return count

def read_all_words(dir_s):
    words = {}
    files = glob.glob(dir_s + '/*.csv')
    for filename in files:
        with open(filename, encoding='utf-8') as file:
            for line in file:
                word = line.split(',')[0]
                words[word] = True
    return list(words.keys())

def main():
    # training_bs.txt
    text = ''
    # Auch wenn die Zeichen in Neologd-Wörterbuch auftaucht, werden die folgenden Zeichen in den Text aufgenommen
    add_list = [
                    '︙',    # full-width 3 points leader
                    '―',     # full-width dash
                    '〱',    # Vertical Kana Repeat Mark
                    '〲',    # Vertical Kana Repeat with Voiced Sound Mark
                    '〻',    # Vertical Ideographic Iteration Mark
                    '￥',    # Fullwidth Yen Sign
                    '〃',    # Ditto Mark
                    'ゟ',    # Hiragana Digraph Yori
                    'ゝ',    # Hiragana Iteration Mark
                    'ヽ',    # Katakana Iteration Mark
                    'ゞ',    # Hiragana dakuten Iteration Mark
                    'ヾ'     # Katakana dakuten Iteration Mark
                ]

    count_required = 20
    chars = read_chars('./traindata/chars.txt')
    words = read_all_words('/path/to/mecab-ipadic-neologd/seed') # hier muss der korrekte Path-Name zu Neologd-Wörterbuch stehen
    print("Total words %d" % len(words))
    training = open('./traindata/training_bs.txt', 'w', encoding='utf-8')
    random.shuffle(words)
    for word in words:
        min_count = 10000
        skip = False
        # Das Zeichen, die am wenigsten in word auftaucht
        for c in word:
            code = ord(c)
            if code not in chars:
                # Wenn das Zeichen nicht auf Char-List steht, skippen
                skip = True
                # Wenn so, dann wird angezeigt
                print("skipped %s by %s" % (word, c), file=sys.stderr)
                break
            count = chars[code] + 1
            if count < min_count:
                min_count = count
        # Wenn das Word weniger als 20-mal auftaucht, wird es in den Trainingstext aufgenommen
        if not skip and min_count <= count_required:
            text += word

            # Nach einem Wort wird ein Zeichen aus der Add-List at rondom hinzufügen
            if random.random() <= 0.3:
                random_c = random.choice(add_list)
                text += random_c
                c_code = ord(random_c)
                chars[c_code] += 1

            # Das verwendete Zeichen wird gezählt 
            for c in word:
                code = ord(c)
                chars[code] += 1


    # Der gesamte Text wird gespeichert
    training.write("\n".join(textwrap.wrap(text, width=40)))
    training.close()

    # Das Zeichen, das nicht verwendet wurde, wird unter "unused_chars.txt" aufgelistet
    with open('./traindata/unused_chars.txt', 'w', encoding='utf-8') as uc:
        for c in chars:
            if chars[c] == 0:
                print('0x%x,%s' % (c, chr(c)), file=uc)

if __name__ == '__main__':
    main()
