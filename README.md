# BroH5
(**Bro**)wser-based GUI (**H**)DF(**5**) Viewer in Python

Web browser-based GUI software is increasingly popular for its cross-platform 
compatibility, but typically requires web programming knowledge. 

The [Nicegui](https://nicegui.io/) framework simplifies this, enabling pure 
Python development of browser-based GUIs. This project leverages Nicegui to 
create an HDF viewer, showcasing its effectiveness for local app development. 
Unlike other HDF/H5/NXS file viewers like hdfviewer, vitables, nexpy, or h5web, 
which are built using C, Java, Qt/PyQt, or HTML/JavaScript; this project is 
unique in being a web browser-based HDF viewer written entirely in Python 
with a minimal codebase.

Features
--------

- A browser-based GUI software for viewing HDF (Hierarchical Data Format) file 
  written in pure Python with minimal codebase.
- The software provides essential tools for viewing hdf files such as: 
  displaying tree structures or paths to datasets/groups; and presenting 
  datasets as values, images, plots, or tables. Users also can save datasets 
  to images or csv formats.

  ![Fig_01](https://github.com/nghia-vo/broh5/raw/main/figs/fig_01.png)

- Broh5 can view compressed hdf files by using compressors from
  [hdf5plugin](https://pypi.org/project/hdf5plugin/).

- The codebase is designed using the RUI (Rendering-Utilities-Interactions) 
  concept, which is known as the MVC (Model-View-Controller) pattern in the 
  GUI development community. The name 'MVC' may not be very intuitive for 
  those new to GUI development. However, this design allows for the development 
  of complex software and makes it easier to extend its capabilities.

Installation
------------

Broh5 can be installed using [pip](https://pypi.org/project/broh5/),
[conda](https://anaconda.org/conda-forge/broh5), or directly from the
[source](https://github.com/algotom/broh5). Users can also generate a
standalone executable file for convenient usage. Details are at:

  - https://broh5.readthedocs.io/en/latest/toc/installation.html

Documentation
-------------

Documentation page is at: https://broh5.readthedocs.io. Brief functionalities of broh5:

  - Users can open a hdf file by clicking the "Select file" button. Multiple hdf 
    files can be opened sequentially.
  - Upon opening, the tree structure of the current hdf file is displayed, allowing 
    users to navigate different branches (hdf groups) or leaves (hdf datasets). 
    The path to datasets/groups is also displayed. If a dataset contains a string 
    or a single float/integer value, it will be shown.
  - If dataset is a 3D array, it's presented as an image. Users can slice 
    through various images and adjust the contrast. Slicing is available for 
    different axes; however, for large datasets, slicing along axis 2 is disabled 
    due to processing time.
  - Datasets that are 1D or 2D arrays will be shown as plots or tables, selectively.
  - Users have the option to save images or tables to disk.
 
 
Author
------

Nghia T. Vo - NSLS-II, Brookhaven National Lab, USA.