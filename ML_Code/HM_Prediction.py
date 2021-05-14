#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 16:16:40 2021

@author: alexis
"""

# Helper libraries
print('Importing Tensorflow... ', end='', flush=True)
import tensorflow as tf
print('Done!')
print('Importing Keras... ', end='', flush=True)
from tensorflow import keras 
print('Done!')

print('Importing numpy... ', end='', flush=True)
import numpy as np
from numpy import linspace
from numpy import fft
print('Done!')
print('Importing scipy... ', end='', flush=True)
import scipy.io as sio
print('Done!')
print('Importing matplotlib.pyplot... ', end='', flush=True)
#import matplotlib.pyplot as plt
import matplotlib
#matplotlib.use('agg')
import matplotlib.pyplot as plt
print('Done!')
print('Importing math... ', end='', flush=True)
import math
print('Done!')
import tkinter
from scipy.signal import savgol_filter

from Form_ML_Data import Load_HM_Data_Output
from Form_ML_Data import Load_Data_QBMM
from ML_Training  import HM_Training
from ML_Training  import HM_Testing


# Load MC data
#cases = "constant";
#cases = "sine";
cases = "random";
output_data, qbmm_HM, max_out, total_cases, total_times, T, input_data, max_in = Load_HM_Data_Output(cases)
# Load QBMM data
#input_data, max_in = Load_Data_QBMM(cases,T,total_times)


used_features = 10
# Train neural-net for High-moments predictions
if (cases == "constant"):
    train_cases = [0,1,3,5,7,9,11,13,15]
elif (cases == "sine"):
    train_cases = [0,2,4,6,8,10,12,14,16,
                   34+0,34+2,34+4,34+6,34+8,34+10,34+12,34+14,34+16,
                   68+0,68+2,68+4,68+6,68+8,68+10,68+12,68+14,68+16,
                   102+0,102+2,102+4,102+6,102+8,102+10,102+12,102+14,102+16]
elif (cases == "random"):
    #train_cases = [0,1,6,7,8,9,10,11]
    train_cases = [0,1,2,3,4,5,6,7,8,9,10,11,12]

    
HM_Training(input_data,output_data,qbmm_HM,max_in,max_out,total_times,train_cases,cases,used_features)

#if (cases == "constant"):
#    model1 = tf.keras.models.load_model('HM_MLQBMM.h5')
#elif (cases == "sine"):
#    model1 = tf.keras.models.load_model('HM_Sinusoidal_MLQBMM.h5')

test_cases = [ii for ii in range(0,25)]

predictions = HM_Testing(input_data,output_data,qbmm_HM,max_in,max_out,total_times,used_features,test_cases,cases)
if (cases == "constant"):
    sio.savemat('HM_MLQBMM.mat',{'predictions':predictions})
elif (cases == "sine"):
    sio.savemat('HM_Sinusoidal_MLQBMM.mat',{'predictions':predictions,'input_data':input_data,'output_data':output_data})
elif (cases == "random"):
    sio.savemat('HM_Random_MLQBMM.mat',{'predictions':predictions,'input_data':input_data,'output_data':output_data,'max_in':max_in,'max_out':max_out})

    
    
    
    
    