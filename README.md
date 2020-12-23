# Occupancy-Estimation
Implementation of "Low-Resolution Overhead Thermal Tripwire Configuration" for Occupancy Estimation as a part of my winter research @ <i>IIT Madras</i> advised by Prof. Raghunathan Rengaswamy. The delivarable of this research project includes the entry-exit count in a room and the occupancy of the room. The current work involves removing lingering blobs.

## Dataset

The dataset which has been used for the implementation is the TIDOS (Thermal Images for Doorbased Occupancy Sensing) dataset. The dataset is publicly available2
and includes several types of door activity: single person entering/leaving the classroom, multiple people entering/leaving through the same door, people lingering in the door, people with backpacks, in thick clothing, carrying various items, etc.

## Algorithm

The implementation has been divided into the following steps:
- Background Subtraction using Markov random fields (MRF)
- Blob detection
- Centroid calculation
- Outlier removal
- Mapping
- Counting

The details of each of the step is given in the paper.

## Requirements

```bash
numpy
scipy
matplotlib
seaborn
```

## Running

In order to run the code, provide your dataset at ```visualize.py``` and run the following command:

```bash
python3 counting.py
```
A sample dataset feeded into  ```visualize.py``` has been provided below:

```python3
print("Visualizer")
# Select the setting
store_list = []
path = '../TIDOS/Data/Edge_Cases/edge_cases_sensor_1/'
seconds = 410
for file in os.listdir(path):
    f_name = path + file
    input_file = open(f_name)
    json_array = json.load(input_file)
    data_time = {"Temperature": json_array['Frames_B'] , "TimeStamp": json_array['TimeStamp']}
    store_list.append(data_time)
```

## Results

The achieved results indicate that typically 80-90% entry and exit events are correctly classified for scenarios with a wide range of extreme challenges, while in
simpler, less-active scenarios even 100% correct classification can be reached.

### Accuracies obtained

- Lecture : 100%
- Lunch Meeting 2 : 100%
- Lunch Meeting 1 : 96%
- Lunch Meeting 3 : 95%
- Edge Cases L 80%

## Further Queries

In case of any further queries, visit <a href="https://nickinack.github.io/about/"> Nickinack's webpage </a>
