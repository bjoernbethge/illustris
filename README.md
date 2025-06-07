# Illustris (Modernized Fork)

**Modern Python package for reading and analyzing Illustris simulation data.**

This is a modernized and extended fork of the original [illustris_python](https://github.com/illustristng/illustris_python) package, featuring:

- 🚀 **Modern CLI tools** with async data downloading
- 🧪 **Comprehensive pytest test suite** with fixtures
- 📚 **Complete documentation** with examples and guides  
- ⚡ **Performance optimizations** and better error handling
- 🔧 **Developer-friendly** setup with uv and modern Python practices

> **Note**: This fork maintains full API compatibility with the original package while adding significant new functionality.

## Features

- **Data Loading**: Load snapshots, group catalogs, and merger trees
- **CLI Tools**: Command-line interface for data management and documentation
- **Modern Testing**: Comprehensive test suite with pytest fixtures
- **Documentation**: Auto-generated Sphinx documentation

## Installation

```bash
# Clone the repository
git clone https://github.com/bjoernbethge/illustris.git
cd illustris

# Install with uv (recommended)
uv sync

# Or install with pip
pip install -e .
```

## Quick Start

### CLI Usage

The `illustris` command provides tools for data management and documentation:

```bash
# Documentation
illustris -docs -generate          # Build documentation
illustris -docs -serve             # Serve documentation (port 8000)
illustris -docs -serve -p 8080     # Serve on custom port

# Data Management
illustris -data -test              # Download complete test data (TNG50-4, all files)
illustris -data -load TNG50-4      # Download latest snapshot
illustris -data -load TNG50-4 -snap 99  # Download specific snapshot
illustris -data -list-sims         # List available simulations
illustris -data -list-snaps TNG50-4 # List snapshots for simulation
```

### Python API

```python
import illustris

# Load snapshot data
gas_data = illustris.snapshot.loadSubset(
    basePath="data/TNG50-4/output", 
    snapNum=99, 
    partType='gas',
    fields=['Coordinates', 'Masses']
)

# Load group catalog
halos = illustris.groupcat.loadHalos(
    basePath="data/TNG50-4/output",
    snapNum=99,
    fields=['GroupMass', 'GroupPos']
)

# Load subhalos
subhalos = illustris.groupcat.loadSubhalos(
    basePath="data/TNG50-4/output", 
    snapNum=99,
    fields=['SubhaloMass', 'SubhaloPos']
)
```

## Configuration

Create a `.env` file for TNG API access:

```bash
# Copy example configuration
cp env.example .env

# Edit with your API key
ILLUSTRIS_API_KEY=your_api_key_here
ILLUSTRIS_DATA_DIR=./data  # Optional: custom data directory
```

Get your API key from: https://www.tng-project.org/users/register/

## Testing

The project includes comprehensive tests using pytest:

```bash
# Run all tests
uv run pytest

# Run specific test modules
uv run pytest tests/test_snapshot.py
uv run pytest tests/test_groupcat.py

# Run with coverage (automatically included)
uv run pytest

# Run with detailed coverage report
uv run pytest --cov-report=term-missing

# Run only tests that don't require data
uv run pytest -m "not requires_data"
```

### Test Data

**Complete Test Data**:
```bash
illustris -data -test
```
- Downloads ~5.3 GB of complete TNG50-4 dataset
- Enables all functionality tests including:
  - All 11 snapshot chunks for `loadSubset` testing
  - Group catalog files for halo/subhalo analysis
  - Offsets files for `loadHalo` testing  
  - SubLink trees for merger analysis
- Recommended for development and full validation

### Test Results

With complete test data:
- ✅ **26 tests pass** - Full functionality tested
- ⏭️ **0 tests skipped** - All features available

Tests automatically detect available data and skip appropriately if files are missing.

## Development

### Project Structure

```
illustris/
├── src/illustris/          # Main package
│   ├── cli.py             # Command-line interface
│   ├── snapshot.py        # Snapshot data loading
│   ├── groupcat.py        # Group catalog loading
│   ├── sublink.py         # Merger tree loading
│   └── util.py            # Utility functions
├── tests/                 # Test suite
│   ├── conftest.py        # Pytest fixtures
│   ├── test_basic.py      # Basic functionality tests
│   ├── test_snapshot.py   # Snapshot loading tests
│   ├── test_groupcat.py   # Group catalog tests
│   └── test_sublink.py    # Merger tree tests
├── docs/                  # Documentation
└── data/                  # Downloaded simulation data
```

### Adding Tests

Tests use pytest fixtures for consistent data access:

```python
import pytest
import illustris

@pytest.mark.requires_data
def test_my_function(test_data_path, test_snapshot):
    """Test with real simulation data."""
    data = illustris.snapshot.loadSubset(
        test_data_path, test_snapshot, 'gas'
    )
    assert data is not None

def test_basic_function():
    """Test without data dependencies."""
    result = illustris.snapshot.partTypeNum('gas')
    assert result == 0
```

### Building Documentation

```bash
# Generate API documentation
illustris -docs -generate

# Serve locally with auto-reload
illustris -docs -serve

# Documentation will be available at http://localhost:8000
```

## API Reference

### Snapshot Module

- `loadSubset(basePath, snapNum, partType, fields=None)` - Load particle data
- `loadHalo(basePath, snapNum, haloID, partType, fields=None)` - Load halo particles
- `partTypeNum(partType)` - Get particle type number
- `snapPath(basePath, snapNum, chunkNum=0)` - Get snapshot file path

### GroupCat Module

- `loadHalos(basePath, snapNum, fields=None)` - Load halo catalog
- `loadSubhalos(basePath, snapNum, fields=None)` - Load subhalo catalog
- `loadSingle(basePath, snapNum, haloID=None, subhaloID=None)` - Load single object
- `gcPath(basePath, snapNum, chunkNum=0)` - Get group catalog path

### SubLink Module

- `loadTree(basePath, snapNum, id, fields=None, onlyMPB=False)` - Load merger tree
- `numMergers(tree, minMassRatio=1e-10, massPartType='stars')` - Count mergers
- `treePath(basePath, chunkNum=0)` - Get tree file path

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Run the test suite (`uv run pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## Changelog

### Latest Changes

- **Simplified CLI**: Streamlined data management commands
- **Complete Test Data**: Single `-test` option for full dataset downloads
- **Modern Testing**: Migrated from nose to pytest with fixtures
- **API Integration**: Direct TNG API access for data downloads
- **Improved Documentation**: Auto-generated Sphinx docs with CLI integration
- **Better Error Handling**: Robust error handling for missing data
- **Smart Test Skipping**: Tests automatically adapt to available data

### Data Download Features

- **Complete Downloads**: Full dataset for comprehensive testing (~5.3 GB)
- **Intelligent Chunk Detection**: Automatically detects all available file chunks
- **Automatic TNG API authentication**
- **Progress indicators for large downloads**
- **Smart file organization** (snapshots, group catalogs, offsets, trees)
- **Support for all TNG simulations** (TNG50, TNG100, TNG300, Illustris)
- **Robust timeout handling** for large files

### Testing Improvements

- **Session-scoped fixtures** for efficient testing
- **Automatic data directory detection**
- **Separate tests for data-dependent and basic functionality**
- **Comprehensive validation** of file structures and data integrity
- **Smart skip mechanisms** for unavailable data
- **Detailed test output** with progress indicators

## Support

- **Documentation**: https://bjoernbethge.github.io/illustris
- **TNG Project**: https://www.tng-project.org/
- **API Documentation**: https://www.tng-project.org/data/docs/api/

## Troubleshooting

### Common Issues

**Permission Denied Errors**:
```bash
# Make sure you have write permissions to the data directory
chmod 755 data/
```

**Incomplete Downloads**:
```bash
# Remove corrupted files and re-download
rm -rf data/TNG50-4/output/snapdir_099/
illustris -data -test
```

**Missing API Key**:
```bash
# Set up your environment file
cp env.example .env
# Edit .env and add your TNG API key
```

**Test Failures**:
```bash
# Download complete test data for full functionality
illustris -data -test
uv run pytest tests/ -v
```