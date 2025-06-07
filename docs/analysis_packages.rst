Analysis Packages and Tools
============================

This page provides an overview of analysis packages and tools available for working with IllustrisTNG data, based on community recommendations and official guidance.

Recommended Analysis Packages
------------------------------

The TNG team has provided guidance on various analysis packages for working with Arepo/TNG data:

illustris (This Package - Modernized Fork)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Best for**: Modern TNG analysis, CLI tools, comprehensive testing

- ✅ **Modernized fork**: Based on original TNG package with significant enhancements
- ✅ **Full API compatibility**: All original functions work unchanged
- ✅ **Modern CLI tools**: Async downloading, data management, documentation
- ✅ **Comprehensive testing**: pytest fixtures, 26 tests, full coverage
- ✅ **Complete documentation**: Examples, troubleshooting, package comparisons
- ✅ **Developer-friendly**: uv support, modern Python practices

.. code-block:: python

   import illustris
   
   # Load merger tree
   tree = illustris.sublink.loadTree(basePath, snap, subhalo_id)
   
   # Load group catalogs
   halos = illustris.groupcat.loadHalos(basePath, snap)

scida
~~~~~

**Best for**: Large-scale analysis, automatic scaling, general-purpose

- ✅ **Dask integration**: Automatic scaling for large computations
- ✅ **General purpose**: Not limited to Arepo, supports multiple formats
- ✅ **Active development**: Modern Python package with regular updates
- ⚠️ **Learning curve**: More complex setup for simple tasks

.. code-block:: python

   import scida
   
   # Load simulation with automatic chunking
   ds = scida.load("path/to/simulation")

paicos
~~~~~~

**Best for**: Arepo-specific analysis, visualization tasks

- ✅ **Arepo-specific**: Built specifically for Arepo simulations
- ✅ **Visualization tools**: Built-in plotting and visualization features
- ✅ **Specialized functions**: Arepo-specific analysis routines
- ⚠️ **Limited scope**: Focused on Arepo, less general-purpose

yt
~~

**Best for**: Complex analysis workflows, advanced users

- ✅ **Feature-rich**: Most comprehensive analysis package
- ✅ **Mature ecosystem**: Large community and extensive documentation
- ⚠️ **TNG compatibility**: Less suited for TNG-specific workflows
- ⚠️ **Complexity**: Steep learning curve for simple tasks

sator
~~~~~

**Status**: Not recommended (no longer under active development)

Package Comparison
------------------

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 15 15 20

   * - Package
     - TNG Support
     - Learning Curve
     - Performance
     - Active Dev
     - Best Use Case
   * - illustris_python
     - ⭐⭐⭐
     - Easy
     - Optimized
     - ✅
     - TNG-specific analysis
   * - scida
     - ⭐⭐
     - Medium
     - Excellent
     - ✅
     - Large-scale studies
   * - paicos
     - ⭐⭐⭐
     - Medium
     - Good
     - ✅
     - Arepo visualization
   * - yt
     - ⭐
     - Hard
     - Good
     - ✅
     - Complex workflows
   * - sator
     - ⭐⭐
     - Medium
     - Good
     - ❌
     - Not recommended

Choosing the Right Package
--------------------------

For TNG Beginners
~~~~~~~~~~~~~~~~~

**Start with illustris** (this modernized fork):

1. **Full compatibility**: All original TNG functions work unchanged
2. **Modern tooling**: CLI tools for easy data management
3. **Complete documentation**: Comprehensive examples and guides
4. **Easy setup**: Modern Python practices with uv support

.. code-block:: python

   # Simple and straightforward
   import illustris
   
   subhalos = illustris.groupcat.loadSubhalos(basePath, snap)
   tree = illustris.sublink.loadTree(basePath, snap, subhalo_id)

For Large-Scale Analysis
~~~~~~~~~~~~~~~~~~~~~~~~

**Consider scida** for:

- Multi-terabyte datasets
- Parallel processing needs
- Cross-simulation comparisons
- Memory-efficient workflows

.. code-block:: python

   # Automatic chunking and parallel processing
   import scida
   
   ds = scida.load("TNG300-1")
   result = ds.compute_large_analysis()  # Automatically parallelized

For Visualization-Heavy Work
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Consider paicos** for:

- Arepo-specific visualizations
- Built-in plotting functions
- Specialized Arepo analysis

For Advanced Users
~~~~~~~~~~~~~~~~~~

**Consider yt** for:

- Complex multi-code analysis
- Advanced visualization needs
- Integration with other simulation codes

Common Analysis Patterns
------------------------

Snapshot Analysis
~~~~~~~~~~~~~~~~~

.. code-block:: python

   # illustris approach
   import illustris
   
   # Load specific fields efficiently
   gas = illustris.snapshot.loadSubset(
       basePath, snap, "gas",
       fields=["Coordinates", "Masses", "Density"]
   )
   
   # Spatial filtering with bounding boxes
   bbox = [[x_min, x_max], [y_min, y_max], [z_min, z_max]]
   region_gas = illustris.snapshot.loadSubset(
       basePath, snap, "gas", fields=["Density"], bbox=bbox
   )

Halo Analysis
~~~~~~~~~~~~~

.. code-block:: python

   # Load group catalogs
   halos = illustris.groupcat.loadHalos(basePath, snap)
   subhalos = illustris.groupcat.loadSubhalos(basePath, snap)
   
   # Load particles in specific halos
   halo_stars = illustris.snapshot.loadHalo(
       basePath, snap, halo_id, "stars"
   )

Merger Tree Analysis
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # SubLink trees (recommended)
   tree = illustris.sublink.loadTree(basePath, snap, subhalo_id)
   
   # LHaloTree alternative
   tree = illustris.lhalotree.loadTree(basePath, snap, subhalo_id)
   
   # Both use identical API
   mass_history = tree['SubhaloMass']
   snap_history = tree['SnapNum']

Performance Considerations
--------------------------

Memory Management
~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Load only needed fields
   minimal_data = illustris.snapshot.loadSubset(
       basePath, snap, "gas",
       fields=["Coordinates"]  # Only what you need
   )
   
   # Use spatial cuts
   bbox = [[center[i]-size, center[i]+size] for i in range(3)]
   region_data = illustris.snapshot.loadSubset(
       basePath, snap, "gas", bbox=bbox
   )

Efficient Workflows
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Process snapshots in batches
   for snap in range(90, 100):  # Last 10 snapshots
       subhalos = illustris.groupcat.loadSubhalos(
           basePath, snap, fields=["SubhaloMass"]
       )
       # Process and save results
       process_snapshot(subhalos, snap)

Integration Examples
--------------------

Using Multiple Packages
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Use illustris for data loading
   import illustris
   
   # Load with official tools
   gas = illustris.snapshot.loadSubset(basePath, snap, "gas")
   
   # Then use other packages for analysis
   import numpy as np
   import matplotlib.pyplot as plt
   
   # Standard scientific Python workflow
   density_map = create_density_projection(gas)
   plt.imshow(density_map)

Best Practices
--------------

1. **Start Simple**: Begin with illustris for TNG-specific tasks
2. **Know Your Data**: Understand TNG data structure before using general tools
3. **Optimize Early**: Use field selection and spatial cuts from the beginning
4. **Test Small**: Develop on TNG50-4 before scaling to larger simulations
5. **Document Workflows**: Keep track of analysis steps for reproducibility

Community Resources
-------------------

- **TNG Forum**: https://www.tng-project.org/data/forum/ - Official support
- **GitHub Issues**: Package-specific bug reports and feature requests
- **Documentation**: Each package has comprehensive documentation
- **Examples**: Look for Jupyter notebooks and example scripts

Getting Help
------------

1. **Check Documentation**: Most questions are answered in package docs
2. **Search Forums**: TNG forum has extensive Q&A history
3. **GitHub Issues**: For package-specific technical problems
4. **Community**: Ask on relevant scientific computing forums

Summary
-------

For most TNG users, **this modernized illustris fork** provides the best balance of simplicity, modern tooling, and TNG-specific features. Consider other packages when you need:

- **scida**: Large-scale parallel processing
- **paicos**: Arepo-specific visualization
- **yt**: Complex multi-code workflows

**Recommendation**: Start with this modernized fork for the best developer experience, then consider specialized tools only when specific advanced features are needed. 