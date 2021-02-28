import urllib.request
import re

# add_list enthält die Schriftzeichen, die in chars.txt bleiben sollen, obwohl sie auf der 'forbidden_characters'-Liste stehen
add_list = [
                0x205D,  # ︙ full-width 3 points leader
                0x2014,  # ― full-width dash
                0x3031,  # 〱 Vertical Kana Repeat Mark
                0x3032,  # 〲 Vertical Kana Repeat with Voiced Sound Mark
                0x303B,  # 〻 Vertical Ideographic Iteration Mark
                0xFFE5,  # ￥ Fullwidth Yen Sign
                0x3003,  # 〃 Ditto Mark
                0x309F,  # ゟ Hiragana Digraph Yori
                0x309D,  # ゝ Hiragana Iteration Mark
                0x30FD,  # ヽ Katakana Iteration Mark
                0x309E,  # ゞ Hiragana dakuten Iteration Mark
                0x30FE  # ヾ Katakana dakuten Iteration Mark                
            ]
# Chars-List erstellen. Sie soll die JIS Kanji-Zeichen (von 1te bis 4te Level) enthalten
chars = {}

with urllib.request.urlopen('http://x0213.org/codetable/sjis-0213-2004-std.txt') as f:
    for line in f.read().decode('ascii').splitlines():
        if line[0] == '#':
            continue
        else:
            m = re.search('U\+([0-9a-f]{4})', line, flags=re.I)
            if m:
                code = int(m.group(1), base=16)
                if code > 0x20:
                    chars[code] = True

# Del-List aus /langdata/jpn_vert/forbiden_characters erstellen
# forbiden_characters von jpn_vert ist unter der URL zu finden: https://github.com/tesseract-ocr/langdata/tree/master/jpn_vert

del_list = {}
with open('/.traindata/forbidden_characters') as f:
    for line in f:
        m = re.search('0x([0-9a-f]{2,4})(-0x([0-9a-f]{2,4}))?\s*$', line, flags=re.I)
        if m:
            if m.group(2):
                range_s = [int(m.group(1), base=16), int(m.group(3), base=16)]
            else:
                range_s = [int(m.group(1), base=16), int(m.group(1), base=16)]
        for c in chars:
            if range_s[0] <= c <= range_s[1]:
                # full-width alphabets&numbers & Kanji-Zeichen sollen in der Char-List bleiben
                if not (ord('！') <= c <= ord('｝') or ord('豈') <= c <= ord('﫿')):
                    print("%s excluded as %x - %x" % (chr(c), range_s[0], range_s[1]))
                    del_list[c] = True

# die Schriftzeichen in der Del-List aus der Char-List löschen
for c in del_list:
    del chars[c]

# Danach die Zeichen auf der Add-List in die Char-List hinzufügen
for c in add_list:
    chars[c] = True

with open('./traindata/chars.txt', 'w') as wf:
    for code in sorted(chars):
        print("%#x,%s" % (code, chr(code)), file=wf)
