Installation
============

Broh5 can be installed using `pip <https://pypi.org/project/broh5/>`__,
`conda <https://anaconda.org/conda-forge/broh5>`__, or directly from the
`source <https://github.com/algotom/broh5>`__. Users can also generate a
standalone executable file for convenient usage.

Using pip
---------

.. code-block:: console

    pip install broh5

Once installed, launching Broh5 with

.. code-block:: console

    broh5

Using conda
-----------

.. code-block:: console

    conda install -c conda-forge broh5


Same as above, launching Broh5 with:

.. code-block:: console

    broh5

Installing from source
----------------------

To install broh5 from source using Conda:

    +   Set up a conda environment:

        First, ensure that you have Conda installed.
        If not, install `Miniconda <https://docs.conda.io/projects/miniconda/en/latest/>`__
        or `Anaconda <https://www.anaconda.com/download>`__.

        Create a new Conda environment. This ensures that any dependencies
        don't interfere with your current Python projects. You can name it whatever
        you like, but for this example, we'll call it *broh5*

        .. code-block:: console

            conda create -n broh5 python=3.10
            conda activate broh5

    +   Clone the Repository:

        Use git to clone the broh5 repository

        .. code-block:: console

            git clone https://github.com/algotom/broh5.git broh5

        Navigate to the cloned directory

        .. code-block:: console

            cd broh5

    +   Install the software:

        Using *setup.py* file by

        .. code-block:: console

            python setup.py install

        or pip

        .. code-block:: console

            pip install .


        Troubleshooting:

        *   If you encounter an error related to *fastapi* and *anyio*, add the
            line "anyio<4.0.0" to the dependencies in *setup.py*.
        *   If you encounter an error related to *matplotlib* and either *PyQt5*
            or *PySide2*, install PySide2 using the command: `pip install PySide2`.

Generating a standalone executable file
---------------------------------------

If you would like to creating a standalone executable for broh5:

    +   Install PyInstaller

        .. code-block:: console

            pip install pyinstaller

    +   Generate the executable file by running `generate_exe.py <https://github.com/algotom/broh5/blob/main/generate_exe.py>`__
        at the cloned directory

        .. code-block:: console

            python generate_exe.py

    +   Navigate to the **dist** directory and run

        .. code-block:: console

            broh5.exe

        the generated file can be moved to another location for more convenient usage.
