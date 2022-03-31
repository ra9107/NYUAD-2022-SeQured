import numpy as np
import pandas as pd
import neurokit2 as nk
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq, ifft
import qrcode
import base64

def QRCoder():
    key = '01100011111100100111111001111101001100110101110110010011100001110010000000110110111010100101000000110110010001110000000111001100010000001000101101100111111100011000001100101011101000011111111111011101000100101001010110011000000010111001101011010010011011010110000011110101001101011111101110000111011111001111011010001110010110010100110101011001101010100100110011010010001101'
    key_array = [int(key[i:i+32],base=2) for i in range(0,32*6, 32)]
    #Variables
    d= 1    #Duration of measurement
    s= 500  #Rate of sampling
    h= 70   #Heart beat
    n= d*s  #Number of samples
    
    #Generate the ECG graph
    ecg = nk.ecg_simulate(duration=d, sampling_rate=s, heart_rate=h)

    #Creating the distortion
    #Distortion factors
    k = 5 #k is factor (noise factor)
    l = 2 #k is a factor (stretch factor)
    m = 3 #m is a factor (decay factor)

    #Fourier Transform
    ft_ecg = fft(ecg)
    xf = fftfreq(n, 1/s)   #Obtaining the frequency for plotting the Fourier Transforms

    #Creating the array with the distortion to apply
    np.random.seed(key_array) #Seed for the generator is only valid for one random function call (number or 1-d array)
    distortion_array = (np.random.rand(n)-0.5)/k  
    
    for i,v in enumerate(distortion_array):
        x = i
        x = (x/n)*l
        distortion_array[i] = distortion_array[i] * (1/(1+x)**m)
        
    distortion_array = distortion_array+1

    #Applying the distortion
    mft_ecg = ft_ecg*distortion_array

    #Applying Inverse Fourier Transform (to obtain modified ECG in time domain)
    m_ecg = ifft(mft_ecg)


    plt.figure(1)
    plt.plot(xf, np.abs(mft_ecg))
    plt.figure(2)
    plt.plot(xf, np.abs(ft_ecg))
    

    plt.figure(3)
    plt.plot(m_ecg)
    plt.figure(4)
    plt.plot(range(0,n),m_ecg,range(0,n),ecg)
    plt.gca().legend(('modified ecg','OG ecg'))
    #Convert the complex number array to float64
    m_ecg_real = m_ecg.real
    plt.figure(5)
    plt.plot(range(0,n),m_ecg,range(0,n),m_ecg_real)
    print('ECG:',type(ecg[0]))
    print('RECG:',type(m_ecg[0]))
    print('RECG_REAL:',type(m_ecg_real[0]))
    print(m_ecg_real[0])

    #Convert Float64 to Float16
    m_ecg_real16 = np.float16(m_ecg_real)
    print('RECG_REAL16:',type(m_ecg_real16[0]))
    print(m_ecg_real16[0])
    plt.figure(6)
    plt.plot(range(0,n),m_ecg_real16,range(0,n),ecg)

    #Writing the Float16 array to a file
    #f1=open("ecg_array.txt",'w')
    #for d in m_ecg_real16:
    #    print(d)
    #    f1.write(f"{d}\n")
    #f1.close()
    np.savetxt('ecg_array.csv', m_ecg_real16, delimiter=',')   # X is an array
    np.savetxt('ecg_array.txt', m_ecg_real16, delimiter='\n')   # X is an array
    
    #Converting the Float16 array into bytes (binary)
    b32_array = b"".join([bytes(x)  for x in m_ecg_real16])

    #Encoding byte string to Base64 
    b64_array = base64.b64encode(b32_array)
    print(b64_array)
    print(type(b64_array))

    #Writing the base64 string to a txt file
    f=open("debug.txt", "wb") 
    f.write(b64_array)
    f.close()

    #Embedding the base64 string into a QR code
    qr = qrcode.QRCode(
    version=26,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=5,
    border=4,
    )
    qr.add_data(b64_array)
    qr.make(fit=False)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save("QR_Code.png")

    #Float64 to Int16
    #scale = np.max(m_ecg_real) - np.min(m_ecg_real)
    scale = 1.2+0.5
    print('scale',scale)
    INT_16_MAX = 2**14
    normalized = np.int16(m_ecg_real*INT_16_MAX/scale)
    print(normalized)
    
    #Converting the Float16 array into bytes (binary)
    #rough = list()
    #for x in normalized:
    #    print(x)
    #    rough.append(bytes(x))
    #norm_string = b"".join([bytes(x) for x in normalized])
    norm_string = normalized.tobytes()
    #print(norm_string)
    #norm_string = b"".join(rough)

    #Encoding byte string to Base64 
    norm64_array = base64.b64encode(norm_string)
    #print(norm64_array)
    print(type(norm64_array))

    #Writing the base64 string to a txt file
    f=open("int_debug.txt", "wb") 
    f.write(norm64_array)
    f.close()

    #Embedding the base64 string into a QR code
    qr = qrcode.QRCode(
    version=26,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=5,
    border=4,
    )
    qr.add_data(norm64_array)
    qr.make(fit=False)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save("int_QR_Code.png")
    plt.show() #Displaying all the figures


QRCoder()



