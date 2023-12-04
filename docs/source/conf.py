#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Project documentation build configuration file, created by
# sphinx-quickstart on Fri Mar 13 16:29:32 2015.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import sys
import os
sys.path.insert(0, os.path.abspath('../..'))

# -- General configuration ------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'nbsphinx',
    'sphinx.ext.autodoc',
    'sphinx.ext.mathjax',
    'sphinx.ext.todo',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'autoapi.extension'
]

# Napoleon settings
napoleon_numpy_docstring = True
napoleon_google_docstring = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = False
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = False
napoleon_use_rtype = False

todo_include_todos = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# General information about the project.
Affiliation = 'NSLS-II, Brookhaven National Lab, US'
project = 'Broh5'
copyright = '2023, Nghia T. Vo, ' + Affiliation

# The full version, including alpha/beta/rc tags.
release = ''

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build', 'build']

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.

html_theme = 'sphinx_rtd_theme'
html_theme_options = {'includehidden': False}

# Output file base name for HTML help builder.
htmlhelp_basename = project + 'doc'

latex_documents = [
    ('index',
     project + '.tex',
     project + ' Documentation',
     Affiliation, 'manual'),
]

man_pages = [
    ('index', project,
     project + u' Documentation',
     [Affiliation, ], 1)
]

texinfo_documents = [
    ('index',
     project,
     project + ' Documentation',
     Affiliation,
     project,
     'Broh5'),
]

autodoc_mock_imports = [
    'h5py',
    'numpy',
    'hdf5plugin',
    'matplotlib',
    'nicegui',
    'PIL',
    'broh5'
]

autoapi_dirs = ['../..']

autodoc_member_order = 'bysource'
numfig = True
numfig_secnum_depth = 2
