# Team SeQured readme file (NYUAD Hackathon 2022) 


# Background:

With the increasing risk of cybersecurity looming over, SeQured uses quantum randomness to anonymize medical data. The aim is to maintain the privacy of the patient's medical data, while at the same time enabling the ability of sharing it with medical practitioners in an easy and secure way. SeQured uses the Electrocardiogram as a use case to demonstrate the added value of the solution.


# 1: Quantum Randomness:

Random numbers are fundamental components of cryptography and cybersecurity. Classical methods of generating random numbers are only psuedo-random. On the other hand quantum mechanics is -- to the best of our knowledge -- fundamentally non-deterministic. Therefore, quantum computers and qubits provide a guaranteed method of generating truly random numbers.

A simple method of generating unbiased random numbers using quantum computers is to perform a Hadamard transform on a register of qubits, followed by a measurement. However, on Noisy Intermediate-Scale Quantum (NISQ) hardware, this will not be truly unbiased due to a variety of errors and noise impacting the qubits, such as T1 decay, imperfect analog gates, unitary errors due to classical crosstalk, correlated errors due to unwanted couplings between qubits, photon shot noise, etc. Therefore, instead of generating a random number (bitstring) using a Hadamard transform, we do so using random circuit sampling experiments.

It is well known that random circuits approximate unitary-2 designs in the limit of long circuit depth [*Comm. Math. Phys. volume 291, pages 257–302 (2009)*]. Therefore, random circuits provide a good method of generating more unbiased random numbers. While an single random circuit may still have some residual bias, by constructing a random number from the results of many random circuits, we hope to provide a truly unbiased random number generator.

Furthermore, Google's quantum supremacy experiment [*Nature volume 574, pages 505–510 (2019)*] demonstrated that random circuits cannot be efficiently simulated using classical computers. More concretely, they claimed that their largest random quantum circuit would take a classical supercomputer ~ 10,000 years to simulate. This results has been confirmed by other related experiments [*Science volume 370, issue 6523, pages 1460-1463 (2020)*],[*Phys. Rev. Lett. 127, 180501 (2021)*], and has shown to be #P-hard [*Nature Physics volume 15, pages 159–163 (2019)*]. Therefore, our random number generator is not only truly random and unbiased, it is also robust to classical methods for trying to hack or reconstruct the random number that is used as a key for encryption.

In our demonstration, we generate randomly sampled circuits containing random SU(2) single-qubit gates and entangling operations on non-local qubits up to depth 30. We measure 35 different random circuits on the IonQ quantum hardware and concatenate the results into a single 384 random bit string. As an example, we use this random bit string to anonymize medical data.


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


