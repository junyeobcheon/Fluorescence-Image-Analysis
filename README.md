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

time_tracking: 

하나의 샘플을 뽑아서 time tracking 을 해봄. 이 때 num_sig, max_sig, threshold 등 파라메터를 찾아야하기 때문에 미리 돌려보고 get_time_track_mat 을 수행하는게 좋다.

get_time_track_mat: time trace mat 을 만들어준다. time tracking 을 통해 파라메터를 조절해놔야지 정보를 알맞게 뽑을 수 있다.

operate_time_track: histogram 을 보여준다 여기서도 역시 파라메터를 잘 설정해서 원하는 결과가 나오도록 조절해야한다.







I developed the codes here while I was in the graduate school (Master Course). I was investigating 
