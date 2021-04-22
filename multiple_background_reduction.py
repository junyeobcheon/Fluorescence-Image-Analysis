from math import sqrt
from skimage import data
from skimage.feature import blob_dog, blob_log, blob_doh
from skimage.color import rgb2gray

import matplotlib.pyplot as plt

from PIL import Image
import numpy as np

import glob
from skimage.io import imread
from scipy.ndimage import gaussian_filter

import os


crop_center = 512
crop_size = 150 #must be even
crop_x = [int(crop_center-crop_size/2), int(crop_center+crop_size/2)]
crop_y = [int(crop_center-crop_size/2), int(crop_center+crop_size/2)]

binning = 5 # odd number
bin_size = int((binning - 1 )/2)

# dark = []
# f_1 = open("dark signal" + ".csv", "r", encoding = "utf8")
# lines = f_1.readlines()
#
# for i in range(len(lines)):
#     a = lines[i].split(',')
#     b = a[-1].split('\n')
#     a.remove(a[-1])
#     a.append(b[0])
#     list = [float(l) for l in a]
#     dark.append(list)

dark = np.zeros( (1024,1024) )

directory_list = ['spol_G0_monomer', 'spol_G0_dimer', 'spol_G3_dimer', 'ppol_G0_monomer', 'ppol_G0_dimer', 'ppol_G3_dimer']

for directory_name in directory_list:

    path = './poltirf/' + directory_name
    path_dir = os.listdir(path)

    # for dir_num in range(0,2):
    for dir_num in range(len(path_dir)):
        directory = path_dir[dir_num]
        stack = glob.glob(path + '/' +  directory + '/*.tif')


        for im_num in range(len(stack)):
            im = Image.open(stack[im_num])
            imarray1 = np.array(im)
            imarray_dark_sub_uncrop = np.subtract(imarray1, dark)
            imarray_dark_sub = []
            inter = imarray_dark_sub_uncrop[crop_x[0]:crop_x[1]]


            for loop in range(0, crop_y[1]-crop_y[0]):
                inter2 = inter[loop][crop_y[0]:crop_y[1]]
                imarray_dark_sub.append(inter2)

            imarray_max = np.zeros((  len(imarray_dark_sub), len(imarray_dark_sub)  ))
            imarray_avg = np.zeros((  len(imarray_dark_sub), len(imarray_dark_sub)  ))
            imarray_cor_avg = np.zeros((  len(imarray_dark_sub), len(imarray_dark_sub)  ))

            num_bin = int( len(imarray_dark_sub)/binning )

            for i in range(bin_size, len(imarray_dark_sub)-bin_size):
                bin1 = imarray_dark_sub[i-bin_size:i+bin_size+1]
                for j in range(bin_size, len(imarray_dark_sub)-bin_size):
                    bin = []
                    for loop in range(binning):
                        bin2 = bin1[loop][j-bin_size:j+bin_size+1]
                        bin.append(bin2)
                    bin_list = np.array(bin).reshape(1,-1)[0]
                    bin_sum = sum(bin_list)
                    bin_avg = bin_sum / len(bin_list)
                    # bin_max = max(bin_list)

                    # imarray_max[i][j] = bin_max
                    imarray_avg[i][j] = bin_avg
                #     if j == 1:
                #         break
                # if i == 1:
                #     break
            # print(bin_max)
            # print(bin_avg)
            # print(bin_list)
            sig = 15
            imarray_corrected = np.subtract(imarray_dark_sub, gaussian_filter(imarray_avg, sigma=sig))

            file_name = stack[im_num].split('_')
            numbering = file_name[-1]

            direc = path + '/' +  directory
            # directory2 = 'C:/users/82108/plot/poltirf/sample/corrected2_view'

            if not os.path.exists(direc + '/correction'):
                os.makedirs(direc + '/correction')
            # if not os.path.exists(directory2):
            #     os.makedirs(directory2)

            data = gaussian_filter(imarray_corrected, sigma=1)
            im = Image.fromarray(data)
            im.save(direc + '/correction/' + str(directory) + '_' + str(numbering) + '.tif')
            print(str(stack[im_num]) + " completed")

            plt.close()
