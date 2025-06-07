Command Line Interface
======================

The Illustris Python package includes a powerful command-line interface for data management and documentation tasks.

Overview
--------

The CLI provides two main categories of commands:

- **Data Management**: Download and manage simulation data
- **Documentation**: Build and serve documentation

Basic Usage
-----------

.. code-block:: bash

   illustris [options]

All commands follow the pattern: ``illustris -category -action [arguments]``

Data Commands
-------------

Download Test Data
~~~~~~~~~~~~~~~~~~

Download complete test data for development and testing:

.. code-block:: bash

   illustris -data -test

This downloads the complete TNG50-4 dataset (~5.3 GB) including:

- All 11 snapshot chunks for comprehensive testing
- Group catalog files for halo/subhalo analysis  
- Offsets files for ``loadHalo`` functionality
- SubLink trees for merger analysis
- Automatic file organization and library compatibility

Download Simulation Data
~~~~~~~~~~~~~~~~~~~~~~~~

Download data for specific simulations:

.. code-block:: bash

   # Download latest snapshot for TNG50-4
   illustris -data -load TNG50-4
   
   # Download specific snapshot
   illustris -data -load TNG100-1 -snap 99
   
   # Download latest snapshot for Illustris-1
   illustris -data -load Illustris-1

The CLI automatically:

- Detects all available file chunks
- Downloads snapshot and group catalog files
- Includes optional files (offsets, SubLink trees) when available
- Creates library-compatible file copies
- Provides detailed progress reporting

List Available Data
~~~~~~~~~~~~~~~~~~~

Explore available simulations and snapshots:

.. code-block:: bash

   # List all available simulations
   illustris -data -list-sims
   
   # List snapshots for a specific simulation
   illustris -data -list-snaps TNG50-1
   illustris -data -list-snaps TNG100-1
   illustris -data -list-snaps Illustris-1

Documentation Commands
----------------------

Build Documentation
~~~~~~~~~~~~~~~~~~~

Generate HTML documentation from source:

.. code-block:: bash

   illustris -docs -generate

This builds the complete documentation including:

- API reference from docstrings
- User guides and examples
- Automatically generated module documentation

Serve Documentation
~~~~~~~~~~~~~~~~~~~

Serve documentation locally for development:

.. code-block:: bash

   # Serve on default port (8000)
   illustris -docs -serve
   
   # Serve on custom port
   illustris -docs -serve -p 8080

The documentation will be available at ``http://localhost:8000`` (or your specified port).

Configuration
-------------

API Key Setup
~~~~~~~~~~~~~

Before downloading data, configure your TNG API key:

1. **Get API Key**: Register at https://www.tng-project.org/users/register/
2. **Create .env file**:

   .. code-block:: bash

      cp env.example .env

3. **Edit .env**:

   .. code-block:: bash

      ILLUSTRIS_API_KEY=your_api_key_here
      ILLUSTRIS_DATA_DIR=./data  # Optional: custom data directory

Data Directory
~~~~~~~~~~~~~~

By default, data is stored in ``./data/``. Customize with:

.. code-block:: bash

   # In .env file
   ILLUSTRIS_DATA_DIR=/path/to/your/data
   
   # Or environment variable
   export ILLUSTRIS_DATA_DIR=/path/to/your/data

Advanced Usage
--------------

Download Features
~~~~~~~~~~~~~~~~~

The CLI includes several advanced features:

**Intelligent Chunk Detection**:
  Automatically detects all available file chunks for each simulation

**Progress Reporting**:
  Real-time download progress with file sizes and transfer rates

**Error Handling**:
  Robust error handling with helpful error messages

**Resume Support**:
  Skips already downloaded files (basic resume functionality)

**Library Compatibility**:
  Automatically creates file copies in expected locations

Examples
~~~~~~~~

**Complete Workflow**:

.. code-block:: bash

   # 1. Download test data
   illustris -data -test
   
   # 2. Verify installation
   python -c "import illustris; print('✓ Ready to use')"
   
   # 3. Run tests
   uv run pytest
   
   # 4. Build documentation
   illustris -docs -generate
   
   # 5. Serve documentation
   illustris -docs -serve

**Production Data Download**:

.. code-block:: bash

   # Download multiple simulations
   illustris -data -load TNG50-1 -snap 99
   illustris -data -load TNG100-1 -snap 99
   illustris -data -load TNG300-1 -snap 99

**Exploration Workflow**:

.. code-block:: bash

   # Explore available data
   illustris -data -list-sims
   
   # Check snapshots for interesting simulation
   illustris -data -list-snaps TNG50-1
   
   # Download specific snapshot
   illustris -data -load TNG50-1 -snap 50

Output Examples
---------------

Successful Download
~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   $ illustris -data -test
   Downloading complete test data (TNG50-4, snapshot 99)...
   This includes multiple snapshot files, group catalogs, and offsets for comprehensive testing.
   
   Downloading snapdir_099/snap_099.0.hdf5...
   ✓ Downloaded snap_099.0.hdf5 (499.1 MB)
   ✓ Downloaded: snapdir_099/snap_099.0.hdf5
   
   [... more files ...]
   
   📊 Download Summary:
     Required files: 4/4
     Optional files: 2/2
   
   ✓ Successfully downloaded complete test data to data\TNG50-4\output
     - Multiple snapshot files for loadSubset testing
     - Group catalog files for halo/subhalo analysis
     - 2 optional files for advanced testing
     - Additional copies created for library compatibility
   
   Use this path in your tests: data\TNG50-4\output
   All tests should now pass with this complete dataset!

Simulation Listing
~~~~~~~~~~~~~~~~~~

.. code-block:: text

   $ illustris -data -list-sims
   Available simulations:

   📊 TNG Project:
     • TNG50-1 (51.7 Mpc/h, 2160³ particles)
       Full snapshot: 2.7 TB, Total data: ~320 TB
     • TNG50-2 (51.7 Mpc/h, 1080³ particles)
       Full snapshot: 350 GB, Total data: 18 TB
     • TNG50-3 (51.7 Mpc/h, 540³ particles)
       Full snapshot: 44 GB, Total data: 7.5 TB
     • TNG50-4 (51.7 Mpc/h, 270³ particles)
       Full snapshot: 5.2 GB, Total data: 0.6 TB
     • TNG100-1 (75.0 Mpc/h, 1820³ particles)
       Full snapshot: 1.7 TB, Total data: 128 TB
     • TNG100-2 (75.0 Mpc/h, 910³ particles)
       Full snapshot: 215 GB, Total data: 14 TB
     • TNG100-3 (75.0 Mpc/h, 455³ particles)
       Full snapshot: 27 GB, Total data: 1.5 TB
     • TNG300-1 (205.0 Mpc/h, 2500³ particles)
       Full snapshot: 4.1 TB, Total data: 235 TB
     • TNG300-2 (205.0 Mpc/h, 1250³ particles)
       Full snapshot: 512 GB, Total data: 31 TB
     • TNG300-3 (205.0 Mpc/h, 625³ particles)
       Full snapshot: 63 GB, Total data: 4 TB

   🔬 Original Illustris:
     • Illustris-1 (106.5 Mpc/h, 1820³ particles)
       Full snapshot: 1.5 TB, Total data: 204 TB
     • Illustris-2 (106.5 Mpc/h, 910³ particles)
       Full snapshot: 176 GB, Total data: 24 TB
     • Illustris-3 (106.5 Mpc/h, 455³ particles)
       Full snapshot: 22 GB, Total data: 3 TB

   ✓ TNG API is accessible

Troubleshooting
---------------

Common Issues
~~~~~~~~~~~~~

**API Key Errors**:

.. code-block:: text

   ✗ API key not found. Please set ILLUSTRIS_API_KEY in .env file

**Solution**: Create ``.env`` file with your API key

**Permission Errors**:

.. code-block:: text

   ✗ Permission denied: data/TNG50-4/output/

**Solution**: Check directory permissions:

.. code-block:: bash

   chmod 755 data/
   # or choose different directory
   export ILLUSTRIS_DATA_DIR=/tmp/illustris_data

**Network Errors**:

.. code-block:: text

   ✗ Failed to download: Connection timeout

**Solution**: Check internet connection and try again. Large files may take time.

**Incomplete Downloads**:

.. code-block:: bash

   # Remove corrupted files and re-download
   rm -rf data/TNG50-4/output/snapdir_099/
   illustris -data -test

Getting Help
~~~~~~~~~~~~

.. code-block:: bash

   # Show help
   illustris --help
   
   # Show version
   python -c "import illustris; print(illustris.__version__)"

For additional support:

- Check the `GitHub issues <https://github.com/illustristng/illustris_python/issues>`_
- Review the `troubleshooting guide <installation.html#troubleshooting>`_
- Consult the `TNG project documentation <https://www.tng-project.org/data/>`_ 