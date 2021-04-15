from nltk.tokenize import regexp_tokenize
from collections import defaultdict
from random import choice, choices


def can_start(token):
    return token[0].isupper() and token[-1] not in '.!?'


def can_end(token):
    return token[-1] in '.!?'


pattern = r'[^\s]+'
filename = input()
with open(filename, 'r', encoding="utf-8") as f:
    corpus = f.read()
    tokens = regexp_tokenize(corpus, pattern)
    n_tokens = len(tokens)
    trigrams = [(f'{tokens[index]} {tokens[index + 1]}', tokens[index + 2]) for index in range(n_tokens - 2)]
    trigram_dict = defaultdict(dict)
    for head, tail in trigrams:
        trigram_dict[head].setdefault(tail, 0)
        trigram_dict[head][tail] += 1

head = None
sentence = []
count = 0
heads = list(trigram_dict.keys())
while count < 10:
    sentence_complete = False
    sentence_redo = False
    if not head:
        while not head or not can_start(head.split()[0]) or can_end(head.split()[1]):
            head = choice(heads)
        sentence = [head]
    while not sentence_complete and not sentence_redo:
        population = list(trigram_dict[head].keys())
        weights = list(trigram_dict[head].values())
        tail_list = choices(population, weights=weights)
        new_head = None
        for tail in tail_list:
            potential_head = f'{head.split()[1]} {tail}'
            if len(sentence) == 0:
                if can_start(tail):
                    new_head = potential_head
                    break
            elif len(sentence) < 4:
                if not can_end(tail):
                    new_head = potential_head
                    break
            else:
                new_head = potential_head
                if can_end(tail):
                    sentence_complete = True
                break
        head = new_head
        if not new_head:
            sentence_redo = True
        else:
            head = new_head
            sentence.append(head.split()[1])
    if sentence_complete:
        print(*sentence)
        count += 1
    sentence = []
