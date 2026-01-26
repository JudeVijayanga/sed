
# Getting Started

Welcome to **sed**!  
This page gives you a quick introduction to the package.

## 🌌 What is an SED?

A Spectral Energy Distribution (SED) describes how an astronomical object emits energy across the electromagnetic spectrum.
It represents flux (or luminosity) as a function of wavelength or frequency, combining data from ultraviolet (UV), optical, infrared (IR), and sometimes radio or X-ray observations.

In galaxy studies, SEDs are essential because they allow us to:

- estimate stellar masses, star-formation rates, and dust attenuation,

- measure dust temperatures and infrared luminosities,

- compare observations with physical models or simulations,

- study galaxy evolution across cosmic time.

By modelling an SED — often using functions like the Casey (2012) dust emission model — astronomers can translate raw photometric data into meaningful physical properties.



## A lightweight Python library that:

- reads SIMBA SED files  
- converts flux units  
- computes synthetic photometry  
- outputs results into clean folders  

## Requirements

- Python ≥ 3.9  
- NumPy  
- Matplotlib  
- SciPy  
- (Optional) Jupyter Notebook  

## Project structure
```
gsed/
│
├── sed/
│ ├── init.py
│ ├── conversion.py
│ ├── spectrum.py
│ ├── filters/
│ └── suppliments/
│    ├── sed_flux1_1.txt
│   ├── output.txt
├── tests/
│ 
│ └── test_conversion.py
├── output/
├── pyproject.toml
├── README.md
└── LICENSE
```

