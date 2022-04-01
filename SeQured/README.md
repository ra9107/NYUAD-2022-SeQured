# This is the readme file for NYUAD Hackathon 2022 for group SeQure 


# Background:

With the increasing risk of cybersecurity looming over, SeQured uses quantum randomness to anonymize medical data. The aim is to maintain the privacy of the patient's medical data, while at the same time enabling the ability of sharing it with medical practitioners in an easy and secure way. SeQured uses the Electrocardiogram as a use case to demonstrate the added value of the solution.


# 1: Quantum Randomness:

Random numbers are fundamental components of cryptography and cybersecurity. Classical methods of generating random numbers are only psuedo-random. On the other hand quantum mechanics is -- to the best of our knowledge -- fundamentally non-deterministic. Therefore, quantum computers and qubits provide a guaranteed method of generating truly random numbers.

A simple method of generating unbiased random numbers using quantum computers is to perform a Hadamard transform on a register of qubits, followed by a measurement. However, on Noisy Intermediate-Scale Quantum (NISQ) hardware, this will not be truly unbiased due to a variety of errors and noise impacting the qubits, such as T1 decay, imperfect analog gates, unitary errors due to classical crosstalk, correlated errors due to unwanted couplings between qubits, photon shot noise, etc. Therefore, instead of generating a random number (bitstring) using a Hadamard transform, we do so using random circuit sampling experiments.

It is well known that random circuits approximate unitary-2 designs in the limit of long circuit depth [*Comm. Math. Phys. volume 291, pages 257–302 (2009)*]. Therefore, random circuits provide a good method of generating more unbiased random numbers. While an single random circuit may still have some residual bias, by constructing a random number from the results of many random circuits, we hope to provide a truly unbiased random number generator.

Furthermore, Google's quantum supremacy experiment [*Nature volume 574, pages 505–510 (2019)*] demonstrated that random circuits cannot be efficiently simulated using classical computers. More concretely, they claimed that their largest random quantum circuit would take a classical supercomputer ~ 10,000 years to simulate. This results has been confirmed by other related experiments [*Science volume 370, issue 6523, pages 1460-1463 (2020)*],[*Phys. Rev. Lett. 127, 180501 (2021)*], and has shown to be #P-hard [*Nature Physics volume 15, pages 159–163 (2019)*]. Therefore, our random number generator is not only truly random and unbiased, it is also robust to classical methods for trying to hack or reconstruct the random number that is used as a key for encryption.

In our demonstration, we generate randomly sampled circuits containing random SU(2) single-qubit gates and entangling operations on non-local qubits up to depth 30. We measure 35 different random circuits on the IonQ quantum hardware and concatenate the results into a single 384 random bit string. As an example, we use this random bit string to anonymize medical data.


# 2: Coding Electrodiagram Signals with QR Codes

	- The ECG signal anonymizer sub-system: For demonstration purposes, the ECG signal anonymizer sub-system simulates the ECG waveform. It then uses Fast Fourier Transformation to transform the ECG signal into a frequency domain for easier manipulation. Once the ECG is transformed, it is then converted into bytes and encoded on base64. This will encode the binary data into the appropriate characters for ASCII. This is then integrated into a QR code for easier sharing with medical practitioners.

	- Intergrating Quantum Randomness into ECG's

		- The Medical Interface: the platform where the system re-creates the original signal for the patient/medical practitioner from the data encoded in the created QR code. This will enable easier access to the medical record.

	- Key array generator:

	- the ECG distortion:

	- Float trandformation:
