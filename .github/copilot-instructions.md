# Repository Instructions for GitHub Copilot

This is a Python package for reading and analyzing Illustris astronomy simulation data. This is a modernized fork of the original illustris_python package, maintaining full API compatibility while adding modern development practices.

## Quick Reference

### Build and Test Commands
```bash
# Setup
uv sync --dev                    # Install all dependencies

# Testing
uv run pytest                    # Run all tests with coverage
uv run pytest -m "not requires_data"  # Run tests without data dependencies
uv run pytest tests/test_snapshot.py  # Run specific test file

# Code Quality
uv run ruff check src/ tests/    # Run linter
uv run ruff check --fix src/ tests/  # Auto-fix linting issues
uv run ruff format src/ tests/   # Format code

# Documentation
illustris -docs -generate        # Build documentation
illustris -docs -serve           # Serve docs at localhost:8000
```

## Project Overview

**Tech Stack:**
- Python 3.11+ (minimum required version)
- Package manager: **uv** (not pip or poetry)
- Testing: **pytest** with pytest-cov
- Documentation: **Sphinx** with NumPy-style docstrings
- Linting/Formatting: **ruff**
- Data format: **HDF5** via h5py

**Core Dependencies:**
- h5py (HDF5 file access)
- numpy (numerical arrays)
- httpx (async HTTP for data downloads)
- python-dotenv (environment configuration)
- six (Python 2/3 compatibility layer)

## Code Standards

### Python Style
- Follow **PEP 8** with **88 character line length** (Black/Ruff standard)
- Use **type hints** where appropriate (mypy configured)
- Import order: standard library → third-party → local imports
- Use **descriptive variable names**

### Naming Conventions (IMPORTANT)
- **Functions**: **camelCase** (e.g., `loadSubset`, `loadHalos`) - this is intentional for API compatibility with original illustris_python
- **Variables**: camelCase for parameters matching function signatures
- **Constants**: UPPER_CASE
- **Classes**: PascalCase
- **DO NOT** convert camelCase to snake_case for public API functions

### Documentation
- Use **NumPy-style docstrings** for all public functions
- Include parameter types, return types, and examples
- Update README.md for user-facing changes
- Keep docstrings accurate and up-to-date

### Testing Requirements
- Add tests for all new functionality
- Use `@pytest.mark.requires_data` for tests needing simulation data
- Tests should skip gracefully if data is unavailable
- Use session-scoped fixtures from conftest.py
- Aim for >80% code coverage (>90% for critical modules)

## Repository Structure

```
illustris/
├── src/illustris/          # Main package source
│   ├── cli.py             # Command-line interface (async downloads)
│   ├── snapshot.py        # Snapshot data loading (particle data)
│   ├── groupcat.py        # Group catalog loading (halos/subhalos)
│   ├── sublink.py         # Merger tree loading
│   ├── lhalotree.py       # LHaloTree format support
│   ├── cartesian.py       # Cartesian coordinate utilities
│   └── util.py            # Utility functions
├── tests/                 # Pytest test suite
│   ├── conftest.py        # Fixtures (test_data_path, etc.)
│   ├── test_basic.py      # Basic functionality tests
│   ├── test_snapshot.py   # Snapshot loading tests
│   ├── test_groupcat.py   # Group catalog tests
│   └── test_sublink.py    # Merger tree tests
├── docs/                  # Sphinx documentation
│   ├── conf.py            # Sphinx configuration
│   └── _build/            # Generated docs (not in git)
├── data/                  # Downloaded simulation data (not in git)
└── .github/
    └── agents/            # Custom Copilot agents
```

## Key Constraints

### API Compatibility
- **MUST** maintain backward compatibility with original illustris_python
- Core functions (loadSubset, loadHalos, etc.) must keep consistent signatures
- New features should be additive, not breaking
- Preserve camelCase naming for all public API functions

### Security
- **Never commit** API keys, secrets, or credentials
- Use `.env` file for configuration (in .gitignore)
- Validate file paths to prevent directory traversal
- Handle network errors and timeouts appropriately

### Data Handling
- Simulation data is **HDF5 format** accessed via h5py
- Data directory (`data/`) is **not committed** to git
- Handle missing data gracefully with informative errors
- TNG API key stored in `.env` file (use python-dotenv to load)

### Dependencies
- **Minimize** new dependencies - prefer standard library
- If adding dependencies, use only well-maintained, popular packages
- Core dependencies: h5py, numpy, six, httpx, python-dotenv
- Dev dependencies: pytest, pytest-cov, sphinx, sphinx-rtd-theme, ruff

## What NOT to Change

- **DO NOT** modify the camelCase naming convention for core API functions (it's intentional for compatibility)
- **DO NOT** commit large data files or API keys
- **DO NOT** add unnecessary dependencies
- **DO NOT** remove or disable existing tests without good reason
- **DO NOT** modify files in `data/` directory (it's for downloaded simulations)
- **DO NOT** break backward compatibility with original illustris_python API
- **DO NOT** change core function signatures without maintaining compatibility

## Git Workflow

1. **Create feature branch**: `git checkout -b feature/description` or `fix/description`
2. **Make changes**: Implement feature/fix with tests
3. **Run tests**: `uv run pytest` (all must pass)
4. **Run linter**: `uv run ruff check --fix src/ tests/`
5. **Commit**: Clear, descriptive commit message
6. **Push**: `git push origin branch-name`
7. **Create PR**: Include description of changes and testing done

## Testing

### Running Tests
- All tests: `uv run pytest`
- Specific file: `uv run pytest tests/test_snapshot.py`
- Without data: `uv run pytest -m "not requires_data"`
- Verbose: `uv run pytest -v`
- With coverage: `uv run pytest --cov-report=term-missing`

### Test Data
- Test data: ~5.3 GB TNG50-4 simulation
- Download: `illustris -data -test`
- Tests auto-skip if data unavailable
- Use fixtures: `test_data_path`, `test_snapshot`, `test_sim_name`

## Development Environment Setup

```bash
# Clone repository
git clone https://github.com/bjoernbethge/illustris.git
cd illustris

# Install dependencies with uv
uv sync --dev

# Install package in editable mode
uv pip install -e .

# Set up environment configuration
cp env.example .env
# Edit .env to add TNG API key

# Download test data (optional, 5.3 GB)
illustris -data -test

# Run tests
uv run pytest
```

## Before Submitting Changes

Checklist:
- [ ] All tests pass: `uv run pytest`
- [ ] Code is linted: `uv run ruff check --fix src/ tests/`
- [ ] Code is formatted: `uv run ruff format src/ tests/`
- [ ] Documentation is updated (docstrings, README if needed)
- [ ] New functionality has tests
- [ ] Tests use appropriate markers (`@pytest.mark.requires_data`)
- [ ] No secrets or API keys committed
- [ ] Backward compatibility maintained
- [ ] Commit message is clear and descriptive

## Special Notes

This is a **scientific computing package** used by astronomy researchers to analyze multi-gigabyte simulation datasets. Code quality requirements:

- **Correctness**: Incorrect calculations can invalidate research
- **Stability**: Breaking changes impact dependent research projects
- **Performance**: Operations on large HDF5 files must be efficient
- **Documentation**: Scientists need clear examples and explanations

Treat this repository with care - researchers depend on it for their work.
