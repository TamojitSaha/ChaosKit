import os
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.cm as cm
from matplotlib.pyplot import imsave,imshow

'''
#..........................Sample Usage.................................#

Copy this....
neighborhood('image.tiff','8', 10000)
neighborhood('image_encoded.tiff','8', 10000)

#.......................................................................#
'''

def Entropy(signal):
        '''
        function returns entropy of a signal
        signal must be a 1-D numpy array
        '''
        lensig=signal.size
        symset=list(set(signal))
        #numsym=len(symset)
        propab=[np.size(signal[signal==i])/(1.0*lensig) for i in symset]
        ent=np.sum([p*np.log2(1.0/p) for p in propab])
        return ent

def neighborhood(file_name, neighborhood, DPI):
        """
        neighborhood('image.tiff','8', 10000)
        neighborhood('image_encoded.tiff','8', 10000)
        """
        with Image.open(file_name) as img:
            width, height = img.size

        base = os.path.basename(file_name)
        name = os.path.splitext(base)[0]
        #ext = os.path.splitext(base)[1]

        colorIm=Image.open(file_name)
        width, height = colorIm.size
        greyIm=colorIm.convert('L')
        colorIm=np.array(colorIm)
        greyIm=np.array(greyIm)
        neighborhood = min(abs(int(neighborhood))*2, width, height)/2
        if neighborhood%2 !=0:
            neighborhood +=1
        N = neighborhood/2
        S=greyIm.shape
        E=np.array(greyIm)
        for row in range(S[0]):
                for col in range(S[1]):
                        Lx=np.max([0,col-N])
                        Ux=np.min([S[1],col+N])
                        Ly=np.max([0,row-N])
                        Uy=np.min([S[0],row+N])
                        region=greyIm[Ly:Uy,Lx:Ux].flatten()
                        E[row,col]=Entropy(region)

        plt.imshow(E, cmap=plt.cm.jet)
        #plt.xlabel(image_caption)

#        figure = plt.gcf() # get current figure
#        figure.set_size_inches(image_height, image_width)#in inches
        # when saving, specify the DPI
        new_file_name = name+"_entropy_"+str(neighborhood)+"x"+str(neighborhood)+".pdf"
        plt.savefig(new_file_name, format='pdf', dpi = DPI, bbox_inches='tight')
        plt.clf()
        plt.cla()
        plt.close()
        return E
