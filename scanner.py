#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@author: Tanmoy Das Gupta, Sandeepan Sengupta, Tamojit Saha
"""

def scanner(array, pattern):
    """
    Test usage:
    scanner(larger_1D_numpy_array, smaller_1D_numpy_array)
    """

    import numpy as np
    if np.size(pattern) < np.size(array):

        i = 0
        index = []
        while i < np.size(array):
            if np.array_equal(array[i:i+np.size(pattern)], pattern):
                index.append(i)
            i += np.size(pattern) #skip blocks

        if np.size(index) > 0:
            return index
        else:
            return index.append(-1)
