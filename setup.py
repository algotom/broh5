import pathlib
import setuptools

dependencies = [
    "numpy>=1.23",
    "h5py>3.7",
    "hdf5plugin",
    "pillow",
    "matplotlib",
    "nicegui>=3.0"
]

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setuptools.setup(
    name="broh5",
    version="1.4.2",
    author="Nghia Vo",
    author_email="nvo@bnl.gov",
    description='Browser-based GUI HDF Viewer in Python',
    long_description=README,
    long_description_content_type="text/markdown",
    keywords=['HDF Viewer', 'NXS Viewer', 'Browser-based GUI'],
    url="https://github.com/algotom/broh5",
    download_url="https://github.com/algotom/broh5.git",
    license="Apache 2.0",
    platforms="Any",
    packages=setuptools.find_packages(include=["broh5", "broh5.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering"
    ],
    install_requires=dependencies,
    entry_points={'console_scripts': ['broh5 = broh5.main:main']},
    python_requires='>=3.9',
)
