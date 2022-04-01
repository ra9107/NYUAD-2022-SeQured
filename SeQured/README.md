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


# 4: Generating QR Codes

# 5: Where Next?
**Complete Decoding in JavaScript:** We have only implemented the system for decoding the Base64 back into an array of integers in JavaScript. This array can be used to display the Distorted ECG. The original ECG can be obtained (see Decoder.py) but a similar functionality has not been implemented with JavaScript. 

**QR Code and Key Transaction:** We have not implemented any methods for transferring these files securely. Currently, we simply share information between the Generator and Decoder by saving information to files, with the keys in plaintext. Additional security measures are required for transporting the QR code and Key array. Concepts of Security in Depth need to be applied. 

**Integrating with Real ECG data:** The project uses NeuroKit2 (a Python package for simulating an ECG). Many of the parameters and operations have been implemented around this simulation. Modification will very likely be required for real ECG data. 


