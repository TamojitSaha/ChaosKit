#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@author: Tanmoy Das Gupta, Sandeepan Sengupta, Tamojit Saha
"""


from configurator import configurator as cfgr
CHANNEL, PLANE, SCOPE, BUFFER = cfgr('setup.cfg')

def slicer(file_name='image.tiff', channel=CHANNEL, plane=PLANE):
    """
    Test usage:
    slc('image.tiff', 'R', 0)
    slc('image.tiff')
    """

    from matplotlib.pyplot import imread
    image_data = imread(file_name)

    if channel == 'R':
        slc = image_data[:, :, 0]
        slc &= pow(2, plane)
        slc = slc/pow(2, plane)
        return slc

    if channel == 'G':
        slc = image_data[:, :, 1]
        slc &= pow(2, plane)
        slc = slc/pow(2, plane)
        return slc

    if channel == 'B':
        slc = image_data[:, :, 2]
        slc &= pow(2, plane)
        slc = slc/pow(2, plane)
        return slc

if __name__ == '__main__':
    slicer()
