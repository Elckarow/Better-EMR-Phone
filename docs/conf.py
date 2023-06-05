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
sys.path.insert(0, os.path.abspath('..'))
sys.path.append(os.path.abspath('.'))
on_rtd = os.environ.get('READTHEDOCS') == 'True'


# -- Project information -----------------------------------------------------

project = 'Better EMR Phone Documentation'
copyright = '2023, Elckarow'
author = 'Elckarow'

# The full version, including alpha/beta/rc tags
release = 'v3.0'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
# Add napoleon to the extensions list
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.coverage', 'sphinx.ext.napoleon',
    'recommonmark', 'sphinx_rtd_theme',
    'sphinx_markdown_tables',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.todo',
    'renpydoc',
    'sphinx.ext.githubpages',]
napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_type_aliases = None

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
source_parsers = {
    '.md': 'recommonmark.parser.CommonMarkParser',
}

source_suffix = ['.rst', '.md']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
# pygments_style = 'sphinx'
pygments_style = 'default'


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_static_path = ['_static']
import sphinx_nervproject_theme
html_context = {
    'css_files': [
        '_static/theme_overrides.css',  # override wide tables in RTD theme
        ],
    }
if True or on_rtd:
    html_theme = "sphinx_rtd_theme"
else:
    html_theme = "nervproject"
#html_theme_path = [sphinx_nervproject_theme.get_html_theme_path()]
#html_theme_path = [sphinx_pdj_theme.get_html_theme_path()]

html_sidebars = { '**': ['globaltoc.html',
                        'relations.html',
                        'sourcelink.html',
                        'searchbox.html'
                        ] }

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