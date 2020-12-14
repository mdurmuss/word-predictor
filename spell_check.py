#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Mustafa Durmuş [mustafa-durmuss@outlook.com]


from predictor import WordPredictor
from functools import lru_cache


@lru_cache()
def iterative_levenshtein(s, t, costs=(1, 1, 2)):
    """
        iterative_levenshtein(s, t) -> ldist
        ldist is the Levenshtein distance between the strings
        s and t.
        For all i and j, dist[i,j] will contain the Levenshtein
        distance between the first i characters of s and the
        first j characters of t

        costs: a tuple or a list with three integers (d, i, s)
               where d defines the costs for a deletion
                     i defines the costs for an insertion and
                     s defines the costs for a substitution
    """

    rows = len(s)+1
    cols = len(t)+1
    deletes, inserts, substitutes = costs

    dist = [[0 for x in range(cols)] for x in range(rows)]

    # source prefixes can be transformed into empty strings
    # by deletions:
    for row in range(1, rows):
        dist[row][0] = row * deletes

    # target prefixes can be created from an empty source string
    # by inserting the characters
    for col in range(1, cols):
        dist[0][col] = col * inserts

    for col in range(1, cols):
        for row in range(1, rows):
            if s[row-1] == t[col-1]:
                cost = 0
            else:
                cost = substitutes
            dist[row][col] = min(dist[row-1][col] + deletes,
                                 dist[row][col-1] + inserts,
                                 dist[row-1][col-1] + cost)  # substitution

    # printing env.
    # for r in range(rows):
    #     print(dist[r])

    return dist[row][col]


def spell_checking(inp_word, predictor):

    # getting all the words as list.
    words = list(predictor.dict.keys())

    result_dict = {}
    for idx, word in enumerate(words):
        distance = iterative_levenshtein(inp_word, word)  # mesafeyi bul.
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
