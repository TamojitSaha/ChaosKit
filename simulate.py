#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@author: Tanmoy Das Gupta, Sandeepan Sengupta, Tamojit Saha
"""

from steganography import embed, decipher
from entropy import ENTROPY
from matplotlib.pyplot import imread

embed('micro.txt')
print '\n'
print decipher()
print '\n'
print ENTROPY(imread('image.tiff')), 'Original Image Entropies'
print ENTROPY(imread('image_encoded.tiff')), 'Encoded Image Entropies'

print '\n\n'

embed('preamble.txt')
print '\n'
print decipher()
print '\n'
print ENTROPY(imread('image.tiff')), 'Original Image Entropies'
print ENTROPY(imread('image_encoded.tiff')), 'Encoded Image Entropies'

print '\n\n'

embed('unicode.txt')
print '\n'
print decipher()
print '\n'
print ENTROPY(imread('image.tiff')), 'Original Image Entropies'
print ENTROPY(imread('image_encoded.tiff')), 'Encoded Image Entropies'

from reporter import reporter
reporter('image.tiff')
reporter('image_encoded.tiff')
