# sed

# 🌌 gsed — Galaxy SED Generator

A Python tool to generate **spectral energy distributions (SEDs)** from galaxy photometry and compute **FIR luminosity**, **dust temperature**, and **UV luminosity** using the *Casey (2012)* model.

![SED](best_sed_1_s110.png)

---

## 📖 Overview

`gSEd` reads galaxy photometry (in **mJy**) and produces:

- **Total far-infrared (FIR) luminosity** in solar units (L☉), by integrating over the rest-frame range of 8–1000 μm.  
- **Dust temperature** (K) using the modified greybody + power-law SED formulation from *Casey (2012)*.  
- **UV luminosity** (L☉) evaluated at rest-frame 1500 Å.

---

## 🧱 Project Structure
```
sed/
│
├── README.md # Main program: generates SEDs
├── LICENSE # Reads and processes photometric input
├── gsed/ # Utility functions and helpers
│ ├── conversion.py
│ └── spectrum.py
  └── suppliments\
  
├── tests/ # Unit tests (optional)
 
```

---

## 🧩 The Casey (2012) Model

The **Casey (2012)** far-infrared SED model combines a *modified greybody* and a *mid-infrared power-law* component.

### Functional Form

```math
S(\nu) \propto \left[ 1 - e^{-\tau(\nu)} \right] \, B(\nu, T) + A \, \nu^{-\alpha}
```

where:
- **B(ν, T)** — Planck function at temperature T  
- **τ(ν)** — optical depth = (ν / ν₀)^β  
- **β** — dust emissivity index (typically ~1.6)  
- **α** — mid-IR power-law slope (typically ~2.0)  
- **A** — normalization constant ensuring continuity at the transition point

This function captures both the **thermal emission from dust** and the **warmer mid-IR continuum**.

### FIR Luminosity

The total FIR luminosity is computed by integrating the rest-frame SED from **8 μm to 1000 μm**:
```math
L_{\mathrm{FIR}} = 4\pi D_{L}^{2} \int_{8\,\mu\mathrm{m}}^{1000\,\mu\mathrm{m}} S(\nu)\, d\nu

```

where **D_L** is the luminosity distance.

### UV Luminosity

The **UV luminosity** is derived from the SED at the rest-frame wavelength of **1500 Å**, tracing the unobscured star formation component.

---

## ⚙️ Installation

Clone the repository and install locally:

```bash
git clone https://github.com/JudeVijayanga/sed.git
cd sed
pip install .
```

## 🚀 How to use.

1. Quick Test Run

Before you run the code below, copy and paste it into a new Python file and save it outside the "sed" folder. For information read the manual inside the docs folder.
```bash

import numpy as np
import gsed


# 1. Initialize the Analyzer
# This sets up the cosmology and the output folders
spect=gsed.GalaxySEDAnalyzer(filter_dir='sed/gsed/suppliments/filters', 
    output_dir='sed/gsed/outputs')

# 2. Setup your parameters
# Usually, you would load these from a file
try:
    redshifts = np.loadtxt('sed/gsed/suppliments/outputs.txt')
    galId = 1
    snap = 110
    
    # Check if snap exists in your redshift file
    if snap < len(redshifts):
        z = redshifts[int(snap)][1]
    else:
        z = 0.5  # Fallback example redshift
        print("Snap index out of range, using fallback redshift.")

    # 3. Define the path to your specific SED file
    sed_file_path = "sed/gsed/suppliments/sed_flux1_1.txt"

    # 4. Run the Pipeline
    # This extracts fluxes, fits the model, saves .dat files, and saves the .png plot
    print(f"Starting analysis for Galaxy {galId} (Snap {snap})...")
    
    lir, temp = spect.run_analysis(
        galId=galId, 
        snap=snap, 
        z=z, 
        sed_file=sed_file_path
    )

    print("-" * 30)
    print("Analysis Successful!")
    print(f"L_IR (solar): 10^{np.log10(lir):.2f}")
    print(f"Dust Temp: {temp:.2f} K")
    print(f"Files saved in: {spect.output_dir}/")

except Exception as e:
    print(f"An error occurred: {e}")

```

In your terminal, 

```bash
cd ../sed
python your_save_file_name.py
```


Results appear in the  output folder inside the gsed folder. 


___________________________________________________

2. Using Your Own Galaxy SED
   To compute synthetic SIMBA photometry:

- First, Update the input SED - replace gsed/suppliments/sed_flux1_1.txt with your own wavelength (µm) and flux (mJy) data.
- Second, Set the galaxy redshift - Find the redshift in: gsed/suppliments/output.txt and update spectrum.py:
- Third, Run the program $python spectrum.py.
- Retrieve results: Outputs go to: output/

3. Testing
- Find testing folder: cd test/
- Run the program $pytest test_conversion.py
