# SPLSCATT

A Spinless Partial-Wave Elastic Scattering Code for Finite-Range Central Potentials

## Overview

SPLSCATT is a Python package for solving the radial Schrödinger equation and computing elastic scattering observables using the partial-wave expansion method.

The package consists of two graphical applications:

* **POTGEN** – Potential Generator
* **SPLSCATT** – Elastic Scattering Solver

Both programs are written in Python and use a simple Tkinter graphical user interface.

The code is intended for educational and research applications in nuclear physics, quantum scattering, and related fields.

---

## Features

### POTGEN

Generate central potentials on a radial mesh and save them in a format directly readable by SPLSCATT.

Available potentials:

* Square well
* Woods–Saxon
* One-Yukawa
* Two-Yukawa (Malfliet–Tjon)
* Three-Yukawa
* Gaussian

Output:

```text
potential.dat
```

containing

```text
r(fm)    V(MeV)
```

---

### SPLSCATT

Solve the radial Schrödinger equation using the Numerov method and calculate:

* Radial wave functions
* Partial-wave phase shifts
* Differential cross sections
* Partial elastic cross sections
* Total elastic cross section
* Low-energy scattering length (when applicable)

Output:

```text
scatt.out
```

---

## Quick Start

The easiest way to use the package is through the provided launcher scripts.

### Linux

Make the launcher executable:

```bash
chmod +x run_splscatt.sh
```

Run:

```bash
./run_splscatt.sh
```

The script automatically:

* Checks Python installation
* Checks required libraries
* Installs missing dependencies
* Launches POTGEN
* Launches SPLSCATT

---

### macOS

Make the launcher executable:

```bash
chmod +x run_splscatt_macos.sh
```

Run:

```bash
./run_splscatt_macos.sh
```

The script automatically:

* Checks Python installation
* Verifies NumPy, SciPy, Matplotlib, and Tkinter
* Installs missing Python packages
* Launches POTGEN
* Launches SPLSCATT

---

## Repository Structure

```text
SPLSCATT/
│
├── potgen_gui.py
├── splscatt_gui.py
│
├── run_splscatt.sh
├── run_splscatt_macos.sh
│
├── requirements.txt
├── README.md
│
├── potential.dat
└── scatt.out
```

### Files

| File                  | Description               |
| --------------------- | ------------------------- |
| potgen_gui.py         | Potential generator       |
| splscatt_gui.py       | Elastic scattering solver |
| run_splscatt.sh       | Linux launcher            |
| run_splscatt_macos.sh | macOS launcher            |
| potential.dat         | Generated potential       |
| scatt.out             | Scattering output         |
| requirements.txt      | Python dependencies       |
| README.md             | Documentation             |

---

## Manual Installation

### Fedora

```bash
sudo dnf install \
    python3 \
    python3-numpy \
    python3-scipy \
    python3-tkinter \
    python3-matplotlib
```

---

### Ubuntu / Debian

```bash
sudo apt update

sudo apt install \
    python3 \
    python3-numpy \
    python3-scipy \
    python3-tk \
    python3-matplotlib
```

---

### macOS

Install Python:

```bash
brew install python
```

Install required packages:

```bash
pip3 install numpy scipy matplotlib
```

Verify Tkinter:

```bash
python3 -c "import tkinter"
```

If Tkinter is unavailable, install the appropriate Homebrew package for your Python version.

---

## Running the Programs

### Generate a Potential

Launch POTGEN:

```bash
python3 potgen_gui.py
```

Choose:

* Potential type
* Potential parameters

Then click:

```text
Generate potential.dat
```

A file named

```text
potential.dat
```

will be written in the current directory.

---

### Run a Scattering Calculation

Launch SPLSCATT:

```bash
python3 splscatt_gui.py
```

Specify:

* Potential file
* Reduced mass μ
* Scattering energy E
* Maximum orbital angular momentum lmax

Click:

```text
Run
```

The program writes

```text
scatt.out
```

containing all calculated observables.

---

## Typical Workflow

### Step 1

Generate a potential:

```text
POTGEN
    ↓
potential.dat
```

### Step 2

Run the scattering calculation:

```text
SPLSCATT
    ↓
scatt.out
```

---

## Input Potential Format

SPLSCATT expects a two-column text file:

```text
0.0500   -49.90
0.1000   -49.85
0.1500   -49.78
...
```

Columns:

| Column | Meaning              |
| ------ | -------------------- |
| 1      | Radius r (fm)        |
| 2      | Potential V(r) (MeV) |

Comment lines beginning with `#` are ignored.

---

## Numerical Method

The code uses:

* Partial-wave expansion
* Numerov integration method
* Matching to asymptotic spherical Bessel functions
* Phase-shift analysis

The scattering amplitude is

```math
f(\theta)
=
\frac{1}{2ik}
\sum_l
(2l+1)
\left(
e^{2i\delta_l}-1
\right)
P_l(\cos\theta)
```

and the differential cross section is

```math
\frac{d\sigma}{d\Omega}
=
|f(\theta)|^2 .
```

---

## Future Development

Planned features include:

* Coulomb scattering
* Optical model potentials
* Complex potentials
* Bound-state solver
* Resonance analysis tools
* Graphical plotting utilities
* Export of results in CSV format

---

## Author

**Nguyen Le Anh, PhD**

Department of Physics

Ho Chi Minh City University of Education (HCMUE)

Vietnam

---

## Citation

If you use this code in research or publications, please cite:

Nguyen Le Anh, *SPLSCATT: A Spinless Partial-Wave Elastic Scattering Code for Finite-Range Central Potentials*.

---

## License

This project is released under the MIT License.
