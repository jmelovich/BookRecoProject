from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import pybind11
import sys
import platform
import os
import zipfile
import shutil
from urllib.request import urlretrieve

# Download and extract Eigen if not already present
def get_eigen():
    eigen_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lib', 'eigen')
    if not os.path.exists(eigen_dir):
        print("Downloading Eigen...")
        os.makedirs('lib', exist_ok=True)
        # Download Eigen 3.4.0
        url = "https://gitlab.com/libeigen/eigen/-/archive/3.4.0/eigen-3.4.0.zip"
        zip_path = os.path.join('lib', 'eigen.zip')
        urlretrieve(url, zip_path)
        
        # Extract Eigen
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall('lib')
        
        # Rename the extracted directory
        extracted_dir = os.path.join('lib', 'eigen-3.4.0')
        if os.path.exists(extracted_dir):
            os.rename(extracted_dir, eigen_dir)
        
        # Clean up
        os.remove(zip_path)
    
    return os.path.join(eigen_dir)

# Get Eigen include path
eigen_include = get_eigen()

class BuildExt(build_ext):
    """A custom build extension for adding compiler-specific options."""
    def build_extensions(self):
        opts = []
        if platform.system() == "Windows":
            opts.append('/EHsc')
        else:
            opts.extend(['-std=c++11', '-fvisibility=hidden'])
        
        for ext in self.extensions:
            ext.extra_compile_args = opts
        build_ext.build_extensions(self)

ext_modules = [
    Extension(
        "book_database_cpp",
        ["book_database.cpp"],
        include_dirs=[
            pybind11.get_include(),
            pybind11.get_include(user=True),
            eigen_include,
        ],
        language='c++',
    ),
]

setup(
    name="book_database_cpp",
    version="0.0.1",
    author="Your Name",
    author_email="your.email@example.com",
    description="A C++ implementation of BookDatabase",
    long_description="",
    ext_modules=ext_modules,
    install_requires=['pybind11>=2.4.3'],
    setup_requires=['pybind11>=2.4.3'],
    cmdclass={'build_ext': BuildExt},
    zip_safe=False,
)