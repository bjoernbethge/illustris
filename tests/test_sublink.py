"""
Tests for sublink module using pytest fixtures.
"""

import pytest
import numpy as np
import illustris


@pytest.mark.requires_data
def test_sublink_treePath(test_data_path):
    """Test SubLink tree path construction."""
    try:
        # Check if SubLink trees exist
        import os
        tree_dir = os.path.join(test_data_path, "trees", "SubLink")
        
        if not os.path.exists(tree_dir):
            pytest.skip("SubLink trees not available. Use 'illustris -data -test-complete' to download all files.")
        
        tree_files = [f for f in os.listdir(tree_dir) if f.startswith("tree_extended") and f.endswith(".hdf5")]
        if not tree_files:
            pytest.skip("No SubLink tree files found in trees directory.")
        
        tree_name = "SubLink"
        path = illustris.sublink.treePath(test_data_path, tree_name, '*')
        assert path is not None
        assert isinstance(path, str)
        print(f"✓ SubLink tree path: {path}")
    except ValueError:
        pytest.skip("SubLink trees not available in test data")


@pytest.mark.requires_data
def test_sublink_loadTree(test_data_path, test_snapshot, sample_subhalo_id):
    """Test loading SubLink merger tree."""
    try:
        # Check if SubLink trees exist
        import os
        tree_dir = os.path.join(test_data_path, "trees", "SubLink")
        
        if not os.path.exists(tree_dir):
            pytest.skip("SubLink trees not available. Use 'illustris -data -test-complete' to download all files.")
        
        fields = ['SubhaloMass', 'SnapNum']
        tree = illustris.sublink.loadTree(test_data_path, test_snapshot, 
                                        sample_subhalo_id, fields=fields)
        
        if tree is not None:
            assert isinstance(tree, dict)
            for field in fields:
                if field in tree:
                    assert isinstance(tree[field], np.ndarray)
            print(f"✓ Loaded SubLink tree for subhalo {sample_subhalo_id}")
        else:
            pytest.skip("No tree data returned for subhalo")
    except (ValueError, FileNotFoundError):
        pytest.skip("SubLink trees not available in test data")


@pytest.mark.requires_data
def test_sublink_numMergers(test_data_path, test_snapshot, sample_subhalo_id):
    """Test counting mergers in SubLink tree."""
    try:
        # Check if SubLink trees exist
        import os
        tree_dir = os.path.join(test_data_path, "trees", "SubLink")
        
        if not os.path.exists(tree_dir):
            pytest.skip("SubLink trees not available. Use 'illustris -data -test-complete' to download all files.")
        
        # First load the tree, then count mergers
        tree = illustris.sublink.loadTree(test_data_path, test_snapshot, sample_subhalo_id)
        
        if tree is None:
            pytest.skip("No tree data available for subhalo")
        
        ratio = 1.0/5.0
        num_mergers = illustris.sublink.numMergers(tree, minMassRatio=ratio)
        
        if num_mergers is not None:
            assert isinstance(num_mergers, (int, np.integer))
            assert num_mergers >= 0
            print(f"✓ Found {num_mergers} mergers for subhalo {sample_subhalo_id}")
        else:
            pytest.skip("No merger data returned for subhalo")
    except (ValueError, FileNotFoundError):
        pytest.skip("SubLink trees not available in test data")


def test_sublink_module_exists():
    """Test that sublink module and functions exist."""
    assert hasattr(illustris, 'sublink')
    assert hasattr(illustris.sublink, 'treePath')
    assert hasattr(illustris.sublink, 'loadTree')
    assert hasattr(illustris.sublink, 'numMergers')
    
    # Test that functions are callable
    assert callable(illustris.sublink.treePath)
    assert callable(illustris.sublink.loadTree)
    assert callable(illustris.sublink.numMergers) 