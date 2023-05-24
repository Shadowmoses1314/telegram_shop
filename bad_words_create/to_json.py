import json

ar = []

with open('bad_words.txt', encoding='utf-8') as r:
    for line in r:
        words = line.strip().lower().split(' ')
        for word in words:
            if word != '':
                ar.append(word)

with open('bad_words.json', 'w', encoding='utf-8') as e:
    json.dump(ar, e)