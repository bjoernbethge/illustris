Quick Start Guide
=================

This guide will get you up and running with Illustris Python in just a few minutes.

Prerequisites
-------------

Make sure you have:

1. **Installed the package** (see :doc:`installation`)
2. **Configured your API key** in ``.env`` file
3. **Downloaded test data**: ``illustris -data -test``

Basic Usage
-----------

Import the Package
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import illustris
   import numpy as np
   import matplotlib.pyplot as plt

Set Data Path
~~~~~~~~~~~~~

.. code-block:: python

   # Path to your downloaded data
   basePath = "data/TNG50-4/output"
   snapNum = 99  # Final snapshot

Loading Snapshot Data
~~~~~~~~~~~~~~~~~~~~~

Load particle data from simulation snapshots:

.. code-block:: python

   # Load gas particle coordinates and masses
   gas = illustris.snapshot.loadSubset(
       basePath, snapNum, "gas",
       fields=["Coordinates", "Masses"]
   )
   
   print(f"Loaded {len(gas['Masses'])} gas particles")
   print(f"Coordinate range: {gas['Coordinates'].min():.2f} to {gas['Coordinates'].max():.2f}")

Available particle types:

- ``"gas"`` (type 0) - Gas particles
- ``"dm"`` (type 1) - Dark matter particles  
- ``"stars"`` (type 4) - Star particles
- ``"bh"`` (type 5) - Black hole particles

Loading Group Catalogs
~~~~~~~~~~~~~~~~~~~~~~

Load halo and subhalo information:

.. code-block:: python

   # Load halo properties
   halos = illustris.groupcat.loadHalos(
       basePath, snapNum,
       fields=["GroupMass", "GroupPos", "GroupVel"]
   )
   
   # Load subhalo properties
   subhalos = illustris.groupcat.loadSubhalos(
       basePath, snapNum, 
       fields=["SubhaloMass", "SubhaloPos", "SubhaloStellarPhotometrics"]
   )
   
   print(f"Found {len(halos['GroupMass'])} halos")
   print(f"Found {len(subhalos['SubhaloMass'])} subhalos")

Loading Individual Objects
~~~~~~~~~~~~~~~~~~~~~~~~~~

Load particles belonging to specific halos:

.. code-block:: python

   # Load all particles in the most massive halo
   halo_id = np.argmax(halos['GroupMass'])
   
   halo_stars = illustris.snapshot.loadHalo(
       basePath, snapNum, halo_id, "stars",
       fields=["Coordinates", "Masses", "GFM_StellarFormationTime"]
   )
   
   print(f"Halo {halo_id} contains {len(halo_stars['Masses'])} star particles")

Simple Analysis Examples
------------------------

Stellar Mass Function
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import matplotlib.pyplot as plt
   
   # Calculate stellar masses (convert to solar masses)
   stellar_masses = subhalos['SubhaloMass'][:, 4] * 1e10 / 0.704  # h^-1 factor
   
   # Remove zero masses
   stellar_masses = stellar_masses[stellar_masses > 0]
   
   # Plot histogram
   plt.figure(figsize=(8, 6))
   plt.hist(np.log10(stellar_masses), bins=30, alpha=0.7)
   plt.xlabel('log₁₀(M* / M☉)')
   plt.ylabel('Number of Subhalos')
   plt.title('Stellar Mass Function')
   plt.show()

Gas Density Map
~~~~~~~~~~~~~~~

.. code-block:: python

   # Load gas data in a central region
   center = [50000, 50000, 50000]  # Box center in kpc/h
   size = 10000  # 10 Mpc/h region
   
   # Create bounding box
   bbox = [
       [center[0] - size/2, center[0] + size/2],
       [center[1] - size/2, center[1] + size/2], 
       [center[2] - size/2, center[2] + size/2]
   ]
   
   gas_region = illustris.snapshot.loadSubset(
       basePath, snapNum, "gas",
       fields=["Coordinates", "Masses", "Density"],
       bbox=bbox
   )
   
   # Create 2D projection
   x = gas_region['Coordinates'][:, 0]
   y = gas_region['Coordinates'][:, 1]
   density = gas_region['Density']
   
   plt.figure(figsize=(10, 8))
   plt.scatter(x, y, c=np.log10(density), s=1, alpha=0.6)
   plt.colorbar(label='log₁₀(ρ)')
   plt.xlabel('x [ckpc/h]')
   plt.ylabel('y [ckpc/h]')
   plt.title('Gas Density Projection')
   plt.show()

Merger Tree Analysis
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Load merger tree for the most massive subhalo
   subhalo_id = np.argmax(subhalos['SubhaloMass'][:, 1])  # Total mass
   
   tree = illustris.sublink.loadTree(
       basePath, snapNum, subhalo_id,
       fields=["SubhaloMass", "SnapNum", "SubfindID"]
   )
   
   if tree:
       # Plot mass evolution
       snap_nums = tree['SnapNum']
       masses = tree['SubhaloMass'][:, 1] * 1e10 / 0.704  # Total mass
       
       plt.figure(figsize=(10, 6))
       plt.plot(snap_nums, np.log10(masses))
       plt.xlabel('Snapshot Number')
       plt.ylabel('log₁₀(M_total / M☉)')
       plt.title(f'Mass Evolution of Subhalo {subhalo_id}')
       plt.show()
       
       # Count major mergers
       mergers = illustris.sublink.numMergers(tree, minMassRatio=0.1)
       print(f"Number of major mergers (>1:10): {mergers}")

Command Line Interface
----------------------

The CLI provides convenient data management:

.. code-block:: bash

   # Download test data
   illustris -data -test
   
   # Download specific simulation
   illustris -data -load TNG100-1 -snap 99
   
   # List available simulations
   illustris -data -list-sims
   
   # List snapshots for a simulation
   illustris -data -list-snaps TNG50-1

Documentation and Help
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Build documentation
   illustris -docs -generate
   
   # Serve documentation locally
   illustris -docs -serve

Next Steps
----------

Now that you've got the basics, explore:

- :doc:`examples` - More detailed analysis examples
- :doc:`cli` - Complete CLI reference
- :doc:`api/illustris` - Full API documentation

Common Patterns
---------------

**Loading Multiple Fields**:

.. code-block:: python

   data = illustris.snapshot.loadSubset(
       basePath, snapNum, "stars",
       fields=["Coordinates", "Masses", "Velocities", "GFM_StellarFormationTime"]
   )

**Error Handling**:

.. code-block:: python

   try:
       data = illustris.snapshot.loadSubset(basePath, snapNum, "gas")
   except FileNotFoundError:
       print("Snapshot file not found. Download data first:")
       print("illustris -data -test")

**Memory Management**:

.. code-block:: python

   # For large datasets, load only what you need
   coords_only = illustris.snapshot.loadSubset(
       basePath, snapNum, "dm", 
       fields=["Coordinates"]  # Only coordinates, not masses
   )

**Unit Conversions**:

.. code-block:: python

   # Illustris uses comoving coordinates and h^-1 units
   h = 0.704  # Hubble parameter
   
   # Convert masses to solar masses
   mass_solar = data['Masses'] * 1e10 / h
   
   # Convert coordinates to physical kpc
   coords_kpc = data['Coordinates'] / h  # Already physical at z=0 