#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@author: Tanmoy Das Gupta, Sandeepan Sengupta, Tamojit Saha
"""

import os
import matplotlib.pyplot as plt
from matplotlib.pyplot import imread

def autocorrelation(file_name,DPI):
    """
    autocorrelation('image.tiff')
    autocorrelation('image_encoded.tiff')
    """
    data = imread(file_name)
    base = os.path.basename(file_name)
    name = os.path.splitext(base)[0]


    for i in range(0,512,128):
        plt.plot(data[:,i,0], data[:,i+1,0],'r+')
        plt.plot(data[:,i,2], data[:,i+1,2],'b+')
        plt.plot(data[:,i,1], data[:,i+1,1],'g+')

    plt.axis('tight')
    plt.grid()
    plt.xlabel('Pixel intensity')
    plt.ylabel('Intensity of adjacent pixel')
    new_file_name = name+"_autocorrelation"+".pdf"
#    print "\nThe filename is: "+new_file_name
    plt.savefig(new_file_name, dpi=DPI, format="pdf",bbox_inches='tight')
    plt.clf()
    plt.cla()
    plt.close()