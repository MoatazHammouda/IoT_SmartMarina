
import numpy as np
import pandas as pd
from scipy import signal

#fs is the sampling frequency
#cutoff is the cutoff frequency in Hertz
#data is the signal you want to filter 

# to call the functions: filtered_signal = butter_highpass_filter(signal.data,cutoff,fs)
# signal.data is the data of the input signal to the filter 


def butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
    return b, a
    
def butter_lowpass(cutoff,fs,order=5):
    nyq=0.5*fs
    normal_cutoff=cutoff/nyq
    b,a = signal.butter(order,normal_cutoff, btype='low',analog=False)
    return b,a

def butter_highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = signal.filtfilt(b, a, data)
    return y

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = signal.filtfilt(b, a, data)
    return y
