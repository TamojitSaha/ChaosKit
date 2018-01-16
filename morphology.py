#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@author: Tanmoy Das Gupta, Sandeepan Sengupta, Tamojit Saha
"""

from configurator import configurator as cfgr
CHANNEL, PLANE, SCOPE, BUFFER = cfgr('setup.cfg')

def morphology(file_name='image.tiff', channel=CHANNEL, plane=PLANE, scope=SCOPE):
    """
    @author: Sandeepan Sengupta, Tamojit Saha
    Usage:
    from morphology import morphology as morphology
    morphology('image.tiff')
    morphology('image.tiff', 'R', 0, 5)
    """

    import cv2
    import numpy as np

    from slicer import slicer as slc
    slm = slc(file_name, channel, plane)

    kernel = np.ones((scope, scope), np.uint8)
    closing = cv2.morphologyEx(slm, cv2.MORPH_CLOSE, kernel)
    opening = cv2.morphologyEx(slm, cv2.MORPH_OPEN, kernel)

    bpm = opening | ~closing
    bpm &= 1

    return bpm

if __name__ == '__main__':
    morphology()
