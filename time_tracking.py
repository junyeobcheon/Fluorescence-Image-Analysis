from math import sqrt
from skimage import data
from skimage.feature import blob_dog, blob_log, blob_doh
from skimage.color import rgb2gray

import matplotlib.pyplot as plt

from PIL import Image
import numpy as np

import glob
from skimage.io import imread
import os

def distance(blobs1, blobs2):
    sq = np.power(( blobs1[0] - blobs2[0] ), 2) + np.power(( blobs1[1] - blobs2[1] ), 2)
    return np.sqrt(sq)

def far_enough(blobs1, blobs2):
    sq = np.power(( blobs1[0] - blobs2[0] ), 2) + np.power(( blobs1[1] - blobs2[1] ), 2)
    if distance(blobs1, blobs2) > (blobs1[2] + blobs2[2]):
        return 1
    else:
        return 0

def close_enough(blobs1, blobs2):
    if distance(blobs1, blobs2) < (blobs1[2] + blobs2[2])/4:
        return 1
    else:
        return 0

def blob_sorted(blobs_log):
    reject = []
    for i in range(len(blobs_log)):
        for j in range(i+1, len(blobs_log)):
            if far_enough(blobs_log[i], blobs_log[j]) == 0:
                reject.append(int(i))
                reject.append(int(j))

    if reject == []:
        return blobs_log
    else:

        reject1 = list(set(reject))
        reject1.sort(reverse = True)

        for loop in range(len(reject1)):
            index = reject1[loop]
            blobs_log = np.delete(blobs_log, index, 0)
        return blobs_log

def get_nearest_index(blobs0, blob_log):
    d = []
    for loop in range(len(blob_log)):
        dis = distance(blobs0, blob_log[loop])
        d.append(dis)
    min_distance = min(d)

    index = d.index(min_distance)

    return index

def get_keys(dict, val):
    list = []
    for key, value in dict.items():
        if value == val:
            list.append(key)
            return list


def reverse_dict(dic):
    reverse = {}
    for key, value in dic.items():
        reverse[value] = key

    return reverse

def get_repeated_key(dic):
    reverse = reverse_dict(dic)

    rep = [key for key, values in reverse.items() if len(values) > 1]

    return rep

def index_matching_list(mat1, mat2):
    list = []
    for mat1_index in range(len(mat1)):
        mat2_index = get_nearest_index(mat1[mat1_index], mat2)
        if close_enough(mat1[mat1_index], mat2[mat2_index]) == 1:
            list.append(mat2_index)
        elif close_enough(mat1[mat1_index], mat2[mat2_index]) == 0:
            list.append("None")

    for i in range(len(list)):
        for j in range(i+1, len(list)):
            if list[i] == list[j]:
                if list[i] == "None":
                    list[i] == "None"
                else:
                    distance_i = distance(mat1[i], mat2[list[i]])
                    distance_j = distance(mat1[j], mat2[list[j]])
                    if distance_i > distance_j:
                        list[i] = "None"
                    else:
                        list[j] = "None"
    return list

def is_there(list_input, element):
    list_s = list(set(list_input))
    bool = 0
    for loop in range(len(list_s)):
        if list_s[loop] == element:
            bool = 1

            return bool

def reappearing(mat1, mat2):
    matching_list = index_matching_list(mat1, mat2)
    matched_mat2_elements = list(set(matching_list))
    if is_there(matched_mat2_elements, "None") == 1:
        matched_mat2_elements.remove("None")
    reappearing = list(np.arange(len(mat2)))
    for element in matched_mat2_elements:
        reappearing.remove(element)

    return reappearing

def brightness(im, blob):
    y, x, r = blob

    min_bound_x = max(0, int(x-r) )
    max_bound_x = min(len(im), int(x+r+1) )
    min_bound_y = max(0, int(y-r) )
    max_bound_y = min(len(im), int(y+r+1) )

    intensity = 0

    for i in range(min_bound_x, max_bound_x):
        for j in range(min_bound_y, max_bound_y):
            sq = np.power( (i-x), 2 ) + np.power( (j-y), 2 )
            if sq < np.power(r,2):
                intensity = intensity + float(im[j][i])

    return intensity

path = './20210201poltirf_anal'
path_dir = os.listdir(path)

for dir_num in range(0,1):
# for dir_num in range(len(path_dir)):
    directory = path_dir[dir_num]
    stack = glob.glob(path + '/' +  directory + '/correction' +'/*.tif')

    im = Image.open(stack[0])
    imarray0 = np.array(im)

    fig0, ax0 = plt.subplots(1, 1)
    fig0.set_figheight(8)
    fig0.set_figwidth(8)
    max_sig = 3.4
    blobs_log0 = blob_log(imarray0, max_sigma=max_sig, num_sigma=10, threshold=50)
    blobs_log0[:, 2] = blobs_log0[:, 2] * sqrt(2)

    blobs_log0 = blob_sorted(blobs_log0)


    plt.imshow(imarray0, cmap='gray', vmin = -50, vmax = 300)
    for count in range(len(blobs_log0)):
        y, x, r = blobs_log0[count]
        ax0.text(x-1, y-5, count, color='red', fontsize=10)
        ax0.text(x-1, y, round(brightness(imarray0, blobs_log0[count])), color='forestgreen', fontsize=10)
        c = plt.Circle((x, y), r, color='red', linewidth=0.8, fill=False)
        ax0.add_patch(c)

    direc = path + '/' +  directory

    if not os.path.exists(direc + '/analysis'):
        os.makedirs(direc + '/analysis')

    plt.savefig(direc + '/analysis/' + str(directory) + '_' + str(0) + '.tif', format = "tif")
    print(str(stack[0]) + " completed")

    plt.close()

    previous_im = imarray0
    previous_blob = blobs_log0
    # ---------------------------------------------------------------------------------------------------------------------------------
    for im_num in range(1, len(stack)):
        im = Image.open(stack[im_num])
        imarray = np.array(im)

        fig, ax = plt.subplots(1, 1)
        fig.set_figheight(8)
        fig.set_figwidth(8)

        blobs_log = blob_log(imarray, max_sigma=max_sig, num_sigma=10, threshold=50)
        blobs_log[:, 2] = blobs_log[:, 2] * sqrt(2)

        blobs_log = blob_sorted(blobs_log)

        plt.imshow(imarray, cmap='gray', vmin = -50, vmax = 300)

        for count in range(len(blobs_log)):
            y, x, r = blobs_log[count]
            if is_there(reappearing(previous_blob, blobs_log), count) == 1:
                ax.text(x-1, y+5, 'new', color='dodgerblue', fontsize=10)

            else:
                now_list = index_matching_list(previous_blob, blobs_log)
                ind = now_list.index(count)
                ax.text(x-1, y+5, ind, color='dodgerblue', fontsize=10)

            ax.text(x-1, y, round(brightness(imarray, blobs_log[count])), color='forestgreen', fontsize=10)
            ax.text(x-1, y-5, count, color='red', fontsize=10)
            c = plt.Circle((x, y), r, color='red', linewidth=0.8, fill=False)
            ax.add_patch(c)

        # numrows = len(blobs_log0)
        # print("Number of blobs counted : " ,numrows)
        # numrows = len(blobs_log1)
        # print("Number of blobs counted : " ,numrows)

        # plt.tight_layout()
        # plt.show()
        direc = path + '/' +  directory
        # directory2 = 'C:/users/82108/plot/poltirf/sample/corrected2_view'

        if not os.path.exists(direc + '/analysis'):
            os.makedirs(direc + '/analysis')
        # if not os.path.exists(directory2):
        #     os.makedirs(directory2)

        # data = gaussian_filter(imarray_corrected, sigma=1)
        # im = Image.fromarray(data)
        # im.save(direc + '/correction/' + str(directory) + '_' + str(im_num) + '.tif')
        # print(str(stack[im_num]) + " completed")

        plt.savefig(direc + '/analysis/' + str(directory) + '_' + str(im_num) + '.tif', format = "tif")
        print(str(stack[im_num]) + " completed")

        plt.close()

        previous_im = imarray
        previous_blob = blobs_log
