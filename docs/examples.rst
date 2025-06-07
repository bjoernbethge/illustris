Examples
========

This page contains detailed examples for common analysis tasks with Illustris data.

Galaxy Analysis
---------------

Stellar Mass-Size Relation
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import illustris
   import numpy as np
   import matplotlib.pyplot as plt
   
   basePath = "data/TNG50-4/output"
   snapNum = 99
   
   # Load subhalo properties
   subhalos = illustris.groupcat.loadSubhalos(
       basePath, snapNum,
       fields=["SubhaloMass", "SubhaloHalfmassRad", "SubhaloFlag"]
   )
   
   # Filter for central galaxies with stellar mass
   central = subhalos['SubhaloFlag'] == 1
   has_stars = subhalos['SubhaloMass'][:, 4] > 0
   mask = central & has_stars
   
   # Extract stellar masses and half-mass radii
   stellar_mass = subhalos['SubhaloMass'][mask, 4] * 1e10 / 0.704
   half_mass_rad = subhalos['SubhaloHalfmassRad'][mask, 4] / 0.704
   
   # Plot mass-size relation
   plt.figure(figsize=(10, 8))
   plt.scatter(np.log10(stellar_mass), np.log10(half_mass_rad), alpha=0.6)
   plt.xlabel('log₁₀(M* / M☉)')
   plt.ylabel('log₁₀(R₁/₂ / kpc)')
   plt.title('Stellar Mass-Size Relation')
   plt.show()

Halo Mass Function
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Load halo masses
   halos = illustris.groupcat.loadHalos(
       basePath, snapNum, fields=["GroupMass"]
   )
   
   # Convert to solar masses
   halo_masses = halos['GroupMass'] * 1e10 / 0.704
   
   # Create mass bins and plot
   mass_bins = np.logspace(10, 15, 30)
   counts, _ = np.histogram(halo_masses, bins=mass_bins)
   bin_centers = np.sqrt(mass_bins[1:] * mass_bins[:-1])
   
   plt.figure(figsize=(10, 8))
   plt.loglog(bin_centers, counts, 'o-', linewidth=2)
   plt.xlabel('Halo Mass [M☉]')
   plt.ylabel('Number of Halos')
   plt.title('Halo Mass Function')
   plt.show()

Merger Tree Analysis
--------------------

Mass Assembly History
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Find a massive central galaxy
   central_mask = subhalos['SubhaloFlag'] == 1
   stellar_masses = subhalos['SubhaloMass'][central_mask, 4]
   subhalo_id = np.where(central_mask)[0][np.argmax(stellar_masses)]
   
   # Load the merger tree
   tree = illustris.sublink.loadTree(
       basePath, snapNum, subhalo_id,
       fields=["SubhaloMass", "SnapNum"]
   )
   
   if tree:
       # Plot mass evolution
       snap_nums = tree['SnapNum']
       total_masses = tree['SubhaloMass'][:, 1] * 1e10 / 0.704
       
       plt.figure(figsize=(10, 6))
       plt.semilogy(snap_nums, total_masses, 'b-', linewidth=2)
       plt.xlabel('Snapshot Number')
       plt.ylabel('Total Mass [M☉]')
       plt.title(f'Mass Assembly History - Subhalo {subhalo_id}')
       plt.show()

Performance Tips
----------------

.. code-block:: python

   # Load only needed fields
   minimal_data = illustris.snapshot.loadSubset(
       basePath, snapNum, "gas",
       fields=["Coordinates"]  # Only coordinates
   )
   
   # Use bounding boxes for spatial cuts
   center = [50000, 50000, 50000]
   size = 5000
   bbox = [[center[i]-size, center[i]+size] for i in range(3)]
   
   region_data = illustris.snapshot.loadSubset(
       basePath, snapNum, "gas",
       fields=["Coordinates", "Masses"],
       bbox=bbox
   ) 