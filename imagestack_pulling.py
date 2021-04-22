from math import sqrt
from skimage import data
from skimage.feature import blob_dog, blob_log, blob_doh
from skimage.color import rgb2gray
import skimage.io as skio
import matplotlib.pyplot as plt

from PIL import Image
import numpy as np

import glob
from skimage.io import imread
from scipy.ndimage import gaussian_filter
import os

def serial_genertor(number):
    first = number//1000
    second = number//100 - 10*first
    third = number//10 - 100*first - 10*second
    fourth = number%10

    return str(first) + str(second) + str(third) + str(fourth)

directory_list = ['spol_G0_monomer', 'spol_G0_dimer', 'spol_G3_dimer', 'ppol_G0_monomer', 'ppol_G0_dimer', 'ppol_G3_dimer']

for directory_name in directory_list:

    path = './poltirf/' + directory_name
    path_dir = os.listdir(path)

    for dir_num in range(0, len(path_dir)):
    # for dir_num in range(len(path_dir)):
        directory = path_dir[dir_num]
        stack = glob.glob(path + '/' +  directory + '/*.tif')
        print(stack[0])
        im = skio.imread(stack[0])
        imarray = np.array(im)

        for i in range(len(imarray)):
            data = np.array(imarray[i])
            im = Image.fromarray(data)
            im.save(path + '/' +  directory + '/' +  directory + '_' + serial_genertor(i) + '.tif')

        os.remove(stack[0])
