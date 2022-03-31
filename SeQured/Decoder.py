import numpy as np
import pandas as pd
import neurokit2 as nk
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq, ifft
import qrcode
import base64

# Open a file: file
f = open('int_debug.txt',mode='r')
 
# read all lines at once
norm64_array = f.read()

# close the file
f.close()

norm_string = base64.b64decode(norm64_array)

normalized = np.frombuffer(norm_string, dtype=np.int16)

print(normalized)

scale = 1.570274229379865

ascale = 1.2+0.5

INT_16_MAX = 2**14

m_ecg_real = np.float64((normalized*ascale)/(INT_16_MAX))

plt.figure(1)
plt.plot(range(0,len(m_ecg_real)),m_ecg_real)
plt.figure(2)
plt.plot(range(0,len(m_ecg_real)),normalized)
plt.show()