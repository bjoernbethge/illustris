Illustris Documentation
========================

.. image:: https://img.shields.io/badge/python-3.11+-blue.svg
   :target: https://www.python.org/downloads/
   :alt: Python Version

.. image:: https://img.shields.io/badge/license-MIT-green.svg
   :target: https://github.com/illustristng/illustris_python/blob/main/LICENSE.md
   :alt: License

.. image:: https://img.shields.io/badge/fork-modernized-brightgreen.svg
   :alt: Modernized Fork

**Illustris** is a modernized and extended fork of the original `illustris_python <https://github.com/illustristng/illustris_python>`_ package. It provides comprehensive tools for reading and analyzing data from the Illustris cosmological simulation suite.

.. note::
   **Fork Features**: This modernized version adds CLI tools, async downloading, comprehensive testing, and complete documentation while maintaining full API compatibility with the original package.

.. note::
   This package supports all Illustris simulations: **Illustris-1**, **TNG50**, **TNG100**, and **TNG300**.

Quick Start
-----------

Install the package and download test data:

.. code-block:: bash

   # Install with uv (recommended)
   uv sync
   
   # Download complete test data
   illustris -data -test

Load simulation data in Python:

.. code-block:: python

   import illustris
   
   # Load gas particle data
   gas = illustris.snapshot.loadSubset(
       "data/TNG50-4/output", 99, "gas", 
       fields=["Coordinates", "Masses"]
   )
   
   # Load halo catalog
   halos = illustris.groupcat.loadHalos(
       "data/TNG50-4/output", 99,
       fields=["GroupMass", "GroupPos"]
   )

Features
--------

🚀 **Easy Data Access**
   Simple Python API for loading simulation data

📊 **Complete Coverage**
   Support for snapshots, group catalogs, and merger trees

🛠️ **CLI Tools**
   Command-line interface for data management

🧪 **Modern Testing**
   Comprehensive test suite with pytest

📚 **Rich Documentation**
   Detailed examples and API reference

User Guide
----------

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   installation
   quickstart
   examples
   cli
   simulation_sizes
   analysis_packages
   troubleshooting

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/modules
   api/illustris

.. toctree::
   :maxdepth: 1
   :caption: Development

   contributing
   changelog

Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

