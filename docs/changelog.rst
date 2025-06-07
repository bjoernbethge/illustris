Changelog
=========

All notable changes to this project will be documented in this file.

Version 0.1.0 (2025-01-XX)
---------------------------

**Initial Release**

This is the first release of the modernized Illustris Python package.

Added
~~~~~

**Core Features**:

- Complete Python package for reading Illustris simulation data
- Support for snapshots, group catalogs, and merger trees
- Compatibility with all Illustris simulations (Illustris-1, TNG50, TNG100, TNG300)

**Command Line Interface**:

- ``illustris -data -test`` - Download complete test data
- ``illustris -data -load SIMULATION -snap NUMBER`` - Download simulation data
- ``illustris -data -list-sims`` - List available simulations
- ``illustris -data -list-snaps SIMULATION`` - List snapshots
- ``illustris -docs -generate`` - Build documentation
- ``illustris -docs -serve`` - Serve documentation locally

**Data Management**:

- Automatic TNG API integration with authentication
- Intelligent chunk detection for all simulations
- Progress reporting with file sizes and transfer rates
- Automatic file organization and library compatibility
- Support for optional files (offsets, SubLink trees)

**Testing Infrastructure**:

- Modern pytest-based test suite
- Session-scoped fixtures for data management
- Automatic test adaptation based on available data
- 26 comprehensive tests with 100% pass rate
- Coverage reporting with pytest-cov

**Documentation**:

- Modern Sphinx documentation with Read the Docs theme
- Comprehensive user guides and examples
- Complete API reference with auto-generated documentation
- Installation guide with troubleshooting
- CLI reference with examples

**Development Tools**:

- uv-based dependency management
- Black code formatting
- Ruff linting
- MyPy type checking
- Pre-commit hooks support

Technical Details
~~~~~~~~~~~~~~~~~

**Dependencies**:

- h5py ≥3.14.0 - HDF5 file reading
- numpy ≥2.2.6 - Numerical computations
- six ≥1.17.0 - Python 2/3 compatibility
- httpx ≥0.28.1 - HTTP client for API access
- python-dotenv ≥1.0.0 - Environment variable management

**API Modules**:

- ``illustris.snapshot`` - Particle data loading
- ``illustris.groupcat`` - Halo and subhalo catalogs
- ``illustris.sublink`` - Merger tree analysis
- ``illustris.lhalotree`` - Legacy tree format support
- ``illustris.cartesian`` - Cartesian grid data
- ``illustris.util`` - Utility functions

**Data Support**:

- All TNG simulations (TNG50-1/2/3/4, TNG100-1/2/3, TNG300-1/2/3)
- Original Illustris simulations (Illustris-1/2/3)
- Complete snapshot data with all particle types
- Group catalogs with halo and subhalo properties
- SubLink merger trees for galaxy evolution
- Offsets files for efficient halo loading

**Performance Features**:

- Memory-efficient data loading
- Spatial filtering with bounding boxes
- Field selection to minimize memory usage
- Parallel download support
- Resume capability for interrupted downloads

Migration Notes
~~~~~~~~~~~~~~~

This release modernizes the original Illustris Python tools:

**Breaking Changes**:

- CLI changed from ``illustris-docs`` to ``illustris``
- Test framework changed from nose to pytest
- Requires Python 3.11+ (was Python 2.7+)

**Compatibility**:

- All original API functions remain unchanged
- Existing analysis scripts should work without modification
- Data file formats and paths are identical

**New Requirements**:

- TNG API key required for data downloads
- ``.env`` file for configuration
- Modern Python environment (3.11+)

Known Issues
~~~~~~~~~~~~

- Large file downloads may timeout on slow connections
- Some legacy test files removed (nose-based tests)
- Documentation theme requires internet connection for fonts

Future Plans
~~~~~~~~~~~~

**Version 0.2.0** (Planned):

- Visualization utilities
- Parallel processing improvements
- Additional analysis examples
- Performance optimizations

**Version 0.3.0** (Planned):

- Support for additional file formats
- Interactive Jupyter notebook examples
- Advanced analysis tools
- Memory usage optimizations

Contributors
~~~~~~~~~~~~

- Illustris Team - Original codebase and algorithms
- TNG Project - API and data infrastructure
- Community - Testing and feedback

For detailed commit history, see the `GitHub repository <https://github.com/illustristng/illustris_python>`_. 