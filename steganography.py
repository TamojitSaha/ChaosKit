#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@author: Tanmoy Das Gupta, Sandeepan Sengupta, Tamojit Saha
"""

import os
import numpy as np

from matplotlib.pyplot import imread, imsave

setup_file = 'setup.cfg'
from configurator import configurator as cfgr
CHANNEL, PLANE, SCOPE, BUFFER = cfgr(setup_file)

MSG_FILE = 'msg.txt'
IMAGE_FILE = 'image.tiff'

#==============================================================================
# Channel Auto-Selection Module
#==============================================================================
def validate(msg_file=MSG_FILE, image_file=IMAGE_FILE, channel=CHANNEL):
    from coder import hide
    msg_bin = hide(msg_file)
    msg_length = len(msg_bin)

    from entropy import ENTROPY

    from analyze import analyze
    address_r, chunk_r = analyze(msg_length, 'image.tiff', 'R')
    address_g, chunk_g = analyze(msg_length, 'image.tiff', 'G')
    address_b, chunk_b = analyze(msg_length, 'image.tiff', 'B')

    entropies = []
    restrict = []
    if np.size(chunk_r) > 0:
        if chunk_r[-1]-chunk_r[0] >= msg_length:
            entropies.append(ENTROPY(imread(image_file))[0])
        else:
            entropies.append(0)
            restrict.append('R')
    else:
        entropies.append(0)
        restrict.append('R')

    if np.size(chunk_g) > 0:
        if chunk_g[-1]-chunk_g[0] >= msg_length:
            entropies.append(ENTROPY(imread(image_file))[1])
        else:
            entropies.append(0)
            restrict.append('G')
    else:
        entropies.append(0)
        restrict.append('G')

    if np.size(chunk_b) > 0:
        if chunk_b[-1]-chunk_b[0] >= msg_length:
            entropies.append(ENTROPY(imread(image_file))[2])
        else:
            entropies.append(0)
            restrict.append('B')
    else:
        entropies.append(0)
        restrict.append('B')

    CHANNEL = np.argmax(entropies)
    if CHANNEL == 0:
        CHANNEL = 'R'
    elif CHANNEL == 1:
        CHANNEL = 'G'
    elif CHANNEL == 2:
        CHANNEL = 'B'

    if np.size(restrict) == 3:
        return None
    elif channel in restrict:
#        print '\n\nNOTE =>> Channel switched to '+CHANNEL+'\n\n'                          #Notice<=
        return CHANNEL
    else:
        return channel
#==============================================================================


def maker(image, channel, plane, bitplane):
    from numpy import uint8, zeros_like, bitwise_and

    bitplane_array = np.reshape(bitplane, (-1, 512))
    bitplane_array = bitplane_array*pow(2, plane)       #correction required <=

    image_data = 0

    if channel == 'R':
        image_data = image[:, :, 0]
    elif channel == 'G':
        image_data = image[:, :, 1]
    elif channel == 'B':
        image_data = image[:, :, 2]

    bitplane_all = zeros_like(image_data, dtype=uint8)
    bitplane_all[:] = 255 - pow(2, plane)               #correction required <=
    image_bitplane_cleared = bitwise_and(image_data, bitplane_all)

    if channel == 'R':
        image_r = image_bitplane_cleared[:, :] + bitplane_array
        image_g = image[:, :, 1]
        image_b = image[:, :, 2]

    elif channel == 'G':
        image_r = image[:, :, 0]
        image_g = image_bitplane_cleared[:, :] + bitplane_array
        image_b = image[:, :, 2]

    elif channel == 'B':
        image_r = image[:, :, 0]
        image_g = image[:, :, 1]
        image_b = image_bitplane_cleared[:, :] + bitplane_array

    output_image = zeros_like(image, dtype=uint8)

    output_image[:, :, 0] = image_r
    output_image[:, :, 1] = image_g
    output_image[:, :, 2] = image_b
    output_image[:, :, 3] = 255

    return output_image

def embed(msg_file=MSG_FILE, password=[-1, 2.01, 3], image_file=IMAGE_FILE, channel=CHANNEL, plane=PLANE, scope=SCOPE, ID=BUFFER):
    """
    Test usage:

    embed('msg.txt', [-1, 2.01, 3], 'image.tiff')
    embed('msg.txt', [-1, 2.01, 3], 'image.tiff', 'R', 0, 5, 64)
    """

#==============================================================================
#   Filtering inputs
#==============================================================================
    try:
        open(image_file) and open(msg_file)
    except IOError:
        return None
    except AttributeError:
        return None

    try:
        float(password[0])
    except TypeError:
        return None
    except ValueError:
        return None
    except AttributeError:
        return None

    if channel == 'r' or channel == 'R' or channel == '0' or channel == 0:
        channel = 'R'
    elif channel == 'g' or channel == 'G' or channel == '1' or channel == 1:
        channel = 'G'
    elif channel == 'b' or channel == 'B' or channel == '2' or channel == 2:
        channel = 'B'
    else:
        channel = 'R'            #Set channel to RED in case of incorrect input

    try:
        plane = abs(int(plane))
        if plane > 7:
            plane = 7
    except ValueError:
        return None

    try:
        ID = abs(int(ID))
        if ID < 4:
            ID = 4
        if ID%4 != 0:
            ID = 4*(1+ID/4)
    except ValueError:
        return None

    try:
        scope = abs(int(scope))
        if scope%2 == 0:
            scope += 1
        if scope > 9:
            scope = 9
    except ValueError:
        return None

    try:
        imread(image_file)
        try:
            imread(msg_file)
            return None
        except IOError:
            image = imread(image_file)
    except IOError:
        try:
            image = imread(msg_file)
            image_file, msg_file = msg_file, image_file
        except IOError:
            return None
#==============================================================================

    channel=validate(msg_file, image_file, channel)#Switch to optimum channel<=
    if channel is None:
        return None
    elif channel != CHANNEL:
#        print 'Replace ``Channel`` value in ``setup_file`` with '+channel
        from configurator import reconfigure as rcfg
        rcfg(setup_file, 'Channel', channel) #filename, Keyword, newValue
#        CHANNEL = channel   #Updating value for cross function use: Not Working

    from numpy import shape
    rows, columns, channels = shape(image)

    from cryptography import encrypt
    encrypted_bitplane = encrypt(image_file, msg_file, password, channel, plane, scope, ID)
    if np.size(encrypted_bitplane) == rows*columns:

        output_image = maker(image, channel, plane, encrypted_bitplane)

        base = os.path.basename(image_file)
        name = os.path.splitext(base)[0]
        ext = os.path.splitext(base)[1]
        new_image_file = name+"_encoded"+ext
        imsave(new_image_file, output_image, format='tiff')
    else:
        return None


def decipher(password=[-1, 2.01, 3], image_file='image_encoded.tiff', channel=CHANNEL, plane=PLANE, ID=BUFFER):
    """
    Test usage:

    decipher([-1, 2.01, 3], 'image_encoded.tiff')
    decipher([-1, 2.01, 3], 'image_encoded.tiff', 'R', 0, 64)
    """

#==============================================================================
#   Filtering inputs
#==============================================================================
    try:
        imread(image_file)
    except IOError:
        return None
    except AttributeError:
        return None

    try:
        float(password[0])
    except TypeError:
        return None
    except ValueError:
        return None
    except AttributeError:
        return None

    if channel == 'r' or channel == 'R' or channel == '0' or channel == 0:
        channel = 'R'
    elif channel == 'g' or channel == 'G' or channel == '1' or channel == 1:
        channel = 'G'
    elif channel == 'b' or channel == 'B' or channel == '2' or channel == 2:
        channel = 'B'
    else:
        channel = 'R'            #Set channel to RED in case of incorrect input

    try:
        plane = abs(int(plane))
        if plane > 7:
            plane = 7
    except ValueError:
        return None

    try:
        ID = abs(int(ID))
        if ID < 4:
            ID = 4
        if ID%4 != 0:
            ID = 4*(1+ID/4)
    except ValueError:
        return None
#==============================================================================

    from cryptography import decrypt
    msg = decrypt(image_file, password, channel, plane, ID)
    if msg != None:
        name = os.path.splitext(os.path.basename(image_file))[0]
        with open(name+"_deciphered.txt", "wb") as FILE:
            FILE.write(msg)
        return msg
    else:
        return None

if __name__ == '__main__':
    embed()
#    decipher()
