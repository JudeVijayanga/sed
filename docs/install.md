# Installation instructions

We recommend that you install the solar system generator in a conda environment.
If you don't already have conda, install [Miniconda](https://www.anaconda.com/download/success) 
following the [instructions](https://www.anaconda.com/docs/getting-started/miniconda/install) for your operating system. 
Once you have miniconda, create a new conda environment using the [myenv.yml](https://drive.google.com/file/d/1e44vjI2q-3aW41ChRvum1KCcGCevo2tf/view?usp=sharing) file.
In a terminal (or Anaconda Powershell prompt for Windows), run:

```
conda env create -f myenv.yml
```

Then, activate the conda environment:

```
conda activate my-env
```

Clone the repository and pip install:

```
git clone https://gitlab.com/iubr/py3umk.git
cd py3umk
pip install .
```
