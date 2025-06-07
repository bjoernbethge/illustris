"""
Basic tests for Illustris package that don't require external data.
"""

import pytest
import illustris


def test_package_import():
    """Test that the package imports correctly."""
    assert illustris is not None


def test_snapshot_partTypeNum():
    """Test particle type number mapping."""
    assert illustris.snapshot.partTypeNum('gas') == 0
    assert illustris.snapshot.partTypeNum('dm') == 1
    assert illustris.snapshot.partTypeNum('stars') == 4
    assert illustris.snapshot.partTypeNum('bh') == 5


def test_snapshot_partTypeNum_invalid():
    """Test invalid particle type raises Exception."""
    with pytest.raises(Exception):
        illustris.snapshot.partTypeNum('invalid')


def test_util_functions():
    """Test utility functions exist."""
    # Test that key utility functions are available
    assert hasattr(illustris.util, 'partTypeNum') if hasattr(illustris, 'util') else True
    assert hasattr(illustris.snapshot, 'partTypeNum')
    assert hasattr(illustris.groupcat, 'loadHalos')
    assert hasattr(illustris.groupcat, 'loadSubhalos')


def test_modules_exist():
    """Test that all expected modules exist."""
    assert hasattr(illustris, 'snapshot')
    assert hasattr(illustris, 'groupcat')
    assert hasattr(illustris, 'sublink')


@pytest.mark.requires_data
def test_data_dependent_functions():
    """Test that data-dependent functions exist but don't call them."""
    # These functions exist but require actual data to test
    assert callable(illustris.snapshot.loadSubset)
    assert callable(illustris.snapshot.loadHalo)
    assert callable(illustris.groupcat.loadHalos)
    assert callable(illustris.groupcat.loadSubhalos)
    assert callable(illustris.sublink.loadTree) 