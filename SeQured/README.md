# This is the readme file for NYUAD Hackathon 2022 for group SeQure 


- Background:


# 1: Quantum Randomization 

	- Using 


# 2: Generating ECG Signals
**ECG Simulation Parameters**

d: Duration of measurement

s: Rate of sampling

h: Heart Beat Rate

n: Number of samples (n=d\*s)

These parameters determines how Neurokit generates the ECG signals. The signal can be generated with the following function. 
ecg = nk.ecg_simulate(duration=d, sampling_rate=s, heart_rate=h)

The most important parameters here are s and d. They determine the size of the array (n), which needs to be encoded into a QR Code. The size needs to be adjusted to make the information fit the QR code.

# 3: Intergrating Quantum Randomness into ECG's
We begin by applying the Fourier Transform to the ECG signal. The Fourier Transform of the signal can be obtained by:

	ft_ecg = fft(ecg)
	xf = fftfreq(n, 1/s)
	
fftfreq() is used to obtain the frequencies needed for plotting the Fourier Transform (because Fourier Transform converts the signal from time domain to frequency domain). 

We then create the array with the distortion to apply. The distortion factors can be manipulated to control the distortion. The  distortion factors are:

k: Noise factor

l: Stretch factor

m: Decay factor

The following code snippet generates the distortion array:

	np.random.seed(key_array) #Seed for the generator is only valid for one random function call (number or 1-d array)
	distortion_array = np.complex128(np.random.rand(n)-0.5)/k  #Shifting values from 0-1 to -0.5 to 0.5, then dividing by k
	for i,v in enumerate(distortion_array):
	    x = i
	    x = (x/n)\*l
	    distortion_array[i] = distortion_array[i] \* (1/(1+x)\*\*m)    
	distortion_array = np.exp(1j\*2\*np.pi\*distortion_array)

The distortion array will be multiplied to the Fourier Transform of the ECG signal.

	mft_ecg = np.complex128(ft_ecg)\*distortion_array

We then apply the Inverse Fourier Transform to obtain the modified ECG in the time domain.

	m_ecg = ifft(mft_ecg)

The complex number based distortion can have a few issues. If obtaining the original ECG is absolutely necessary, the following code snippet for the distortion array should 
# 4: Generating QR Codes

# 5: Where Next?
**Solving the Complex Number Problem:** With the complex number distortion, the massively increased noise and shifting results in the decoded ECG appearing different to the original. 

**Complete Decoding in JavaScript:** We have only implemented the system for decoding the Base64 back into an array of integers in JavaScript. This array can be used to display the Distorted ECG. The original ECG can be obtained from the Distorted ECG (see Decoder.py) but the functionality has not been implemented with JavaScript. 

**QR Code and Key Transaction:** We have not implemented any methods for transferring these files securely. Currently, we simply share information between the Generator and Decoder by saving information to files, with the keys in plaintext. Additional security measures are required for transporting the QR code and Key array. Concepts of Security in Depth need to be applied. Something similar to Yubikeys could be utilized for physically transporting the key.

**Integrating with Real ECG data:** The project uses NeuroKit2 (a Python package for simulating an ECG). Many of the parameters and operations have been implemented around this simulation. Modification will very likely be required for real ECG data. 



