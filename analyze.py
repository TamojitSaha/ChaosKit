#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@author: Tanmoy Das Gupta, Sandeepan Sengupta, Tamojit Saha
"""

from configurator import configurator as cfgr
CHANNEL, PLANE, SCOPE, BUFFER = cfgr('setup.cfg')

def analyze(block, image_name='image.tiff', channel=CHANNEL, plane=PLANE, scope=SCOPE):

    """
    Test syntax
    analyze(6, 'image.tiff')
    analyze(765, 'image.tiff', 'R', 0, 5)

    """

    from morphology import morphology as mp

    stencil = mp(image_name, channel, plane, scope)
    zone = stencil.flatten()

    restrict = []

    import numpy as np
    for i in range(np.size(zone)):

        if zone[i] == 1:

            restrict.append(i)

    restrict = np.array(restrict)


    #checking available space at the beginning of array

    start = 0
    stop = restrict[0]

    address = []
    chunk = []

    if (stop - start - 1) >= block:
        address.append((start, stop))
        chunk.append(start)
        chunk.append(stop)


    #checking available space at the end of array

    edge = (np.size(zone)-1)-restrict[-1]
    if edge > restrict[0]:
        start = restrict[-1]
        stop = np.size(zone)
        address.append((start, stop))
        if stop - start > chunk[-1] - chunk[0]:
            chunk[0] = start
            chunk[-1] = stop


    #checking available block of space inside array

    for i in range(1, np.size(restrict)):
        segment = (restrict[i] - restrict[i-1]) - 1
        if segment >= block:
            start = restrict[i-1]
            stop = restrict[i]
            address.append((start, stop))
            if stop - start > chunk[-1] - chunk[0]:
                chunk[0] = start
                chunk[-1] = stop

    if address is None:
        return None
    else:
        return address, chunk

if __name__ == '__main__':
    analyze()
