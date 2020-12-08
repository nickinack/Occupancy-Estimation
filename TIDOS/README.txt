All the frames in TIDOS dataset can be visualized by using 'tidos_visualizer.m'

In this code there are three variables that you need to initialize:

1) location

This variable should be set to the location (in your computer) of the specific recording that you want to visualize

e.g: location = 'C:\Users\xxxx\Desktop\TIDOS\Data\Lecture\lecture_sensor_1'

2) sec

You should set this variable to the specific second of the recording that you want to visualize
Note: The constraint for the variable 'sec' is the following, 0 < sec < ((length of the recording in seconds) + 1)

e.g: sec = 10

3) frame

You should set this variable to the frame that you want to visualize in a specific second.
Note: Variable 'frame' can take values from 1 to 16. Because we recorded data at 16 Hz and there 16 frames captured in a single second(.JSON file).

e.g: frame = 12


A toy example:

If you set sec=10 and frame=12, it means you will visualize the 12th frame within the 10th second of the video.

All the initializations are performed at the very beginning of the code. Once you initialize the variables mentioned above. You are ready the visualize frames from TIDOS dataset.