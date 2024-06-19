# -*- coding: utf-8 -*-
#
# LazyLLM documentation build configuration file

import pkg_resources
import os
import sys

sys.path.insert(0, os.path.abspath("../"))

version = "v" + pkg_resources.get_distribution("lazyllm").version

project = u'LazyLLM'
copyright = u'2024, SenseTime Research'
author = u'SenseTime Research'

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.coverage",
    "sphinx.ext.autodoc.typehints",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx_rtd_theme",
    "sphinx.ext.mathjax",
    "m2r2",
    "myst_nb",
    "sphinxcontrib.autodoc_pydantic",
    # "sphinx_reredirects",
    "sphinx_automodapi.automodapi",
    # "sphinxcontrib.gtagjs",
]

# automodapi requires this to avoid duplicates apparently
numpydoc_show_class_members = False


myst_heading_anchors = 5
# TODO: Fix the non-consecutive header level in our docs, until then
# disable the sphinx/myst warnings
suppress_warnings = ["myst.header"]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "DOCS_README.md"]
html_theme = "furo"
html_title = project + " " + version
html_static_path = ["_static"]

html_css_files = [
    "css/custom.css",
    "css/algolia.css",
    "https://cdn.jsdelivr.net/npm/@docsearch/css@3",
]
html_js_files = [
    "js/mendablesearch.js",
    (
        "https://cdn.jsdelivr.net/npm/@docsearch/js@3.3.3/dist/umd/index.js",
        {"defer": "defer"},
    ),
    ("js/algolia.js", {"defer": "defer"}),
    ("js/leadfeeder.js", {"defer": "defer"}),
]
html_permalinks_icon = "#"
nb_execution_mode = "off"
autodoc_pydantic_model_show_json_error_strategy = "coerce"
nitpicky = True

# language = 'cn'
# exclude_patterns = []
# pygments_style = 'sphinx'
# todo_include_todos = True
# html_static_path = ['_static']
# html_sidebars = {
#     '**': [
#         'relations.html',  # needs 'show_related': True theme option to display
#         'searchbox.html',
#     ]
# }
# htmlhelp_basename = 'LazyLLMdoc'
# latex_elements = {
# }

# latex_documents = [
#     (master_doc, 'LazyLLM.tex', u'LazyLLM Documentation',
#      u'SenseTime Research', 'manual'),
# ]


# man_pages = [
#     (master_doc, 'lazyllm', u'LazyLLM Documentation',
#      [author], 1)
# ]

# texinfo_documents = [
#     (master_doc, 'LazyLLM', u'LazyLLM Documentation',
#      author, 'LazyLLM', 'One line description of project.',
#      'Miscellaneous'),
# ]
