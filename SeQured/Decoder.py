import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq, ifft
import base64

'''
Required Libraries
The Basic Trinity: NumPy, Pandas, Matplotlib
SciPy: For Fourier Transforms
Base64: For converting between binary and Base64 code

Note: Matplotlib can be avoided if need be. It is only required for plotting the graphs if one needs to. (see end of file)
'''

#Note: ensure consistency of variables between generator and decoder

#ECG Simulation Parameters
d= 1    #Duration of measurement
s= 500  #Rate of sampling
h= 70   #Heart beat
n= d*s  #Number of samples

#Distortion factors
k= 5    #k is the noise factor
l= 2    #l is the stretch factor
m= 3    #m is the decay factor

#Retrieving and Loading the array of keys
key_array= np.uint32(np.loadtxt('key.txt', dtype=int))

#Reading the entire base64 string from the file
f= open('base64_debug.txt',mode='r')
norm64_array = f.read()
f.close()

#Decoding the Base64 string
norm_string = base64.b64decode(norm64_array)

#Converting the Decoded string back into the int16 values (normalized float)
normalized = np.frombuffer(norm_string, dtype=np.int16)

#Converting the Int16 back to float
scale = 1.2+0.5
INT_16_MAX = 2**14
m_ecg_real = np.float64((normalized*scale)/(INT_16_MAX))

#Decoding to get the original graph
#Creating the array with the distortion to apply
np.random.seed(key_array) #Seed for the generator is only valid for one random function call (number or 1-d array)
distortion_array = (np.random.rand(n)-0.5)/k  #Shifting values from 0-1 to -0.5 to 0.5, then dividing by k 
for i,v in enumerate(distortion_array):
    x = i
    x = (x/n)*l
    distortion_array[i] = distortion_array[i] * (1/(1+x)**m)   
distortion_array = distortion_array+1

#Fourier Transform (of the modified ECG)
mft_ecg = fft(m_ecg_real)
xf = fftfreq(n, 1/s)   #Obtaining the frequency for plotting the Fourier Transforms

#Divide by distortion array
ft_ecg = mft_ecg/distortion_array;  #Reversing the distortion scaling

#Applying Inverse Fourier Transform (to obtain the original ECG in time domain)
ecg = ifft(ft_ecg)

#Debug
#plt.figure(1)
#plt.plot(range(0,n),m_ecg_real,range(0,n),ecg)
#plt.gca().legend(('Distorted ECG','ECG'))
#plt.show()