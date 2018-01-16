#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@author: Tanmoy Das Gupta, Sandeepan Sengupta, Tamojit Saha
"""

IMAGE_FILE = 'image.tiff'
NEIGHBORHOOD = 8
DPI = 1000
SCALE = 5

from bitplane import bitplane as bp
from neighborhood import neighborhood as ngbd
from autocorrelation import autocorrelation as atc
from entropy import entropy as entropy
from histogram import histogram as hist

from configurator import configurator as cfgr
CHANNEL, PLANE, SCOPE, BUFFER = cfgr('setup.cfg')

def reporter(image_file=IMAGE_FILE, neighborhood=NEIGHBORHOOD, scale=SCALE, dpi=DPI, channel=CHANNEL, plane=PLANE, scope=SCOPE):
    """
    Test usage:
    reporter('image.tiff')
    reporter('image.tiff', 8, 5, 1000)
    reporter('image.tiff', 8, 5, 500, 'R', 0, 5)
    """

    bp(image_file, dpi, channel, plane)
    hist(image_file, scale, dpi)
    atc(image_file, dpi)
    ngbd(image_file, neighborhood, dpi)
    entropy(image_file)

if __name__ == '__main__':
    reporter()
