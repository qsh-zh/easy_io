"""Configuration for the easy_io Sphinx documentation build.

The layout mirrors the Jacinle docs structure with a landing page, usage
guide, and API reference. The site uses PyData Sphinx Theme with a light
customisation for navigation tabs.
"""

from __future__ import annotations

import importlib.metadata
import os
import sys
from datetime import datetime

PROJECT_ROOT = os.path.abspath(os.path.join(__file__, "..", ".."))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "easy_io"))

project = "easy_io"
author = "Qsh"
COPYRIGHT_NOTICE = f"{datetime.now():%Y}, {author}"
globals()["copyright"] = COPYRIGHT_NOTICE

try:
    release = importlib.metadata.version("easy_io")
except importlib.metadata.PackageNotFoundError:  # pragma: no cover - during local builds
    release = "0.1.0"

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx_autodoc_typehints",
    "sphinx_copybutton",
]

autosummary_generate = True
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
}
autodoc_typehints = "description"

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable/", None),
    "boto3": ("https://boto3.amazonaws.com/v1/documentation/api/latest/", None),
}

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]
html_theme_options = {
    "logo": {
        "text": "easy_io",
    },
    "show_prev_next": False,
    "navbar_end": ["theme-switcher", "navbar-icon-links"],
}

html_context = {
    "github_url": "https://github.com/qsh-zh/easy_io",
    "github_user": "qsh-zh",
    "github_repo": "easy_io",
    "default_mode": "light",
}

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

todo_include_todos = True
