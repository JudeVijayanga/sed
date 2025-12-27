from setuptools import setup, Extension
from Cython.Build import cythonize

ext_modules = [
    Extension(
        "gsed.csed",
        sources=["gsed/unitconversion.pyx", "gsed/unitconversion_cpp.cpp"],
        include_dirs=["gsed"],
        language="c++",
    )
]

setup(ext_modules=cythonize(ext_modules, language_level=3))
