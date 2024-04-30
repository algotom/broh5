Broh5's documentation
=====================

Broh5 is a GUI (Graphical User Interface) software for viewing HDF/H5/NXS files.
Unlike previous viewers built with various languages and platforms, Broh5's UI
components are based on web browsers but the software written entirely in Python,
thanks to the `NiceGUI <https://nicegui.io/>`__ framework.

    .. image:: toc/figs/fig_01.png
      :width: 100 %
      :align: center


**Source code:** https://github.com/algotom/broh5

**Author:** Nghia T. Vo - NSLS-II, Brookhaven National Laboratory, US.

**Keywords:** HDF Viewer, Browser-based GUI.

Features
========

-   A browser-based GUI software for viewing HDF (Hierarchical Data Format) file
    written in pure Python with minimal codebase.
-   The software provides essential tools for viewing hdf files such as:
    displaying tree structures or paths to datasets/groups; and presenting
    datasets as values, images, plots, or tables. Users also can save datasets
    to images or csv formats.
-   Broh5 can view compressed hdf files by using compressors from
    `hdf5plugin <https://pypi.org/project/hdf5plugin/>`__.
-   The codebase is designed using the RUI (Rendering-Utilities-Interactions)
    concept, which is known as the MVC (Model-View-Controller) pattern in the
    GUI development community. The name 'MVC' may not be very intuitive for
    those new to GUI development. However, this design allows for the development
    of complex software and makes it easier to extend its capabilities.

Video demonstration:

    .. image:: https://img.youtube.com/vi/lEJ6LKOaIFk/sddefault.jpg
        :target: https://www.youtube.com/watch?v=lEJ6LKOaIFk
        :alt: Demo

Table of Contents
=================

.. toctree::
   :numbered:
   :maxdepth: 4

   toc/installation
   toc/structure
   toc/api
