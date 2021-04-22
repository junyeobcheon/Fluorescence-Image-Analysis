from math import sqrt
from skimage.feature import blob_dog, blob_log, blob_doh

import matplotlib.pyplot as plt

from PIL import Image
import numpy as np

import glob
from skimage.io import imread
import os
import sys

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

def line_generator(list):
    line = ""
    for loop in range(len(list)):
        line = line + str(list[loop]) + ","
    line = line + "\n"

    return line

threshold = 100
num_sigma = 8
max_sigma = 2.4

cut_up = 100
cut_down = 3
cut_radius = 1.5

directory_list = ['spol_G0_monomer', 'spol_G0_dimer', 'spol_G3_dimer', 'ppol_G0_monomer', 'ppol_G0_dimer', 'ppol_G3_dimer']

for directory_name in directory_list:
    path = './poltirf/time trace mat' + directory_name
    path1 = path + '/data with cut from ' + str(cut_down) + ' and ' + str(cut_up)
    path_dir = os.listdir(path)

    # for dir_num in range(0,1):
    for dir_num in range(len(path_dir)):
        directory = path_dir[dir_num]
        stack = glob.glob(path + '/' +  directory + '/correction' +'/*.tif')

        stack_ini = len(stack) - 1
        for loop in range(len(stack)):
            im = Image.open(stack[loop])
            imarray0 = np.array(im)

            blobs_log0 = blob_log(imarray0, max_sigma=max_sigma, num_sigma=num_sigma, threshold=threshold)
            blobs_log0[:, 2] = blobs_log0[:, 2] * sqrt(2)
            blobs_log0 = blob_sorted(blobs_log0)

            if len(blobs_log0) < cut_up:
                if len(blobs_log0) > cut_down:
                    stack_ini = loop
                    break


        # print(stack_ini - 1)
        im0 = Image.open(stack[stack_ini])
        imarray0 = np.array(im0)

        blobs_log0 = blob_log(imarray0, max_sigma=max_sigma, num_sigma=num_sigma, threshold=threshold)
        blobs_log0[:, 2] = blobs_log0[:, 2] * sqrt(2)
        blobs_log0 = blob_sorted(blobs_log0)

        previous_im = imarray0
        previous_blob = blobs_log0

        direc = path1 + '/' + directory
        if not os.path.exists(direc):
            os.makedirs(direc)

        f1 = open(direc + '/' + str(directory) + " matching" + ".csv", "w", encoding = "utf8")
        f2 = open(direc + '/' + str(directory) + " reappearing" + ".csv", "w", encoding = "utf8")
        f3 = open(direc + '/' + str(directory) + " intensity" + ".csv", "w", encoding = "utf8")
        f4 = open(direc + '/' + str(directory) + " radius" + ".csv", "w", encoding = "utf8")

        for loop in range(stack_ini, len(stack)):
            intensity = []
            radius = []
            im = Image.open(stack[loop])
            imarray = np.array(im)

            blobs_log = blob_log(imarray, max_sigma=max_sigma, num_sigma=num_sigma, threshold=threshold)
            blobs_log[:, 2] = blobs_log[:, 2] * sqrt(2)

            blobs_log = blob_sorted(blobs_log)

            if len(blobs_log) == 0:
                new = []
                matching = []
                for i in range(len(previous_blob)):
                    matching.append("None")
            else:
                for blob_num in range(len(blobs_log)):
                    intensity.append(float(brightness(imarray, blobs_log[blob_num])))
                for blob_num in range(len(blobs_log)):
                    radius.append(float(blobs_log[blob_num][2]))

                new = reappearing(previous_blob, blobs_log)
                matching = index_matching_list(previous_blob, blobs_log)

            f1.write(line_generator(matching))
            f2.write(line_generator(new))
            f3.write(line_generator(intensity))
            f4.write(line_generator(radius))
            previous_im = imarray
            previous_blob = blobs_log
        print(directory, ' done')
    f1.close()
    f2.close()
    f3.close()
    f4.close()
