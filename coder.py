#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@author: Tanmoy Das Gupta, Sandeepan Sengupta, Tamojit Saha
"""

from numpy import zeros

def hide(msg_file='msg.txt'):
    """
    Test usage:
    hide(file_name.txt)
    """

    from binascii import hexlify

    information = open(msg_file,'r').read()

    data = hexlify(information)
    #print data
    temp = zeros(len(data)).astype('str')

    for i in range(len(data)):
        temp[i] = data[i]

    for j in range(len(temp)):
        if temp[j] == '0': temp[j] = '0000'
        if temp[j] == '1': temp[j] = '0001'
        if temp[j] == '2': temp[j] = '0010'
        if temp[j] == '3': temp[j] = '0011'
        if temp[j] == '4': temp[j] = '0100'
        if temp[j] == '5': temp[j] = '0101'
        if temp[j] == '6': temp[j] = '0110'
        if temp[j] == '7': temp[j] = '0111'
        if temp[j] == '8': temp[j] = '1000'
        if temp[j] == '9': temp[j] = '1001'
        if temp[j] == 'a': temp[j] = '1010'
        if temp[j] == 'b': temp[j] = '1011'
        if temp[j] == 'c': temp[j] = '1100'
        if temp[j] == 'd': temp[j] = '1101'
        if temp[j] == 'e': temp[j] = '1110'
        if temp[j] == 'f': temp[j] = '1111'

    encoded_output = zeros(4*len(temp)).astype('uint8')
    for i in range(len(temp)):
        for j in range(4):
            encoded_output[4*i+j] = temp[i][j]

    encoded_output = encoded_output.flatten()
    return encoded_output

def unhide(bindata):
    """
    Test usage:
    unhide(1D numpy array)
    """

    from binascii import unhexlify

    bin_data = bindata
    data = zeros(len(bin_data)/4).astype('str')

    for i in range(len(bin_data)/4):
        data[i] = 1000*bin_data[4*i]+100*bin_data[4*i+1]+10*bin_data[4*i+2]+bin_data[4*i+3]

    for j in range(len(data)):
        if data[j] == '0'   : data[j] = '0'
        if data[j] == '1'   : data[j] = '1'
        if data[j] == '10'  : data[j] = '2'
        if data[j] == '11'  : data[j] = '3'
        if data[j] == '100' : data[j] = '4'
        if data[j] == '101' : data[j] = '5'
        if data[j] == '110' : data[j] = '6'
        if data[j] == '111' : data[j] = '7'
        if data[j] == '1000': data[j] = '8'
        if data[j] == '1001': data[j] = '9'
        if data[j] == '1010': data[j] = 'a'
        if data[j] == '1011': data[j] = 'b'
        if data[j] == '1100': data[j] = 'c'
        if data[j] == '1101': data[j] = 'd'
        if data[j] == '1110': data[j] = 'e'
        if data[j] == '1111': data[j] = 'f'

    hex_string = ''

    for j in range(len(data)):
        hex_string = hex_string + data[j]

    output_information = unhexlify(hex_string)
    return output_information