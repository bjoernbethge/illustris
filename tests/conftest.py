"""
Pytest configuration and fixtures for Illustris tests.
"""

import pytest
import os
from pathlib import Path


@pytest.fixture(scope="session")
def data_dir():
    """Get the data directory path."""
    # Check if we have local data directory first
    local_data_dir = Path("data")
    if local_data_dir.exists():
        return local_data_dir
    
    # Fall back to default
    default_dir = Path.home() / "illustris_data"
    return Path(os.getenv("ILLUSTRIS_DATA_DIR", default_dir))


@pytest.fixture(scope="session")
def test_data_path(data_dir):
    """Path to test data (TNG50-4)."""
    test_path = data_dir / "TNG50-4" / "output"
    if not test_path.exists():
        pytest.skip(f"Test data not found at {test_path}. Run 'illustris -data -test' to download.")
    return str(test_path)


@pytest.fixture(scope="session")
def test_simulation():
    """Test simulation name."""
    return "TNG50-4"


@pytest.fixture(scope="session")
def test_snapshot():
    """Test snapshot number."""
    return 99


@pytest.fixture(scope="session")
def snapshot_path(test_data_path, test_snapshot):
    """Path to test snapshot directory."""
    snap_path = Path(test_data_path) / f"snapdir_{test_snapshot:03d}"
    if not snap_path.exists():
        pytest.skip(f"Snapshot directory not found: {snap_path}")
    return str(snap_path)


@pytest.fixture(scope="session")
def groupcat_path(test_data_path, test_snapshot):
    """Path to test group catalog directory."""
    gc_path = Path(test_data_path) / f"groups_{test_snapshot:03d}"
    if not gc_path.exists():
        pytest.skip(f"Group catalog directory not found: {gc_path}")
    return str(gc_path)


@pytest.fixture(scope="session")
def offsets_path(test_data_path, test_snapshot):
    """Path to offsets file (optional)."""
    offset_path = Path(test_data_path) / "postprocessing" / "offsets" / f"offsets_{test_snapshot}.hdf5"
    if offset_path.exists():
        return str(offset_path)
    return None


@pytest.fixture
def sample_halo_id():
    """Sample halo ID for testing."""
    return 0  # First halo


@pytest.fixture
def sample_subhalo_id():
    """Sample subhalo ID for testing."""
    return 0  # First subhalo


# Marker for tests that require downloaded data
def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line(
        "markers", "requires_data: mark test as requiring downloaded simulation data"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    ) 