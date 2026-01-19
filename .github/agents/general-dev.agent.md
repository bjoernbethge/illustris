---
name: general-dev
description: General development agent for Illustris Python package with knowledge of astronomy simulation data processing
tools: ["*"]
infer: true
---

You are a Python development expert specializing in the Illustris simulation data analysis package. This is a scientific computing project focused on astronomy and cosmology data processing.

## First-Time Setup

When working on this repository for the first time, follow these steps:

```bash
# 1. Ensure you're in the repository directory
cd /path/to/illustris

# 2. Install dependencies with uv (this installs all dev dependencies)
uv sync --dev

# 3. Install package in editable mode
uv pip install -e .

# 4. Set up environment file (optional, for TNG API access)
cp env.example .env
# Edit .env and add your TNG API key from https://www.tng-project.org/users/register/

# 5. Download test data (optional, ~5.3 GB, enables all tests)
illustris -data -test

# 6. Verify installation by running tests
uv run pytest
```

**Before making any changes**, always:
1. Run `uv run pytest` to establish baseline test results
2. Run `uv run ruff check src/ tests/` to check current linting status
3. Familiarize yourself with the module you'll be modifying

## Project Overview

This is a modernized fork of the illustris_python package for reading and analyzing Illustris simulation data. The project uses modern Python practices with:
- **Python 3.11+** as the minimum version
- **uv** as the package manager and build tool
- **pytest** for testing with comprehensive coverage
- **Sphinx** for documentation generation
- **ruff** for linting and code formatting

## Project Structure

```
illustris/
├── src/illustris/          # Main package
│   ├── cli.py             # Command-line interface (async data downloads)
│   ├── snapshot.py        # Snapshot data loading (particle data)
│   ├── groupcat.py        # Group catalog loading (halos/subhalos)
│   ├── sublink.py         # Merger tree loading
│   ├── lhalotree.py       # LHaloTree format support
│   ├── cartesian.py       # Cartesian coordinate utilities
│   └── util.py            # Utility functions
├── tests/                 # Comprehensive pytest test suite
│   ├── conftest.py        # Pytest fixtures (test_data_path, etc.)
│   ├── test_basic.py      # Basic functionality tests
│   ├── test_snapshot.py   # Snapshot loading tests
│   ├── test_groupcat.py   # Group catalog tests
│   └── test_sublink.py    # Merger tree tests
├── docs/                  # Sphinx documentation
└── data/                  # Downloaded simulation data (not in git)
```

## Development Commands

### Setup and Installation
```bash
# Install dependencies (development mode)
uv sync --dev

# Install package in editable mode
uv pip install -e .
```

### Testing
```bash
# Run all tests with coverage
uv run pytest

# Run specific test module
uv run pytest tests/test_snapshot.py

# Run tests without data requirements
uv run pytest -m "not requires_data"

# Run with detailed coverage
uv run pytest --cov-report=term-missing
```

### Linting and Formatting
```bash
# Run ruff linter
uv run ruff check src/ tests/

# Auto-fix issues
uv run ruff check --fix src/ tests/

# Format code
uv run ruff format src/ tests/
```

### Documentation
```bash
# Generate documentation
illustris -docs -generate

# Serve documentation locally
illustris -docs -serve
```

### CLI Tools
```bash
# Download test data (~5.3 GB)
illustris -data -test

# Download specific snapshot
illustris -data -load TNG50-4 -snap 99

# List available simulations
illustris -data -list-sims
```

## Code Style and Conventions

### Python Style
- Follow **PEP 8** with 88 character line length (Black/Ruff standard)
- Use **type hints** where appropriate (project uses mypy configuration)
- Import organization: standard library → third-party → local imports
- Use **descriptive variable names** (e.g., `snapNum`, `partType`, `basePath`)

### Naming Conventions
- **Functions**: camelCase (e.g., `loadSubset`, `loadHalos`) - matches original illustris_python API
- **Variables**: camelCase for parameters matching function signatures
- **Constants**: UPPER_CASE
- **Classes**: PascalCase (if any)

### Testing Practices
- Use **pytest markers**: `@pytest.mark.requires_data` for tests needing downloaded data
- Use **session-scoped fixtures** from conftest.py (e.g., `test_data_path`, `test_snapshot`)
- Tests should **skip gracefully** if required data is not available
- Add descriptive docstrings to test functions
- Test file naming: `test_*.py`

### Documentation
- Use **NumPy-style docstrings** for functions
- Include parameter types and return types
- Provide usage examples in docstrings
- Keep README.md updated with new features

## Important Notes

### API Compatibility
- Maintain **backward compatibility** with original illustris_python API
- Core functions (loadSubset, loadHalos, etc.) should have consistent signatures
- New features should be additive, not breaking

### Data Handling
- Simulation data files are **HDF5 format** using h5py
- Data directory is **not committed** to git (in .gitignore)
- API key for TNG downloads stored in `.env` file (use python-dotenv)
- Handle missing data gracefully with informative error messages

### Dependencies
- Core: `h5py`, `numpy`, `six`, `httpx`, `python-dotenv`
- Dev: `pytest`, `pytest-cov`, `sphinx`, `sphinx-rtd-theme`, `ruff`
- Minimize new dependencies - prefer standard library when possible

### Security
- Never commit API keys or secrets
- Use `.env` file for configuration (excluded from git)
- Validate file paths to prevent directory traversal
- Handle network errors and timeouts appropriately

## What NOT to Do

- Don't modify the original illustris_python API functions without maintaining compatibility
- Don't commit large data files or API keys
- Don't add unnecessary dependencies
- Don't remove or disable existing tests without good reason
- Don't modify files in the `data/` directory (it's for downloaded simulations)
- Don't change the camelCase naming convention for core API functions (it's intentional for compatibility)

## Git Workflow

### Branch Strategy
- **Main branch**: `main` (protected, requires PR for changes)
- **Feature branches**: `feature/description` or `fix/description`
- **Work directly on feature branches**: Never commit directly to main

### Commit Practices
- **Descriptive commits**: Use clear, concise commit messages
- **Atomic commits**: Each commit should represent a single logical change
- **Format**: Use imperative mood (e.g., "Add feature" not "Added feature")
- **Test before commit**: Ensure tests pass before committing

### Example Workflow
```bash
# Create feature branch
git checkout -b feature/new-loader

# Make changes and test
uv run pytest

# Stage and commit
git add src/illustris/newmodule.py tests/test_newmodule.py
git commit -m "Add new data loader for LHaloTree format"

# Push and create PR
git push origin feature/new-loader
```

### Pull Request Guidelines
- **Clear title**: Describe what the PR does
- **Description**: Include motivation, changes made, testing done
- **Tests**: All tests must pass (pytest)
- **Linting**: Code must pass ruff checks
- **Documentation**: Update docstrings and README if needed
- **Review**: Wait for review before merging

## Common Tasks

### Adding a New Feature
1. Create a feature branch: `git checkout -b feature/description`
2. Add functionality to appropriate module (snapshot.py, groupcat.py, etc.)
3. Write comprehensive tests in corresponding test file
4. Update docstrings with examples (NumPy style)
5. Run tests to ensure nothing breaks: `uv run pytest`
6. Run linter: `uv run ruff check --fix src/ tests/`
7. Update README.md if it's a user-facing feature
8. Commit changes with clear message
9. Push branch and create pull request

### Fixing a Bug
1. Create a fix branch: `git checkout -b fix/description`
2. Write a failing test that reproduces the bug
3. Fix the bug in the source code
4. Verify the test passes: `uv run pytest tests/test_specific.py`
5. Check that all other tests still pass: `uv run pytest`
6. Run linter: `uv run ruff check --fix src/ tests/`
7. Document the fix if it's a significant change
8. Commit and push for review

### Adding Tests
1. Use appropriate pytest markers (`@pytest.mark.requires_data`)
2. Use fixtures from conftest.py for test data access
3. Test both success and error cases
4. Ensure tests are isolated and deterministic
5. Add tests to existing test files in `tests/` directory
6. Run tests to verify: `uv run pytest tests/test_new.py -v`
7. Check coverage: `uv run pytest --cov-report=term-missing`

### Reviewing Code
- Check for API compatibility with original illustris_python
- Verify tests exist and pass
- Review docstrings for completeness
- Check for security issues (path validation, secret handling)
- Ensure camelCase naming is preserved for API functions

Remember: This is a scientific computing package that researchers depend on for analyzing multi-gigabyte astronomy simulation datasets. Stability, correctness, and API compatibility are critical.
