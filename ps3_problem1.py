# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 15:10:06 2021

@author: scout
"""

def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    wordvalue = word.lower()
    value = 0
    for c in wordvalue:
        c = SCRABBLE_LETTER_VALUES[c]
        value = value + c
    print((7 * len(word)) - (3*(n-len(word))))
    if (7 * len(word) - 3*(n-len(word))) > 1:
        value = value * (7 * len(word) - 3*(n-len(word)))
        return(value)
    elif 1 > (7 * len(word) - 3*(n-len(word))):
        return(value)