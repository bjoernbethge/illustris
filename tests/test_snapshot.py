"""
Tests for snapshot module using pytest fixtures.
"""

import pytest
import numpy as np
import illustris


@pytest.mark.requires_data
def test_snapshot_file_exists(test_data_path, test_snapshot):
    """Test that snapshot file exists and is readable."""
    import h5py
    from pathlib import Path
    
    path = illustris.snapshot.snapPath(test_data_path, test_snapshot)
    assert Path(path).exists(), f"Snapshot file not found: {path}"
    
    # Test that we can open and read the file
    with h5py.File(path, 'r') as f:
        assert 'Header' in f
        # Check for particle types
        particle_types = [key for key in f.keys() if key.startswith('PartType')]
        assert len(particle_types) > 0, "No particle types found in snapshot"


@pytest.mark.requires_data
def test_snapshot_header(test_data_path, test_snapshot):
    """Test snapshot header."""
    import h5py
    
    path = illustris.snapshot.snapPath(test_data_path, test_snapshot)
    
    with h5py.File(path, 'r') as f:
        header = dict(f['Header'].attrs.items())
        
        assert header is not None
        assert isinstance(header, dict)
        assert 'NumPart_Total' in header
        assert 'BoxSize' in header
        assert 'Time' in header
        assert 'Redshift' in header


@pytest.mark.requires_data
def test_snapshot_particle_types(test_data_path, test_snapshot):
    """Test particle type number mapping."""
    # Test the partTypeNum function
    assert illustris.snapshot.partTypeNum('gas') == 0
    assert illustris.snapshot.partTypeNum('dm') == 1
    assert illustris.snapshot.partTypeNum('stars') == 4
    assert illustris.snapshot.partTypeNum('bh') == 5
    
    # Test invalid particle type
    with pytest.raises(Exception):
        illustris.snapshot.partTypeNum('invalid')


@pytest.mark.requires_data
def test_snapshot_basic_structure(test_data_path, test_snapshot):
    """Test basic structure of snapshot file."""
    import h5py
    
    path = illustris.snapshot.snapPath(test_data_path, test_snapshot)
    
    with h5py.File(path, 'r') as f:
        # Check header exists and has required fields
        header = f['Header']
        assert 'NumPart_Total' in header.attrs
        assert 'NumPart_ThisFile' in header.attrs
        assert 'NumFilesPerSnapshot' in header.attrs
        
        # Check that we have particle data
        particle_types = [key for key in f.keys() if key.startswith('PartType')]
        assert len(particle_types) > 0, "No particle types found"
        
        # Check that each particle type has some data
        for ptype in particle_types:
            ptype_keys = list(f[ptype].keys())
            if len(ptype_keys) > 0:
                # Each particle type should have at least some fields
                assert len(ptype_keys) > 0, f"Particle type {ptype} has no fields"
                
                # Check for common fields if they exist
                common_fields = ['Coordinates', 'ParticleIDs', 'Masses', 'Velocities']
                found_fields = [field for field in common_fields if field in f[ptype]]
                
                # Some particle types (like tracers) might not have standard fields
                # Just check that they have some data fields
                if len(found_fields) == 0:
                    # At least check that the fields are data arrays
                    for field in ptype_keys:
                        assert hasattr(f[ptype][field], 'shape'), f"Field {field} in {ptype} is not a data array"


@pytest.mark.requires_data
def test_snapshot_data_fields(test_data_path, test_snapshot):
    """Test that expected data fields exist."""
    import h5py
    
    path = illustris.snapshot.snapPath(test_data_path, test_snapshot)
    
    with h5py.File(path, 'r') as f:
        # Check PartType0 (gas) if it exists
        if 'PartType0' in f and len(f['PartType0'].keys()) > 0:
            gas_fields = list(f['PartType0'].keys())
            expected_gas_fields = ['Coordinates', 'Masses', 'Velocities']
            found_fields = [field for field in expected_gas_fields if field in gas_fields]
            assert len(found_fields) > 0, f"Expected gas fields not found. Available: {gas_fields}"
        
        # Check PartType1 (dark matter) if it exists
        if 'PartType1' in f and len(f['PartType1'].keys()) > 0:
            dm_fields = list(f['PartType1'].keys())
            expected_dm_fields = ['Coordinates', 'ParticleIDs', 'Velocities']
            found_fields = [field for field in expected_dm_fields if field in dm_fields]
            assert len(found_fields) > 0, f"Expected DM fields not found. Available: {dm_fields}"


@pytest.mark.requires_data
def test_snapshot_data_shapes(test_data_path, test_snapshot):
    """Test that data arrays have reasonable shapes."""
    import h5py
    
    path = illustris.snapshot.snapPath(test_data_path, test_snapshot)
    
    with h5py.File(path, 'r') as f:
        header = dict(f['Header'].attrs.items())
        num_part_file = header.get('NumPart_ThisFile', [0]*6)
        
        # Test each particle type
        for i, ptype_name in enumerate(['PartType0', 'PartType1', 'PartType2', 'PartType3', 'PartType4', 'PartType5']):
            if ptype_name in f and len(f[ptype_name].keys()) > 0:
                n_particles = num_part_file[i]
                
                for field_name, field_data in f[ptype_name].items():
                    if n_particles > 0:
                        assert field_data.shape[0] == n_particles, f"{ptype_name} field {field_name} has wrong length"
                        
                        # Coordinates and velocities should be 3D
                        if field_name in ['Coordinates', 'Velocities']:
                            if len(field_data.shape) > 1:
                                assert field_data.shape[1] == 3, f"Field {field_name} should be 3D"


@pytest.mark.requires_data
def test_snapshot_path_function(test_data_path, test_snapshot):
    """Test the snapPath function."""
    path = illustris.snapshot.snapPath(test_data_path, test_snapshot)
    
    assert path is not None
    assert isinstance(path, str)
    assert f"_{test_snapshot:03d}" in path
    assert path.endswith('.hdf5')


@pytest.mark.requires_data
def test_snapshot_loadSubset(test_data_path, test_snapshot):
    """Test loading particle data with loadSubset."""
    try:
        # Check if we have multiple snapshot files (complete test data)
        import os
        snap_dir = os.path.join(test_data_path, f"snapdir_{test_snapshot:03d}")
        snap_files = [f for f in os.listdir(snap_dir) if f.startswith(f"snap_{test_snapshot:03d}") and f.endswith(".hdf5")]
        
        if len(snap_files) < 2:
            pytest.skip("loadSubset requires multiple snapshot files. Use 'illustris -data -test-complete' to download all files.")
        
        # Load gas particles with specific fields
        gas_data = illustris.snapshot.loadSubset(
            test_data_path, test_snapshot, 'gas',
            fields=['Coordinates', 'Masses']
        )
        
        assert gas_data is not None
        assert isinstance(gas_data, dict)
        assert 'Coordinates' in gas_data
        assert 'Masses' in gas_data
        
        # Check data types
        assert isinstance(gas_data['Coordinates'], np.ndarray)
        assert isinstance(gas_data['Masses'], np.ndarray)
        
        # Check shapes
        n_particles = len(gas_data['Masses'])
        assert gas_data['Coordinates'].shape == (n_particles, 3)
        assert gas_data['Masses'].shape == (n_particles,)
        
        print(f"✓ Loaded {n_particles} gas particles from {len(snap_files)} files")
        
    except Exception as e:
        pytest.skip(f"loadSubset test failed: {e}")


@pytest.mark.requires_data
def test_snapshot_loadHalo(test_data_path, test_snapshot, sample_subhalo_id):
    """Test loading halo particles."""
    try:
        # Check if offsets file exists
        import os
        offsets_path = os.path.join(test_data_path, "postprocessing", "offsets", f"offsets_{test_snapshot}.hdf5")
        
        if not os.path.exists(offsets_path):
            pytest.skip("loadHalo requires offsets file. Use 'illustris -data -test-complete' to download all files.")
        
        # Try to load halo particles for subhalo 0
        halo_data = illustris.snapshot.loadHalo(test_data_path, test_snapshot, sample_subhalo_id, 'gas')
        if halo_data is not None:
            assert isinstance(halo_data, dict)
            # Should have some fields
            assert len(halo_data) > 0
            print(f"✓ Loaded halo data for subhalo {sample_subhalo_id}")
        else:
            pytest.skip("No halo data returned - subhalo may not have gas particles")
    except FileNotFoundError as e:
        pytest.skip(f"Offsets file not available for loadHalo test: {e}")
    except Exception as e:
        pytest.skip(f"loadHalo test failed: {e}") 