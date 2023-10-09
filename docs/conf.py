# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.append(os.path.abspath('.'))

# -- Project information -----------------------------------------------------

project = 'Better EMR Phone Documentation'
copyright = '2023, Elckarow'
author = 'Elckarow'

# The full version, including alpha/beta/rc tags
release = 'v3.2.0'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.todo',
    'sphinx.ext.extlinks',
    'sphinx.ext.ifconfig',
    'renpydoc',
    'sphinx.ext.intersphinx',
    'sphinx_rtd_theme',
    'sphinx_rtd_dark_mode',
    ]
# Add any paths that contain templates here, relative to this directory.
templates_path = [ ]

# The suffix(es) of source filenames.
source_suffix = ".rst"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [ ]

# The name of the Pygments (syntax highlighting) style to use.
# pygments_style = 'sphinx'
pygments_style = 'default'


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_static_path = ['_static']

html_context = {
  'display_github': True,
  'github_user': 'Elckarow',
  'github_repo': 'Better-EMR-Phone',
}

html_theme = "sphinx_rtd_theme"

#html_theme_path = [sphinx_nervproject_theme.get_html_theme_path()]
#html_theme_path = [sphinx_pdj_theme.get_html_theme_path()]
# sets the darker appearence
# html_theme_options = {
#     'style': 'darker'
# }

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']

highlight_language = "renpy"
master_doc = 'index'