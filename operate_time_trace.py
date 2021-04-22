from math import sqrt
from skimage.feature import blob_dog, blob_log, blob_doh

import matplotlib.pyplot as plt

from PIL import Image
import numpy as np

import glob
from skimage.io import imread
import os
from scipy.special import factorial
from scipy.optimize import curve_fit

def is_empty(list):
    if len(list) == 0:
        bool = 1
    else:
        bool = 0
    return bool

def is_there(list_input, element):
    list_s = list(set(list_input))
    bool = 0
    for loop in range(len(list_s)):
        if list_s[loop] == element:
            bool = 1

            return bool

def line_generator(list_input):
    line = ""
    for loop in range(len(list_input)):
        line = line + ", " + str(list_input[loop])
    line = line + "\n"

    return line

def gaussian(x, a, b, c):
    exponent =  -(x-b)*(x-b) / c/c / 2

    return a*np.exp(exponent)

def poissonian(x, a, b):
    return a*(b**x/factorial(x)) * np.exp(-b)


def bin_generator(bin_list):
    list = []
    for loop in range(0, len(bin_list) - 1):
        center = (bin_list[loop] + bin_list[loop + 1]) / 2
        list.append(center)

    return list
# spol , ppol 순서대로 !
directory_list = ['spol_G0_monomer', 'spol_G0_dimer', 'spol_G3_dimer', 'ppol_G0_monomer', 'ppol_G0_dimer', 'ppol_G3_dimer']

f_hist = open("./histogram_poltirf.csv", "w", encoding = "utf8")

for directory_name in directory_list:

    path = './poltirf/' + directory_name + '/data with cut100 and 3'

    path_dir = os.listdir(path)

    hist_radius_mat = []
    hist_intensity_mat = []
    hist_avg_intensity = []
    # 11, 14 spol dimer1
    #16, 19 spol dimer3
    # for dir_num in range(16,19):
    for dir_num in range(len(path_dir)):
        directory = path_dir[dir_num]
        # print(dir_num)
        f_intensity = open(path + '/' +  directory + '/' + str(directory) + " intensity" + ".csv", "r", encoding = "utf8")
        f_matching = open(path + '/' +  directory + '/' + str(directory) + " matching" + ".csv", "r", encoding = "utf8")
        f_reappearing = open(path + '/' +  directory + '/' + str(directory) + " reappearing" + ".csv", "r", encoding = "utf8")
        f_radius = open(path + '/' +  directory + '/' + str(directory) + " radius" + ".csv", "r", encoding = "utf8")

        lines_intensity = f_intensity.readlines()
        lines_matching = f_matching.readlines()
        lines_reappearing = f_reappearing.readlines()
        lines_radius = f_radius.readlines()

        intensity_mat = []
        matching_mat = []
        reappearing_mat = []
        radius_mat = []

        for i in range(len(lines_intensity)-1):
            a = lines_intensity[i].split(",")
            a.remove(a[-1])
            intensity_mat.append(a)
        for i in range(len(lines_matching)-1):
            a = lines_matching[i].split(",")
            a.remove(a[-1])
            matching_mat.append(a)
        for i in range(len(lines_reappearing)-1):
            a = lines_reappearing[i].split(",")
            a.remove(a[-1])
            reappearing_mat.append(a)
        for i in range(len(lines_radius)-1):
            a = lines_radius[i].split(",")
            a.remove(a[-1])
            radius_mat.append(a)

        radius_cut = 3
        ratio_cut = 3
        length_cut = 3
        intensity_downcut = 2000
        intensity_upcut = 20000

    # frame_number = row + 1
        for row in range(len(reappearing_mat)):
        # for row in range(382,383):

            for inn in range(len(reappearing_mat[row])):
            # for inn in range(0,5):
                # print(inn)
                hist_radius = []
                hist_intensity = []
        #1st
                index = int(reappearing_mat[row][inn])
                # print(index)
                if float(radius_mat[row][int(index)]) < radius_cut:
                    hist_radius.append(float(radius_mat[row][index]))
                    hist_intensity.append(float(intensity_mat[row][index]))
        #2nd
                # print(round(float(intensity_mat[row][index])))
                if row+1 > len(reappearing_mat)-1:
                    break
                else:
                    index = matching_mat[row+1][index]
                    # print(index)
                    counter = 2
                while 1:
                    if index == 'None':
                        break
                    else:
                        if float(radius_mat[row+counter-1][int(index)]) < radius_cut:
                            hist_radius.append(float(radius_mat[row+counter-1][int(index)]))
                            hist_intensity.append(float(intensity_mat[row+counter-1][int(index)]))
                            # print(round(float(intensity_mat[row+counter-1][int(index)])))
                        if row+counter > len(reappearing_mat)-1:
                            break
                        else:
                            index = matching_mat[row+counter][int(index)]
                            counter = counter + 1
                            # print(index)
                # print('--------', row)


                if len(hist_intensity) > length_cut:
                    min_intensity = min(hist_intensity)
                    max_intensity = max(hist_intensity)
                    if max_intensity/min_intensity < ratio_cut:
                        avg = sum(hist_intensity)/len(hist_intensity)
                        if avg < intensity_upcut:
                            if avg > intensity_downcut:
                                hist_avg_intensity.append(avg)
                        # hist_intensity_mat.append(hist_intensity)
                        # hist_radius_mat.append(hist_radius)

        f_intensity.close()
        f_matching.close()
        f_reappearing.close()

    avg_avg = sum(hist_avg_intensity)/len(hist_avg_intensity)
    print(avg_avg, directory_name)

    bin_list = []
    num_bin = 20
    step = (intensity_upcut - intensity_downcut)/20
    for i in range(0, num_bin):
        bin_list.append(int(intensity_downcut + i*step))

    # data, bin = np.histogram(hist_avg_intensity, bins=bin_list)
    # xdata1 = bin_generator(bin)
    # ydata1 = data
    # xdata2 = np.linspace(intensity_downcut, intensity_upcut, 200)
    # popt, pcov = curve_fit(poissonian, xdata1, ydata1)
    # plt.plot(xdata2, poissonian(xdata2, *popt), color='royalblue',  label='$fit: mean value = %.1f' % (popt[1]))

    plt.hist(hist_avg_intensity , color="skyblue", density=False, bins=bin_list, lw=1, label='', ec='white', alpha=0.8, width=400)

    plt.xlim(intensity_downcut,intensity_upcut)
    # plt.ylim(550, 850)

    plt.xlabel('Emission (a.u.)', fontsize=20)
    plt.ylabel('Counts', fontsize=20)

    new1 = directory_name.split('_')
    new2 = ""
    for i in range(len(new1)):
        new2 = new2 + new1[i]
    plt.title(new2, fontsize=10)
    # plt.legend(loc=1)
    plt.savefig('./' + directory_name + '.png', format = "png")
    plt.close()
    # plt.show()
    line = str(directory_name) + line_generator(hist_avg_intensity)
    f_hist.write(line)

f_hist.close()
