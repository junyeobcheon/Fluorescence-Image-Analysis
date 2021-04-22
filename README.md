# Fluorescence-Image-Analysis

The set of codes are developed by Junyeob Cheon in order for investigating the fluorescence signals of DNA-conjugated fluorophores.

imagestack_pulling:
The CCD camera records the time trace of fluorophores and gives a tif file as a result. 
When the whole video is saved as a single tif file, the image process is difficult. 
'imagestack.py' turns the tif raw data into individual frames. That makes the image process easier.   

multiple_background_reduction:
Before the CCD signal is interpreted as a proper fluorescence intensity, a background signal must be subtracted.
The background signal comes mainly from dark signal(CCD's background current) and spurious noise(light intensity other than true fluorescence).
In the 'multiple_background_reduction.py', various kinds of background noise are reduced by applying customized average filter and gaussian filter.

![20210407 polTIRF background reduction2](https://user-images.githubusercontent.com/35727159/115662580-2494c800-a37a-11eb-818b-71adc8765d15.png)

time_tracking: 
When the fluorescent molecules are continuously illuminated, the fluorescent molecule stops light emission. These phenomenon is called 'quenching'.
'time_tracking.py' connects individual frames. this code visualizes the relationship between every bright spots in the two consecutive frames.

The code confirms whether the two bright spots from two different frames come from an identical molecule by several rules. 
1) When the distance between the two spots is greater than certain value (threshold), the two spots are distinguishable with each other.  
2) In a single frame, when the two spots are too close to be separatly recognized, these two are excluded in the analysis.
3) 

![20210204 time tracking of blobs](https://user-images.githubusercontent.com/35727159/115664817-52c7d700-a37d-11eb-9d37-ce7154a1c3b8.png)


get_time_track_mat: 
operate_time_track: 

![20210213 polTIRF analysis3](https://user-images.githubusercontent.com/35727159/115664726-2c09a080-a37d-11eb-857a-556eb9ba72f7.png)





