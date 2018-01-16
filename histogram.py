#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@author: Tanmoy Das Gupta, Sandeepan Sengupta, Tamojit Saha
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as path

def histogram(file_name, scale, DPI):
    """
    histogram('image.tiff', 5, 1000)
    histogram('image_encoded.tiff', 5, 1000)
    """
    fig = plt.figure()
    yscale = scale # to adjust the vertical axes
    # histogram our data with numpy

    dat = plt.imread(file_name)
    base = os.path.basename(file_name)
    name = os.path.splitext(base)[0]

    data = dat[:,:,0].reshape(-1,1)
    n, bins = np.histogram(data, 256)

    # get the corners of the rectangles for the histogram
    left = np.array(bins[:-1])
    right = np.array(bins[1:])
    bottom = np.zeros(len(left))
    top = bottom + n


    # we need a (numrects x numsides x 2) numpy array for the path helper
    # function to build a compound path
    XY = np.array([[left,left,right,right], [bottom,top,top,bottom]]).T

    # get the Path object
    barpath = path.Path.make_compound_path_from_polys(XY)

    ax1 = fig.add_subplot(311)
    # make a patch out of it
    patch = patches.PathPatch(barpath, facecolor='red', edgecolor='red', alpha=0.8)
    ax1.add_patch(patch)
    for label in ax1.get_xticklabels():
        label.set_visible(False)
    ax1.locator_params(axis='y', nbins=4)

    # update the view limits
    ax1.set_xlim(0, 255)
    ax1.set_ylim(bottom.min(), top.max()//yscale)
    plt.grid()

    data = dat[:,:,1].reshape(-1,1)
    n, bins = np.histogram(data, 256)

    # get the corners of the rectangles for the histogram
    left = np.array(bins[:-1])
    right = np.array(bins[1:])
    bottom = np.zeros(len(left))
    top = bottom + n


    # we need a (numrects x numsides x 2) numpy array for the path helper
    # function to build a compound path
    XY = np.array([[left,left,right,right], [bottom,top,top,bottom]]).T

    # get the Path object
    barpath = path.Path.make_compound_path_from_polys(XY)

    ax2 = fig.add_subplot(312, sharex=ax1)
    # make a patch out of it
    patch = patches.PathPatch(barpath, facecolor='green', edgecolor='green', alpha=0.8)
    ax2.add_patch(patch)
    for label in ax2.get_xticklabels():
        label.set_visible(False)
    ax2.locator_params(axis='y', nbins=4)
    # update the view limits
    ax2.set_xlim(0, 255)
    ax2.set_ylim(bottom.min(), top.max()//yscale)
    plt.grid()
    plt.ylabel('number of pixels')

    data = dat[:,:,2].reshape(-1,1)
    n, bins = np.histogram(data, 256)

    # get the corners of the rectangles for the histogram
    left = np.array(bins[:-1])
    right = np.array(bins[1:])
    bottom = np.zeros(len(left))
    top = bottom + n


    # we need a (numrects x numsides x 2) numpy array for the path helper
    # function to build a compound path
    XY = np.array([[left,left,right,right], [bottom,top,top,bottom]]).T

    # get the Path object
    barpath = path.Path.make_compound_path_from_polys(XY)

    ax3 = fig.add_subplot(313, sharex=ax1)
    # make a patch out of it
    patch = patches.PathPatch(barpath, facecolor='blue', edgecolor='blue', alpha=0.8)
    ax3.add_patch(patch)
    ax3.locator_params(axis='y', nbins=4)


    # update the view limits
    ax3.set_xlim(0, 255)
    ax3.set_ylim(bottom.min(), top.max()//yscale)
    #axis([0, 255])
    plt.grid()
    plt.xlabel('intensity')

    new_file_name = name+"_histogram"+".pdf"
#    print "\nThe filename is: "+new_file_name
    plt.savefig(new_file_name, format="pdf", dpi = DPI, bbox_inches='tight')
    plt.clf()
    plt.cla()
    plt.close()
