# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
import django
sys.path.insert(0, os.path.abspath('/app'))
os.environ['DJANGO_SETTINGS_MODULE'] = '{{project_name}}.settings'
django.setup()
# -- Project information -----------------------------------------------------

project = '{{project_name}}'
copyright = '2024, The President and Fellows of Harvard College'
author = 'Aaron Kitzmiller'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinxcontrib.openapi',
    'sphinxcontrib_django',
    'sphinx.ext.autosectionlabel',
    'recommonmark',
]

autosectionlabel_prefix_document = True

autodoc_member_order = 'bysource'

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "alabaster"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# --- Do not process common Django functions in autodoc ----------------------
def skip_common_django(app, what, name, obj, skip, options):
    '''
    Don't need these
    '''
    skips = [
        'get_next_by_created',
        'get_next_by_end_date',
        'get_next_by_start_date',
        'get_next_by_updated',
        'get_previous_by_created',
        'get_previous_by_end_date',
        'get_previous_by_start_date',
        'get_previous_by_updated',
        'DoesNotExist',
        'MultipleObjectsReturned',
        '__doc__',
        '__module__',
        '_meta',
        'objects',
        '__dict__',
        '__weakref__',
        '_declared_fields',
    ]
    if what == 'class':
        if name in skips or name[-3:] == '_id' or name[-4:] == '_ptr':
            return True
    return False

globaltoc_maxdepth = 3

# -- Extension configuration -------------------------------------------------
def setup(app):
    app.add_css_file('css/ifx.css')
    app.connect('autodoc-skip-member', skip_common_django)
