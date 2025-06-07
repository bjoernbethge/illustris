Troubleshooting Guide
====================

This page addresses common issues and questions when working with IllustrisTNG data, based on community forum discussions and user experiences.

Data Loading Issues
-------------------

Halo ID Matching Problems
~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem**: Cannot match halo IDs between different data products (e.g., TNG-Cluster and LHaloTree).

**Solution**: Both LHaloTree and SubLink are based on **subhalos**, not halos. Use subhalo IDs consistently:

.. code-block:: python

   import illustris
   
   basePath = 'sims.TNG/TNG-Cluster/output/'
   snap = 99
   sub_id = 12345  # Use subhalo ID, not halo ID
   
   # Both trees use identical API
   tree1 = illustris.sublink.loadTree(basePath, snap, sub_id, onlyMPB=True)
   tree2 = illustris.lhalotree.loadTree(basePath, snap, sub_id, onlyMPB=True)

Missing or Corrupted Files
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem**: Files appear to be HTML instead of HDF5, or downloads are incomplete.

**Solution**: Ensure proper API authentication and redirect handling:

.. code-block:: bash

   # Check your .env file
   TNG_API_KEY=your_api_key_here
   
   # Re-download with proper authentication
   illustris -data -test

**Problem**: "No such file or directory" errors when loading data.

**Solution**: Verify data paths and file structure:

.. code-block:: python

   import os
   
   basePath = "data/TNG50-4/output"
   
   # Check if path exists
   if not os.path.exists(basePath):
       print(f"Path does not exist: {basePath}")
       print("Run: illustris -data -test")
   
   # Check for required files
   snap_dir = f"{basePath}/snapdir_099"
   if not os.path.exists(snap_dir):
       print(f"Snapshot directory missing: {snap_dir}")

Analysis Issues
---------------

Unexpected Galaxy Selection Results
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem**: High gas fractions (>1) or massive objects (>10¹² M☉) labeled as galaxies.

**Solution**: Refine selection criteria to exclude central halos of clusters:

.. code-block:: python

   import illustris
   import numpy as np
   
   # Load subhalo data
   subhalos = illustris.groupcat.loadSubhalos(
       basePath, snap,
       fields=["SubhaloMass", "SubhaloFlag", "SubhaloGasMetallicity"]
   )
   
   # Proper galaxy selection
   stellar_mass = subhalos['SubhaloMass'][:, 4] * 1e10 / 0.704  # M☉
   total_mass = subhalos['SubhaloMass'][:, 1] * 1e10 / 0.704    # M☉
   
   # Filter criteria
   is_central = subhalos['SubhaloFlag'] == 1  # Central subhalo
   has_stars = stellar_mass > 1e8  # Minimum stellar mass
   not_too_massive = total_mass < 1e13  # Exclude massive clusters
   
   # Combined mask
   galaxy_mask = is_central & has_stars & not_too_massive
   
   print(f"Selected {np.sum(galaxy_mask)} galaxies")

Power Spectrum Discrepancies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem**: Matter power spectrum from ray tracing is 5-10% lower than theoretical predictions.

**Solution**: Compare with published results and check analysis methodology:

.. code-block:: python

   # Reference: Springel+18, Figure 4 for TNG300-1
   # For TNG300-1-Dark, see Figure 7 of the same paper
   
   # Ensure proper units and cosmological parameters
   h = 0.6774  # Hubble parameter
   box_size = 205.0  # Mpc/h for TNG300
   
   # Check if using correct snapshot and particle selection
   dm_particles = illustris.snapshot.loadSubset(
       basePath, snap, "dm",
       fields=["Coordinates", "Masses"]
   )

Snapshot Time Resolution Questions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem**: Need to understand time spacing between snapshots for feedback studies.

**Solution**: Extract timing information from snapshot headers:

.. code-block:: python

   import numpy as np
   
   # Load headers for all snapshots
   times = []
   redshifts = []
   
   for snap in range(100):  # 0 to 99
       try:
           header = illustris.groupcat.loadHeader(basePath, snap)
           times.append(header['Time'])
           redshifts.append(header['Redshift'])
       except:
           continue
   
   times = np.array(times)
   redshifts = np.array(redshifts)
   
   # Calculate time differences
   time_diffs = np.diff(times)  # in code units
   
   print(f"Time spacing ranges from {time_diffs.min():.3f} to {time_diffs.max():.3f}")
   print(f"Redshift range: z={redshifts.max():.1f} to z={redshifts.min():.1f}")

Performance Issues
------------------

Memory Problems
~~~~~~~~~~~~~~~

**Problem**: Out of memory errors when loading large datasets.

**Solution**: Use field selection and spatial cuts:

.. code-block:: python

   # Instead of loading everything
   # gas = illustris.snapshot.loadSubset(basePath, snap, "gas")  # DON'T DO THIS
   
   # Load only needed fields
   gas = illustris.snapshot.loadSubset(
       basePath, snap, "gas",
       fields=["Coordinates", "Masses"]  # Only what you need
   )
   
   # Use spatial cuts for regional analysis
   center = [50000, 50000, 50000]  # kpc/h
   size = 5000  # kpc/h
   bbox = [[center[i]-size, center[i]+size] for i in range(3)]
   
   gas_region = illustris.snapshot.loadSubset(
       basePath, snap, "gas",
       fields=["Coordinates", "Masses", "Density"],
       bbox=bbox
   )

Slow Loading Times
~~~~~~~~~~~~~~~~~~

**Problem**: Data loading takes too long.

**Solution**: Optimize data access patterns:

.. code-block:: python

   # Load group catalogs first (smaller files)
   subhalos = illustris.groupcat.loadSubhalos(
       basePath, snap, fields=["SubhaloPos", "SubhaloMass"]
   )
   
   # Then load particles only for interesting objects
   massive_subhalos = np.where(subhalos['SubhaloMass'][:, 1] > 1e12)[0]
   
   for sub_id in massive_subhalos[:10]:  # Top 10 only
       stars = illustris.snapshot.loadSubhalo(
           basePath, snap, sub_id, "stars",
           fields=["Coordinates", "Masses"]
       )
       # Process individual subhalo
       analyze_subhalo(stars)

API and Download Issues
-----------------------

Authentication Problems
~~~~~~~~~~~~~~~~~~~~~~~

**Problem**: API key not working or access denied.

**Solution**: Verify API key setup:

.. code-block:: bash

   # Check .env file in project root
   cat .env
   
   # Should contain:
   TNG_API_KEY=your_actual_api_key_here
   
   # Test API access
   illustris -data -list-sims

Download Failures
~~~~~~~~~~~~~~~~~

**Problem**: Downloads fail or are incomplete.

**Solution**: Check network connectivity and retry:

.. code-block:: bash

   # Test basic connectivity
   illustris -data -list-sims
   
   # For large downloads, ensure stable connection
   # Downloads can be resumed if interrupted
   illustris -data -test

Simulation-Specific Issues
--------------------------

Resolution Differences
~~~~~~~~~~~~~~~~~~~~~~

**Problem**: Confused about which simulation resolution to use.

**Solution**: Choose based on science goals:

.. code-block:: python

   # For testing and development
   basePath_test = "data/TNG50-4/output"  # 0.6 TB total
   
   # For production science
   basePath_prod = "data/TNG100-1/output"  # 128 TB total
   
   # Check available resolution levels
   illustris -data -list-sims

Initial Conditions Questions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem**: Need to understand IC generation for custom runs.

**Solution**: TNG uses specific IC generation procedures:

- **2LPT vs Zel'dovich**: TNG uses Zel'dovich approximation in ICs
- **Resolution scaling**: Same Fourier modes, different particle numbers
- **Custom runs**: Consider generating new ICs rather than modifying TNG ICs

.. code-block:: python

   # For custom simulations, use Gadget4 IC generation
   # rather than trying to modify TNG ICs
   
   # TNG resolution levels use same structures at different resolutions
   # TNG50-1, TNG50-2, TNG50-3, TNG50-4 have same large-scale structure

Data Analysis Best Practices
-----------------------------

Radial Profiles
~~~~~~~~~~~~~~~

**Problem**: How to create proper radial profiles.

**Solution**: Use mass-weighted binning without spatial smoothing:

.. code-block:: python

   import numpy as np
   
   # Load halo particles
   halo_gas = illustris.snapshot.loadHalo(
       basePath, snap, halo_id, "gas",
       fields=["Coordinates", "Masses", "Temperature"]
   )
   
   # Calculate distances from halo center
   halo_pos = halos['GroupPos'][halo_id]
   distances = np.linalg.norm(halo_gas['Coordinates'] - halo_pos, axis=1)
   
   # Create radial bins
   r_bins = np.logspace(0, 2, 20)  # 1 to 100 kpc
   
   # Mass-weighted temperature profile
   temp_profile = []
   for i in range(len(r_bins)-1):
       mask = (distances >= r_bins[i]) & (distances < r_bins[i+1])
       if np.sum(mask) > 0:
           weights = halo_gas['Masses'][mask]
           temp_avg = np.average(halo_gas['Temperature'][mask], weights=weights)
           temp_profile.append(temp_avg)
       else:
           temp_profile.append(np.nan)

Unit Conversions
~~~~~~~~~~~~~~~~

**Problem**: Confusion about units and cosmological parameters.

**Solution**: Use consistent unit conversions:

.. code-block:: python

   # TNG cosmological parameters
   h = 0.6774  # Hubble parameter
   Omega_m = 0.3089
   Omega_Lambda = 0.6911
   
   # Common conversions
   # Masses: code units * 1e10 / h → M☉
   stellar_mass_msun = subhalos['SubhaloMass'][:, 4] * 1e10 / h
   
   # Distances: code units / h → kpc (comoving)
   # For physical distances at z=0: same as comoving
   positions_kpc = subhalos['SubhaloPos'] / h
   
   # Velocities: code units → km/s (peculiar velocities)
   velocities_kms = subhalos['SubhaloVel']  # Already in km/s

Getting Help
------------

When to Ask for Help
~~~~~~~~~~~~~~~~~~~~

1. **Check documentation first**: Most questions are answered here
2. **Search the forum**: https://www.tng-project.org/data/forum/
3. **Provide details**: Include error messages, code snippets, and data paths
4. **Minimal examples**: Create simple test cases that reproduce the issue

Useful Information to Include
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When reporting issues, include:

- **Simulation and snapshot**: e.g., "TNG50-4, snapshot 99"
- **Code version**: `pip show illustris_python`
- **Error messages**: Full traceback
- **Data path**: Where files are located
- **System info**: OS, Python version, available memory

Community Resources
~~~~~~~~~~~~~~~~~~~

- **TNG Forum**: Official support and community discussions
- **GitHub Issues**: Bug reports and feature requests
- **Documentation**: Comprehensive guides and examples
- **Examples**: Jupyter notebooks and analysis scripts 