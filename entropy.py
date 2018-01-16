import os
import numpy as np
from matplotlib.pyplot import imread

#def Entropy(text):
#    import math
#    log2=lambda x:math.log(x)/math.log(2)
#    exr={}
#    infoc=0
#    for each in text:
#        try:
#            exr[each]+=1
#        except:
#            exr[each]=1
#    textlen=len(text)
#    for k,v in exr.items():
#        freq  =  1.0*v/textlen
#        infoc+=freq*log2(freq)
#    infoc*=-1
#    return infoc

def entropy(image_name):
    """Calculate the Shannon entropy of an image.
    The Shannon entropy is defined as S = -sum(pk * log(pk)),
    where pk are the number of pixels of value k.
    
    Parameters
    ----------
    image_name : string
        Grayscale or Colour input image.
        
    Returns
    -------
    entropy : list
        If the input image is a colour image, it returns a list with the
        entropies of the individual channels.
        
    Examples
    --------
    >>> from image_entropy import entropy
    >>> entropy('image.tiff')
    """

    entropies = ENTROPY(imread(image_name))

    file_name = os.path.basename(image_name)
    name = os.path.splitext(file_name)[0]

    f=open(name+'_entropies.txt', 'w')
    f.writelines(file_name+" "+str(entropies))
    f.close()

def ENTROPY(image_data):
    """Calculate the Shannon entropy of an image.
    The Shannon entropy is defined as S = -sum(pk * log(pk)),
    where pk are the number of pixels of value k.
    
    Parameters
    ----------
    image_data : Array
        Numpy array.
        
    Returns
    -------
    entropy : list
        If the input image is a colour image, it returns a list with the
        entropies of the individual channels.
        
    Examples
    --------
    >>> from image_entropy import entropy
    >>> entropy('image.tiff')
    """

    rows, cols, channels = np.shape(image_data)
    num_pixels = rows * cols

    if channels == 4:
        channels = 3  # discard the alpha channel

    entropies = []

    # using the Shannon's formula for calculating the entropy
    # https://en.wiktionary.org/wiki/Shannon_entropy

    for channel in range(channels):
        channel_pixels, _ = np.histogram(image_data[:, :, channel].reshape(-1, 1), 256)
        channel_probability = channel_pixels*1.0 / num_pixels

        # if the number of pixels for a certain intensity is 0, replace it by 1
        # this avoids floating point exceptions in the log2 function
        channel_probability[channel_probability == 0] = 1

        channel_entropy = -np.sum(channel_probability * np.log2(channel_probability))
        entropies.append(channel_entropy)
    
    return (entropies)
