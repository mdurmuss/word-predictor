#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Mustafa Durmuş [mustafa-durmuss@outlook.com]


from predictor import WordPredictor
from functools import lru_cache


@lru_cache()
def find_levenshtein_distance(s, t):
    if s == "":
        return len(t)
    if t == "":
        return len(s)
    if s[-1] == t[-1]:
        cost = 0
    else:
        cost = 2  # substitutes is 2.

    res = min([find_levenshtein_distance(s[:-1], t)+1,
               find_levenshtein_distance(s, t[:-1])+1,
               find_levenshtein_distance(s[:-1], t[:-1]) + cost])

    return res


def spell_checking(inp_word, predictor):

    # getting all the words as list.
    words = list(predictor.dict.keys())

    result_dict = {}
    for idx, word in enumerate(words):
        distance = find_levenshtein_distance(inp_word, word)  # mesafeyi bul.
        if distance in [1, 2, 3]:  # sadece 1-2-3 mesafelerindeki kelimeleri kaydet.
            result_dict.setdefault(str(distance), []).append(idx)  # bir key için birden fazla value eklemek.

    count = 0
    did_u_mean_words = []
    for key, value in sorted(result_dict.items()):
        for idx in value:
            # print(f'\t{words[idx]} -- ({key})')
            count += 1
            did_u_mean_words.append(words[idx])
            if count == 3:
                return did_u_mean_words
                break


if __name__ == '__main__':
    # creating the object.
    corpus_path = "./corpora/little_prince.txt"
    predictor = WordPredictor(corpus_path)

    inp_word = "irens"
    print("Girilen Kelime: ", inp_word)
    print(spell_checking(inp_word, predictor))
