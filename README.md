# BroH5
(**Bro**)wser-based GUI (**H**)DF(**5**) Viewer in Python

Web browser-based GUI software is increasingly popular for its cross-platform 
compatibility, but typically requires web programming knowledge. 

The [Nicegui](https://nicegui.io/) framework simplifies this, enabling pure 
Python development of browser-based GUIs. This project uses Nicegui to create 
an HDF viewer, showcasing its effectiveness for local app development. 
Unlike other apps such as Hdfviewer, Vitables, Nexpy, or H5web, 
which are built using C, Java, Qt/PyQt, or HTML/JavaScript; this project is 
unique in being a browser-based GUI, but written entirely in Python 
with a minimal codebase.

Features
--------

- A browser-based GUI software for viewing HDF (Hierarchical Data Format) file 
  written in pure Python with minimal codebase.
- The software provides essential tools for viewing hdf files such as: 
  displaying tree structures or paths to datasets/groups; and presenting 
  datasets as values, images, plots, or tables. Users also can save datasets 
  to images or csv formats.

  ![Fig_01](https://github.com/algotom/broh5/raw/main/figs/fig_01.png)
  
  ![Fig 04](https://github.com/algotom/broh5/raw/main/figs/fig_04.png)

  ![Fig 05](https://github.com/algotom/broh5/raw/main/figs/fig_05.png)
    
  ![Fig_02](https://github.com/algotom/broh5/raw/main/figs/fig_02.png)

- Broh5 can view compressed hdf files by using compressors from
  [hdf5plugin](https://pypi.org/project/hdf5plugin/).

- The codebase is designed using the RUI (Rendering-Utilities-Interactions) 
  concept, which is known as the MVC (Model-View-Controller) pattern in the 
  GUI development community. This design allows for the development 
  of complex software and makes it easier to extend its capabilities.

Installation
------------

Broh5 can be installed using [pip](https://pypi.org/project/broh5/),
[conda](https://anaconda.org/conda-forge/broh5), or directly from the
[source](https://broh5.readthedocs.io/en/latest/toc/installation.html#installing-from-source). 
Users can also generate a [standalone executable file](https://broh5.readthedocs.io/en/latest/toc/installation.html#generating-a-standalone-executable-file) 
for convenient usage. Details are at:

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
    due to processing time. Starting from version 1.3.0, users can choose to display 
    a **zoomed area** of the current image or the **intensity profile** across a mouse-clicked location.
        
  - Datasets that are 1D or 2D arrays will be shown as plots or tables, selectively.
  - Users have the option to save images or tables to disk.

Update notes
------------
- 30/10/2023: Published codes, deployed on pip and conda.
- 11/02/2024: Added tab for displaying image histogram and statistical information.
- 30/04/2024: Allow to open/save from the last opened folder.
- 04/07/2024: Added features for image zooming and intensity profile plotting
- 01/02/2025: Fixed a bug related to the OK button in FilePicker.
- 05/02/2025: Updated the table-format method for nicegui 2.0 and later.
- 01/06/2025: Fixed mouse-clicked location problem for nicegui>2.14
- 25/12/2025: Updated main.py to work with nicegui>=3.0
 
Author
------

Nghia T. Vo - NSLS-II, Brookhaven National Lab, USA.