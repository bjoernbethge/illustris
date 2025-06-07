Simulation Sizes and Data Volumes
==================================

This page provides detailed information about the sizes and data volumes of all available Illustris and TNG simulations.

Overview
--------

The IllustrisTNG project consists of three main simulation volumes (TNG50, TNG100, TNG300) plus the original Illustris simulations. Each simulation comes in multiple resolution levels, providing a range of options for different scientific applications.

TNG Project Simulations
------------------------

TNG50 Series
~~~~~~~~~~~~

**TNG50** simulations focus on high-resolution galaxy formation in a smaller volume:

.. list-table::
   :header-rows: 1
   :widths: 15 15 15 20 20 15

   * - Simulation
     - Box Size
     - Particles
     - Full Snapshot
     - Total Volume
     - Best For
   * - TNG50-1
     - 51.7 Mpc/h
     - 2160³
     - 2.7 TB
     - ~320 TB
     - Highest resolution galaxy studies
   * - TNG50-2
     - 51.7 Mpc/h
     - 1080³
     - 350 GB
     - 18 TB
     - High-res studies, manageable size
   * - TNG50-3
     - 51.7 Mpc/h
     - 540³
     - 44 GB
     - 7.5 TB
     - Medium resolution studies
   * - TNG50-4
     - 51.7 Mpc/h
     - 270³
     - 5.2 GB
     - 0.6 TB
     - Testing and development

TNG100 Series
~~~~~~~~~~~~~~

**TNG100** simulations provide a balance between resolution and volume:

.. list-table::
   :header-rows: 1
   :widths: 15 15 15 20 20 15

   * - Simulation
     - Box Size
     - Particles
     - Full Snapshot
     - Total Volume
     - Best For
   * - TNG100-1
     - 75.0 Mpc/h
     - 1820³
     - 1.7 TB
     - 128 TB
     - Flagship simulation, balanced studies
   * - TNG100-2
     - 75.0 Mpc/h
     - 910³
     - 215 GB
     - 14 TB
     - Medium resolution, good statistics
   * - TNG100-3
     - 75.0 Mpc/h
     - 455³
     - 27 GB
     - 1.5 TB
     - Lower resolution studies

TNG300 Series
~~~~~~~~~~~~~~

**TNG300** simulations offer the largest volumes for rare object studies:

.. list-table::
   :header-rows: 1
   :widths: 15 15 15 20 20 15

   * - Simulation
     - Box Size
     - Particles
     - Full Snapshot
     - Total Volume
     - Best For
   * - TNG300-1
     - 205.0 Mpc/h
     - 2500³
     - 4.1 TB
     - 235 TB
     - Massive halos, rare objects
   * - TNG300-2
     - 205.0 Mpc/h
     - 1250³
     - 512 GB
     - 31 TB
     - Large volume studies
   * - TNG300-3
     - 205.0 Mpc/h
     - 625³
     - 63 GB
     - 4 TB
     - Large-scale structure

Original Illustris Simulations
-------------------------------

The original **Illustris** simulations that preceded TNG:

.. list-table::
   :header-rows: 1
   :widths: 15 15 15 20 20 15

   * - Simulation
     - Box Size
     - Particles
     - Full Snapshot
     - Total Volume
     - Best For
   * - Illustris-1
     - 106.5 Mpc/h
     - 1820³
     - 1.5 TB
     - 204 TB
     - Original flagship simulation
   * - Illustris-2
     - 106.5 Mpc/h
     - 910³
     - 176 GB
     - 24 TB
     - Medium resolution studies
   * - Illustris-3
     - 106.5 Mpc/h
     - 455³
     - 22 GB
     - 3 TB
     - Lower resolution studies

Data Organization
-----------------

Snapshots
~~~~~~~~~

Each simulation contains **100 snapshots** from z=127 to z=0, with two types:

- **Full snapshots** (20 total): Complete particle data with all fields
- **Mini snapshots** (80 total): Reduced field set for smaller file sizes

File Structure
~~~~~~~~~~~~~~

Data is organized in chunks for manageable file sizes:

- **TNG50-4**: 11 chunks per snapshot (smallest, good for testing)
- **TNG100-1**: 448 chunks per snapshot (flagship simulation)
- **TNG300-1**: 600 chunks per snapshot (largest volume)

Storage Requirements
--------------------

Recommended Storage by Use Case
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 25 25 25

   * - Use Case
     - Recommended Simulation
     - Single Snapshot
     - Full Dataset
   * - Testing/Development
     - TNG50-4
     - 5.2 GB
     - 0.6 TB
   * - Galaxy Studies
     - TNG50-2 or TNG100-2
     - 350 GB / 215 GB
     - 18 TB / 14 TB
   * - Large-Scale Structure
     - TNG300-2
     - 512 GB
     - 31 TB
   * - Highest Resolution
     - TNG50-1
     - 2.7 TB
     - ~320 TB

Download Considerations
-----------------------

Network Requirements
~~~~~~~~~~~~~~~~~~~~

Estimated download times at different speeds:

.. list-table::
   :header-rows: 1
   :widths: 20 20 20 20 20

   * - Connection Speed
     - TNG50-4 (0.6 TB)
     - TNG100-2 (14 TB)
     - TNG100-1 (128 TB)
     - TNG300-1 (235 TB)
   * - 10 Mbps
     - 5.5 days
     - 129 days
     - 3.5 years
     - 6.4 years
   * - 100 Mbps
     - 13 hours
     - 13 days
     - 118 days
     - 216 days
   * - 1 Gbps
     - 1.3 hours
     - 31 hours
     - 12 days
     - 22 days

Partial Downloads
~~~~~~~~~~~~~~~~~

You can download specific components:

- **Single snapshots**: For specific redshift analysis
- **Group catalogs only**: For halo/galaxy property studies  
- **Specific particle types**: Gas, dark matter, stars, or black holes only
- **Specific fields**: Only the data fields you need

CLI Usage
---------

Use the command-line interface to explore and download data:

.. code-block:: bash

   # List all simulations with sizes
   illustris -data -list-sims
   
   # List snapshots for a simulation
   illustris -data -list-snaps TNG50-1
   
   # Download test data (TNG50-4, complete)
   illustris -data -test
   
   # Download specific simulation data
   illustris -data -load TNG50-4 -snap 99

Best Practices
--------------

For New Users
~~~~~~~~~~~~~

1. **Start with TNG50-4**: Download the complete test dataset first
2. **Test your analysis**: Develop and test code on the smallest simulation
3. **Scale up gradually**: Move to larger simulations once your workflow is established

For Large-Scale Studies
~~~~~~~~~~~~~~~~~~~~~~~

1. **Use the API**: For targeted data extraction without full downloads
2. **Consider TNG-Lab**: Use the online JupyterLab environment for large datasets
3. **Plan storage**: Ensure adequate disk space before starting downloads
4. **Use partial downloads**: Download only the snapshots and fields you need

Technical Details
-----------------

File Formats
~~~~~~~~~~~~

- **Format**: HDF5 (Hierarchical Data Format)
- **Compression**: Optimized for scientific data
- **Portability**: Cross-platform compatible
- **Self-describing**: Metadata included in files

Particle Types
~~~~~~~~~~~~~~

Each simulation tracks multiple particle types:

- **Type 0**: Gas cells (hydrodynamics)
- **Type 1**: Dark matter particles
- **Type 3**: Tracer particles (Lagrangian tracking)
- **Type 4**: Star particles and wind cells
- **Type 5**: Supermassive black holes

Resolution Scaling
~~~~~~~~~~~~~~~~~~

Resolution levels differ by factors of 8 in mass and 2 in spatial resolution:

- **Level 1**: Highest resolution (flagship runs)
- **Level 2**: 8× higher particle mass
- **Level 3**: 64× higher particle mass
- **Level 4**: 512× higher particle mass (TNG50 only)

Summary
-------

The IllustrisTNG simulations provide an unprecedented range of scales and resolutions for galaxy formation studies. From the compact 0.6 TB TNG50-4 perfect for testing, to the massive 320 TB TNG50-1 for the highest resolution studies, there's a simulation suited for every research need.

Choose your simulation based on:

- **Scientific goals**: Resolution vs. volume requirements
- **Computational resources**: Available storage and processing power  
- **Network capacity**: Download time considerations
- **Analysis scope**: Single objects vs. statistical samples

For most users, we recommend starting with **TNG50-4** for development and **TNG100-1** or **TNG100-2** for production science. 