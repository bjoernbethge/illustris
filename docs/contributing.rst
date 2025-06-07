Contributing
============

We welcome contributions to Illustris Python! This guide will help you get started.

Development Setup
-----------------

1. **Fork and Clone**:

   .. code-block:: bash

      git clone https://github.com/yourusername/illustris_python.git
      cd illustris_python

2. **Install Development Dependencies**:

   .. code-block:: bash

      # With uv (recommended)
      uv sync --group dev
      
      # With pip
      pip install -e ".[dev]"

3. **Download Test Data**:

   .. code-block:: bash

      illustris -data -test

4. **Run Tests**:

   .. code-block:: bash

      uv run pytest

Code Style
----------

We use modern Python tooling for code quality:

**Formatting**:

.. code-block:: bash

   # Format code with black
   black src/ tests/
   
   # Check formatting
   black --check src/ tests/

**Linting**:

.. code-block:: bash

   # Lint with ruff
   ruff check src/ tests/
   
   # Fix auto-fixable issues
   ruff check --fix src/ tests/

**Type Checking**:

.. code-block:: bash

   # Type check with mypy
   mypy src/

Testing
-------

**Run All Tests**:

.. code-block:: bash

   uv run pytest

**Run Specific Tests**:

.. code-block:: bash

   # Test specific module
   uv run pytest tests/test_snapshot.py
   
   # Test with coverage
   uv run pytest --cov=illustris

**Test Categories**:

- Tests requiring data are marked with ``@pytest.mark.requires_data``
- Tests automatically skip if data is not available
- Download test data with ``illustris -data -test``

Documentation
-------------

**Build Documentation**:

.. code-block:: bash

   illustris -docs -generate

**Serve Documentation**:

.. code-block:: bash

   illustris -docs -serve

**Documentation Structure**:

- ``docs/`` - Documentation source files
- ``docs/api/`` - Auto-generated API documentation
- ``docs/_build/`` - Built HTML documentation

Pull Request Process
--------------------

1. **Create Feature Branch**:

   .. code-block:: bash

      git checkout -b feature/your-feature-name

2. **Make Changes**:
   
   - Write clear, documented code
   - Add tests for new functionality
   - Update documentation if needed

3. **Test Your Changes**:

   .. code-block:: bash

      # Run tests
      uv run pytest
      
      # Check code style
      black --check src/ tests/
      ruff check src/ tests/
      
      # Build documentation
      illustris -docs -generate

4. **Commit and Push**:

   .. code-block:: bash

      git add .
      git commit -m "Add feature: description"
      git push origin feature/your-feature-name

5. **Create Pull Request**:
   
   - Use descriptive title and description
   - Reference any related issues
   - Include test results

Code Guidelines
---------------

**Python Style**:

- Follow PEP 8 (enforced by black and ruff)
- Use type hints where appropriate
- Write docstrings for public functions
- Keep functions focused and small

**Documentation**:

- Use NumPy-style docstrings
- Include examples in docstrings
- Update user guides for new features

**Testing**:

- Write tests for new functionality
- Use descriptive test names
- Test both success and error cases

**Commit Messages**:

- Use present tense ("Add feature" not "Added feature")
- Keep first line under 50 characters
- Include detailed description if needed

Areas for Contribution
----------------------

**High Priority**:

- Performance optimizations for large datasets
- Additional analysis examples
- Better error messages and user experience
- Memory usage optimizations

**Medium Priority**:

- Support for additional file formats
- Visualization utilities
- Parallel processing improvements
- Documentation improvements

**Good First Issues**:

- Fix typos in documentation
- Add more examples to docstrings
- Improve error messages
- Add unit tests for edge cases

Reporting Issues
----------------

**Bug Reports**:

Include:

- Python version and operating system
- Complete error message and traceback
- Minimal code example to reproduce
- Expected vs actual behavior

**Feature Requests**:

Include:

- Clear description of the feature
- Use case and motivation
- Proposed API or interface
- Willingness to implement

**Questions**:

- Check existing documentation first
- Search existing issues
- Provide context about what you're trying to achieve

Development Tips
----------------

**Working with Large Data**:

.. code-block:: python

   # Use test data for development
   basePath = "data/TNG50-4/output"  # Small test dataset
   
   # Load minimal data for testing
   data = illustris.snapshot.loadSubset(
       basePath, 99, "gas", 
       fields=["Coordinates"]  # Only what you need
   )

**Debugging**:

.. code-block:: python

   # Enable verbose logging
   import logging
   logging.basicConfig(level=logging.DEBUG)
   
   # Use IPython for interactive debugging
   import IPython; IPython.embed()

**Performance Testing**:

.. code-block:: bash

   # Profile code
   python -m cProfile -o profile.stats your_script.py
   
   # Memory profiling
   pip install memory-profiler
   python -m memory_profiler your_script.py

Release Process
---------------

For maintainers:

1. **Update Version**:
   
   - Update version in ``pyproject.toml``
   - Update ``CHANGELOG.md``

2. **Test Release**:

   .. code-block:: bash

      uv run pytest
      illustris -docs -generate

3. **Create Release**:

   .. code-block:: bash

      git tag v0.2.0
      git push origin v0.2.0

4. **Build and Publish**:

   .. code-block:: bash

      uv build
      uv publish

Getting Help
------------

- **Documentation**: Read the full documentation
- **Issues**: Check GitHub issues for similar problems
- **Discussions**: Use GitHub discussions for questions
- **Email**: Contact maintainers for sensitive issues

Thank you for contributing to Illustris Python! 