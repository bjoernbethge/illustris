"""
Tests for groupcat module using pytest fixtures.
"""

import pytest
import numpy as np
import illustris


@pytest.mark.requires_data
def test_groupcat_header(test_data_path, test_snapshot):
    """Test loading group catalog header."""
    header = illustris.groupcat.loadHeader(test_data_path, test_snapshot)
    
    assert header is not None
    assert isinstance(header, dict)
    assert 'Ngroups_Total' in header
    assert 'Nsubgroups_Total' in header
    assert header['Ngroups_Total'] > 0
    assert header['Nsubgroups_Total'] > 0


@pytest.mark.requires_data
def test_groupcat_path_function(test_data_path, test_snapshot):
    """Test the gcPath function."""
    path = illustris.groupcat.gcPath(test_data_path, test_snapshot)
    
    assert path is not None
    assert isinstance(path, str)
    assert f"_{test_snapshot:03d}" in path
    assert path.endswith('.hdf5')


@pytest.mark.requires_data
def test_groupcat_file_exists(test_data_path, test_snapshot):
    """Test that the group catalog file exists and is readable."""
    import h5py
    from pathlib import Path
    
    path = illustris.groupcat.gcPath(test_data_path, test_snapshot)
    assert Path(path).exists(), f"Group catalog file not found: {path}"
    
    # Test that we can open and read the file
    with h5py.File(path, 'r') as f:
        assert 'Header' in f
        assert 'Group' in f or 'Subhalo' in f


@pytest.mark.requires_data
def test_groupcat_basic_structure(test_data_path, test_snapshot):
    """Test basic structure of group catalog file."""
    import h5py
    
    path = illustris.groupcat.gcPath(test_data_path, test_snapshot)
    
    with h5py.File(path, 'r') as f:
        # Check header exists and has required fields
        header = f['Header']
        assert 'Ngroups_Total' in header.attrs
        assert 'Nsubgroups_Total' in header.attrs
        assert 'NumFiles' in header.attrs
        
        # Check that we have group and/or subhalo data
        has_groups = 'Group' in f and len(f['Group'].keys()) > 0
        has_subhalos = 'Subhalo' in f and len(f['Subhalo'].keys()) > 0
        
        assert has_groups or has_subhalos, "File should contain either Group or Subhalo data"


@pytest.mark.requires_data
def test_groupcat_data_fields(test_data_path, test_snapshot):
    """Test that expected data fields exist."""
    import h5py
    
    path = illustris.groupcat.gcPath(test_data_path, test_snapshot)
    
    with h5py.File(path, 'r') as f:
        # Check Group fields if they exist
        if 'Group' in f:
            group_fields = list(f['Group'].keys())
            assert len(group_fields) > 0
            
            # Check for some common fields
            common_group_fields = ['GroupMass', 'GroupPos', 'GroupVel']
            found_fields = [field for field in common_group_fields if field in group_fields]
            assert len(found_fields) > 0, f"Expected at least one of {common_group_fields}, found: {group_fields}"
        
        # Check Subhalo fields if they exist
        if 'Subhalo' in f:
            subhalo_fields = list(f['Subhalo'].keys())
            assert len(subhalo_fields) > 0
            
            # Check for some common fields
            common_subhalo_fields = ['SubhaloMass', 'SubhaloPos', 'SubhaloVel']
            found_fields = [field for field in common_subhalo_fields if field in subhalo_fields]
            assert len(found_fields) > 0, f"Expected at least one of {common_subhalo_fields}, found: {subhalo_fields}"


@pytest.mark.requires_data
def test_groupcat_data_shapes(test_data_path, test_snapshot):
    """Test that data arrays have reasonable shapes."""
    import h5py
    
    path = illustris.groupcat.gcPath(test_data_path, test_snapshot)
    
    with h5py.File(path, 'r') as f:
        header = dict(f['Header'].attrs.items())
        
        # Test Group data shapes
        if 'Group' in f:
            n_groups_file = header.get('Ngroups_ThisFile', 0)
            
            for field_name, field_data in f['Group'].items():
                assert field_data.shape[0] == n_groups_file, f"Group field {field_name} has wrong length"
                
                # Position and velocity should be 3D
                if 'Pos' in field_name or 'Vel' in field_name:
                    if len(field_data.shape) > 1:
                        assert field_data.shape[1] == 3, f"Field {field_name} should be 3D"
        
        # Test Subhalo data shapes  
        if 'Subhalo' in f:
            n_subhalos_file = header.get('Nsubgroups_ThisFile', 0)
            
            for field_name, field_data in f['Subhalo'].items():
                assert field_data.shape[0] == n_subhalos_file, f"Subhalo field {field_name} has wrong length"
                
                # Position and velocity should be 3D
                if 'Pos' in field_name or 'Vel' in field_name:
                    if len(field_data.shape) > 1:
                        assert field_data.shape[1] == 3, f"Field {field_name} should be 3D"


@pytest.mark.requires_data
def test_groupcat_error_handling(test_data_path, test_snapshot):
    """Test error handling for invalid inputs."""
    # Test invalid halo/subhalo ID specification for loadSingle
    with pytest.raises(Exception):
        illustris.groupcat.loadSingle(test_data_path, test_snapshot)  # Neither specified
    
    with pytest.raises(Exception):
        illustris.groupcat.loadSingle(test_data_path, test_snapshot, haloID=0, subhaloID=0)  # Both specified 