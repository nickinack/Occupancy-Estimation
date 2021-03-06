import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os

print("Visualizer")
# Select the setting
store_list = []
path = '../TIDOS/Data/Lunch_Meeting_3/lunch_meeting_3_sensor_2/'
seconds = 879
for file in os.listdir(path):
    f_name = path + file
    input_file = open(f_name)
    json_array = json.load(input_file)
    data_time = {"Temperature": json_array['Frames_B'] , "TimeStamp": json_array['TimeStamp']}
    store_list.append(data_time)

# Sort wrt to the timestamps  
sorted_list = sorted(store_list, key=lambda k: k['TimeStamp'])
temp_list = []
for i in sorted_list:
    temp_list.append(i["Temperature"])

# Reshape the JSON data
data = np.zeros((seconds,24,32,16))
for i in range(0,seconds):
    for k in range(0,16):
        for j in range(0,24):
            data[i,j,:,k] = temp_list[i][k][32*j : 32*(j+1)]

# Print the shape
# print(np.shape(data))


