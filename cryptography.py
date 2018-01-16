#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@author: Tanmoy Das Gupta, Sandeepan Sengupta, Tamojit Saha
"""

from numpy import uint8

from configurator import configurator as cfgr
CHANNEL, PLANE, SCOPE, BUFFER = cfgr('setup.cfg')
SIGMA, BETA, RHO, DT = cfgr('chaos.cfg')

def salt(key, space):
    """
    Test usage:
    salt(initial position of a chaotic system in Cartesian, no. of output bits)
    salt([1, 0.2, -3], 64)
    """
    if space < 0:
        return None
    from numpy import zeros, remainder
    dt = DT

    xs = zeros((space + 1,))
    ys = zeros((space + 1,))
    zs = zeros((space + 1,))

    xs[0], ys[0], zs[0] = key[0], key[1], key[2]

    for i in xrange(space) :

        from chaos import lorenz as chaos
        x_dot, y_dot, z_dot = chaos(xs[i], ys[i], zs[i])
        xs[i + 1] = xs[i] + (x_dot * dt)
        ys[i + 1] = ys[i] + (y_dot * dt)
        zs[i + 1] = zs[i] + (z_dot * dt)

    Xs =  remainder(abs(xs*10**14), 2).astype(uint8)
    Ys =  remainder(abs(ys*10**14), 2).astype(uint8)
    Zs =  remainder(abs(zs*10**14), 2).astype(uint8)
    salty_bits = Xs ^ Ys ^ Zs
    return salty_bits


from slicer import slicer as slc
from scanner import scanner as scn
from entropy import ENTROPY

def encrypt(image_file='image.tiff', msg_file='msg.txt', password=[-1, 2.01, 3], channel=CHANNEL, plane=PLANE, scope=SCOPE, ID=BUFFER):
    """
    Test usage:
    encrypt('image.tiff', 'msg.txt', [-1, 2.01, 3])
    encrypt('image.tiff', 'msg.txt', [-1, 2.01, 3], 'R', 0, 5, 64)
    """

    bitplane_array = slc(image_file, channel, plane)

    bitplane_flatten = bitplane_array.flatten().astype(uint8)

    import numpy as np
    if ID >= np.size(bitplane_flatten):
        return None

    from coder import hide
    msg_bin = hide(msg_file)
    msg_length = len(msg_bin)

    null_values = 0
    if msg_length%ID != 0:
        null_values =ID*(1 + msg_length/ID) - msg_length
        msg_length += null_values

    marker = salt(password, ID-1)[::-1]                 #reversing bit sequence
    if marker is None:
        return None

#==============================================================================
#   deweeding unit
#==============================================================================
    weed = scn(bitplane_flatten, marker)
    if weed != None:

        for i in range(np.size(weed)):
            spot = weed[i]
            if bitplane_flatten[spot] == 0:
                bitplane_flatten[spot] = 1
            elif bitplane_flatten[spot] == 1:
                bitplane_flatten[spot] = 0
#==============================================================================

    channel_code = None
    from matplotlib.pyplot import imread
    if channel == 'R':
        channel_code = 0
    elif channel == 'G':
        channel_code = 1
    elif channel == 'B':
        channel_code = 0
    baseline = ENTROPY(imread(image_file))[channel_code]
#    baseline = Entropy(bitplane_flatten)

    msg_length += 2*ID                      #Calculating minimum space required

    from analyze import analyze
    address, block = analyze(msg_length, image_file, channel, plane, scope)

    start, stop = 0, 0
    if address is None:
        return None
    elif np.size(address) == 1:
        start, stop = address[0]
    else:

#==============================================================================
#Simulate all possible successful encoding event and compare respective entropy
#==============================================================================
        deviation = []
        for i in range(np.size(address)/2):                          #Trial run

            import copy
            test_bitplane = copy.deepcopy(bitplane_flatten)  #original bitplane
            MSG_BIN = copy.deepcopy(msg_bin)
            START, STOP = address[i]
            if np.size(test_bitplane) - STOP > START:   #detecting middle range
                START=ID*(START/ID)                  #rounding up start address
                STOP=ID*(1+(STOP/ID))                 #rounding up stop address
            else:
                START=ID*((START/ID)-1)              #rounding up start address
                STOP=ID*(STOP/ID)                     #rounding up stop address

            if STOP - START <= 0:
                return None

            if len(MSG_BIN)%ID != 0:
                MSG_LENGTH = ID*(1+len(MSG_BIN)/ID)         #rounding up length

            for i in range(MSG_LENGTH - len(MSG_BIN)):
                MSG_BIN = np.insert(MSG_BIN, 0, 0) #ading ZERO bits for padding

            if salt(password, ID + MSG_LENGTH - 1) is None:
                return None
            CIPHER = MSG_BIN ^ salt(password, ID + MSG_LENGTH - 1)[-MSG_LENGTH:]
            CIPHER = np.concatenate((CIPHER, marker), axis=0)
            CIPHER = np.concatenate((marker, CIPHER), axis=0)

            if np.size(test_bitplane) - STOP > START:   #detecting middle range
                START = STOP - np.size(CIPHER)
            else:
                STOP = START + np.size(CIPHER)

            for i in range(STOP - START):
                test_bitplane[START+i] = CIPHER[i]

            image = imread(image_file)
            from steganography import maker
            test_image = maker(image, channel, plane, test_bitplane)
            Current_Entropy = ENTROPY(test_image)[channel_code]
            deviation.append(abs(baseline - Current_Entropy))
#            deviation.append(abs(baseline-Entropy(test_bitplane)))
#==============================================================================

        index = np.argmin(deviation)
        start, stop = address[index]

#==============================================================================
#         import random
#         from datetime import datetime
#         random.seed(datetime.now())
#
#         start, stop = random.choice(address)
#==============================================================================

    if np.size(bitplane_flatten) - stop > start:        #detecting middle range
        start=ID*(start/ID)                          #rounding up start address
        stop=ID*(1+(stop/ID))                         #rounding up stop address
    else:
        start=ID*((start/ID)-1)                      #rounding up start address
        stop=ID*(stop/ID)                             #rounding up stop address

    if stop - start <= 0:
        return None

    if len(msg_bin)%ID != 0:
        msg_length = ID*(1+len(msg_bin)/ID)                 #rounding up length

    for i in range(msg_length - len(msg_bin)):
        msg_bin = np.insert(msg_bin, 0, 0)         #ading ZERO bits for padding

    if salt(password, ID + msg_length - 1) is None:
        return None
    cipher = msg_bin ^ salt(password, ID + msg_length - 1)[-msg_length:]
    cipher = np.concatenate((cipher, marker), axis=0)
    cipher = np.concatenate((marker, cipher), axis=0)

    if np.size(bitplane_flatten) - stop > start:        #detecting middle range
        start = stop - np.size(cipher)
    else:
        stop = start + np.size(cipher)

    for i in range(stop - start):
        bitplane_flatten[start+i] = cipher[i]

    return bitplane_flatten


def decrypt(image_file='image_encoded.tiff', password=[-1, 2.01, 3], channel=CHANNEL, plane=PLANE, ID=BUFFER):
    """
    Test usage:
    decrypt('image.tiff', [-1, 2.01, 3])
    decrypt('image.tiff', [-1, 2.01, 3], 'R', 0, 5, 64)
    """

    bitplane_encoded = slc(image_file, channel, plane).flatten().astype(uint8)
    identifier = salt(password, ID-1)[::-1]             #reversing bit sequence
    if identifier is None:
        return None

    location = scn(bitplane_encoded, identifier)
    if location != None:
        zone = location[-1] - location[0] - ID

        encrypted_msg = []
        for i in range(zone):
            encrypted_msg.append(bitplane_encoded[location[0]+ID+i])

        if salt(password, zone-1) is None:
            return None
        decrypted_msg = encrypted_msg ^ salt(password, ID+zone-1)[-zone:]

        from coder import unhide
        msg = unhide(decrypted_msg)
        msg = msg.replace('\x00','')
        return msg
    else:
        return None
