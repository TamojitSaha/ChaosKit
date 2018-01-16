#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@author: Tanmoy Das Gupta, Sandeepan Sengupta, Tamojit Saha
"""

from configurator import configurator as cfgr
CHANNEL, PLANE, SCOPE, BUFFER = cfgr('setup.cfg')

def bitplane(image_file='image.tiff', DPI=1000, channel=CHANNEL, plane=PLANE):
    """
    Usage:
    bitplane('image.tiff', 1000)
    bitplane('image.tiff', 500, 'R', 0)
    """

    import os
    from slicer import slicer as slc
    import numpy as np
    #from matplotlib.pyplot import imsave,imshow
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm

    base = os.path.basename(image_file)

    bit_array = slc(image_file, channel, plane)
    bit_array = np.reshape(bit_array, (-1,512))
    #imshow(bit_array)
    name = os.path.splitext(base)[0]

    new_image_file = name+"_"+channel+"_"+str(plane)+".pdf"
    plt.imshow(bit_array, cmap=cm.gray)
    plt.savefig(new_image_file,format='pdf', dpi=DPI, bbox_inches='tight')
    plt.clf()
    plt.cla()
    plt.close()

if __name__ == '__main__':
    bitplane()