import matplotlib.pyplot as plt
import numpy as np

def get_seperators_from_line(imgarray):
    """ Takes image array of a line and outputs the seperating spaces for words"""
    shape_x, shape_y = imgarray.shape
    total_seperator = 0
    result = []
    for i in range(shape_y):
        curr_col = imgarray[:, i]
        if np.average(curr_col) > 250.0:
            result.append(i)
    return result

def get_seperators_from_pagragraph(imgarray):
    """ Takes image array of a paragraph and outputs the seperating spaces for lines """
    shape_x, shape_y = imgarray.shape
    total_seperator = 0
    result = []
    for i in range(shape_x):
        curr_row = imgarray[i, :]
        if np.average(curr_row) > 250.0:
            result.append(i)
    return result

def group_consecutives(vals, step=1):
    """Finds gaps between words or letters in an array"""
    run = []
    result = [run]
    expect = None
    for v in vals:
        if (v == expect) or (expect is None):
            run.append(v)
        else:
            run = [v]
            result.append(run)
        expect = v + step
    return result

def breakup_consecutive_line(result):
    """ Takes gaps of words and letters and classifies it into word or letter gap """
    word_indices = []
    letter_indices = []
    for group in result:
        if len(group) <= 2:
            letter_indices.append(group[0])
        else:
            word_indices.append(group[int(len(group)/2)])
    return (word_indices, letter_indices)
            
    
def breakup_consecutive_paragraph(result):
    """ Takes gaps from paragraph image and outputs the lines """
    print(result)
    line_indices = []
    for group in result:
        line_indices.append((group[0], group[-1]))
    return line_indices


def allocate_letters(word_indices, letter_indices):
    """ Takes letter indices and allocates them into words."""
    """ Returns a map that maps words to its letters. """
    letter_pointer = 0
    end = len(letter_indices)
    word_map = {}
    for i in range(len(word_indices)-1):
        left_word_index = word_indices[i]
        right_word_index = word_indices[i+1]
        curr_letters = [left_word_index]
        while left_word_index < letter_indices[letter_pointer] < right_word_index:
            curr_letters.append(letter_indices[letter_pointer])
            letter_pointer += 1
            if letter_pointer > end-1:
                curr_letters.append(right_word_index)
                word_map[(left_word_index, right_word_index)] = curr_letters
                return word_map
        curr_letters.append(right_word_index)
        word_map[(left_word_index, right_word_index)] = curr_letters
    return word_map

def line_pipeline(lineimg):
    """ Takes image of a line and outputs the line's word map """ 
    groups = group_consecutives(get_seperators_from_line(lineimg))
    word_indices, letter_indices = breakup_consecutive_line(groups)
    wordmap = allocate_letters(word_indices, letter_indices)
    return wordmap

def image_pipeline(imgarray):
    """ Pipeline for an image. Out puts a graph structure for lines, words, characters"""
    result = get_seperators_from_pagragraph(imgarray)
    result = breakup_consecutive_paragraph(group_consecutives(result))
    output = {}
    for i in range(1, len(result)):
        start, end = result[i]
        currline = imgarray[result[i-1][1]:start, :]
        currmap = line_pipeline(currline)
        output[(result[i-1][1],start)] = currmap
    return output




