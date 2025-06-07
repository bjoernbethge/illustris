Installation
============

Requirements
------------

- Python 3.11 or higher
- Git (for cloning the repository)

Dependencies
~~~~~~~~~~~~

The package automatically installs these dependencies:

- **h5py** (≥3.14.0) - HDF5 file reading
- **numpy** (≥2.2.6) - Numerical computations  
- **six** (≥1.17.0) - Python 2/3 compatibility
- **httpx** (≥0.28.1) - HTTP client for API access
- **python-dotenv** (≥1.0.0) - Environment variable management

Installation Methods
--------------------

Using uv (Recommended)
~~~~~~~~~~~~~~~~~~~~~~

`uv <https://docs.astral.sh/uv/>`_ is a fast Python package manager:

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/illustristng/illustris_python.git
   cd illustris_python
   
   # Install with uv
   uv sync

Using pip
~~~~~~~~~

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/illustristng/illustris_python.git
   cd illustris_python
   
   # Install in development mode
   pip install -e .

Development Installation
~~~~~~~~~~~~~~~~~~~~~~~~

For development with additional tools:

.. code-block:: bash

   # With uv
   uv sync --group dev
   
   # With pip
   pip install -e ".[dev]"

This installs additional development dependencies:

- **pytest** - Testing framework
- **sphinx** - Documentation generation
- **black** - Code formatting
- **ruff** - Linting
- **mypy** - Type checking

Configuration
-------------

API Access
~~~~~~~~~~

To download data from the TNG project, you need an API key:

1. Register at https://www.tng-project.org/users/register/
2. Get your API key from your profile
3. Create a ``.env`` file:

.. code-block:: bash

   # Copy the example configuration
   cp env.example .env

4. Edit ``.env`` and add your API key:

.. code-block:: bash

   ILLUSTRIS_API_KEY=your_api_key_here
   ILLUSTRIS_DATA_DIR=./data  # Optional: custom data directory

Data Directory
~~~~~~~~~~~~~~

By default, data is stored in ``./data/``. You can customize this:

.. code-block:: bash

   # In .env file
   ILLUSTRIS_DATA_DIR=/path/to/your/data

   # Or set environment variable
   export ILLUSTRIS_DATA_DIR=/path/to/your/data

Verification
------------

Test your installation:

.. code-block:: bash

   # Test basic functionality
   python -c "import illustris; print('✓ Installation successful')"
   
   # Run tests (requires test data)
   illustris -data -test  # Download test data first
   uv run pytest         # Run test suite

Troubleshooting
---------------

Common Issues
~~~~~~~~~~~~~

**Import Error**:

.. code-block:: bash

   # Make sure you're in the right environment
   which python
   pip list | grep illustris

**Permission Denied**:

.. code-block:: bash

   # Check data directory permissions
   ls -la data/
   chmod 755 data/

**API Key Issues**:

.. code-block:: bash

   # Verify your .env file
   cat .env
   # Make sure ILLUSTRIS_API_KEY is set correctly

**Missing Dependencies**:

.. code-block:: bash

   # Reinstall dependencies
   uv sync --reinstall
   # or
   pip install -e . --force-reinstall

Getting Help
~~~~~~~~~~~~

If you encounter issues:

1. Check the `troubleshooting section <https://github.com/illustristng/illustris_python#troubleshooting>`_
2. Search existing `issues <https://github.com/illustristng/illustris_python/issues>`_
3. Create a new issue with:
   - Your Python version (``python --version``)
   - Your operating system
   - Complete error message
   - Steps to reproduce the problem 