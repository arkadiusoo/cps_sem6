# Digital Signal Processing (Cyfrowe Przetwarzanie Sygnałów) – Assignments

## Assignment 1 – Signal and Noise Generation

This task implements a signal processing tool that allows users to generate, visualize, and analyze various types of signals and noise through an intuitive graphical user interface.

### Implemented Features

- **Generation of 11 signal types:**
  - Uniform noise, Gaussian noise
  - Sinusoidal (regular, half-wave rectified, full-wave rectified)
  - Square wave (classic and symmetric), triangular signal
  - Unit step, unit impulse, impulse noise

- **Support for continuous and discrete signal modes**

- **Interactive GUI** built with **PyQt6**

- **Visualization using matplotlib:**
  - Signal plots (amplitude vs. time)
  - Histograms with adjustable bin count (5–20 bins)

- **Binary file support:**
  - Save and load signal data
  - Customizable signal and sampling parameters (amplitude, duration, sampling frequency, etc.)

- **Basic operations on signals:**
  - Addition, subtraction, multiplication, division

- **Display of signal parameters:**
  - Mean, absolute mean, RMS, variance, average power

- **Signal history and reuse:**
  - Combine previously generated signals using arithmetic operations

- **Multi-screen support:**
  - The application window is centered on the second screen if available

---


## Assignment 2 – Sampling and Quantization

This task extends the first assignment by introducing signal digitization and reconstruction techniques.

### Implemented Features

- **Sampling of signals** from Assignment 1 with adjustable sampling frequency
- **Quantization** methods:
  - Truncation
  - Rounding
- **Reconstruction** methods:
  - Zero-order hold (ZOH)
  - First-order hold (FOH)
  - Sinc interpolation
- **Interactive plots**: original vs quantized vs reconstructed signal
- **Comparison metrics**:
  - MSE, SNR, PSNR, MD
  - Theoretical SNR (for sinusoidal signals)
  - ENOB (Effective Number of Bits)
- **Signal info popup** on double-click with full analysis

---
## Assignment 3 – Convolution, Correlation, and Filtering

This task focuses on signal processing operations such as convolution, correlation, and FIR filtering.

### Implemented Features

- **Manual and library-based convolution** of two arbitrary-length discrete signals
- **Cross-correlation**:
  - Manual (linear and circular)
  - Via convolution
  - Using NumPy
- **FIR filter design** (window method):
  - High-pass filters (variant F2)
  - Hanning window (variant O2)
- **Filter application via convolution**
- **Integrated GUI (PyQt6)**:
  - Signal selection from Assignment 1
  - Operation selection and parameter input
  - Dynamic plotting with matplotlib
  - Result history with comparison

---
 ## Assignment 4 – Transformations and Frequency Analysis

This task implements various discrete transformations for analyzing signals in the frequency and spectral domains.

### Implemented Features

- **Transformations supported**:
  - Discrete Fourier Transform (DFT)
  - Fast Fourier Transform (FFT) using Decimation-in-Frequency (DIF)
  - Walsh-Hadamard Transform (WHT)
  - Fast Walsh-Hadamard Transform (FWHT)

- **Interactive GUI (PyQt6)**:
  - Selection of signals from Assignment 1 or example signals
  - Transformation type selection and execution
  - Visualization modes for complex-valued transforms:
    - Real / Imaginary parts
    - Magnitude / Phase

- **Visualization using matplotlib**:
  - Frequency domain plots with subplots for amplitude and phase components

- **Result management**:
  - Result history with labels
  - Save and load transform results from `.npz` files

- **Performance metrics**:
  - Execution time of each transform function printed to console

- **Automatic zero-padding** for non-power-of-two lengths (for Walsh-Hadamard)
