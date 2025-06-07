# Documentation Deployment

This document explains how to deploy the Illustris Python documentation.

## GitHub Pages

### Automatic Deployment

The documentation is automatically built and deployed to GitHub Pages when:

- Code is pushed to the `main` or `master` branch
- A pull request is created (build only, no deployment)
- Manually triggered via GitHub Actions

### Setup Instructions

1. **Enable GitHub Pages**:
   - Go to repository Settings → Pages
   - Source: "GitHub Actions"
   - The workflow will handle the rest

2. **Workflow Configuration**:
   - File: `.github/workflows/docs.yml`
   - Uses uv for fast dependency management
   - Builds with `illustris -docs -generate`
   - Deploys to `https://username.github.io/illustris_python`

### Manual Build

```bash
# Install documentation dependencies
uv sync --group docs

# Build documentation
uv run illustris -docs -generate

# Serve locally
uv run illustris -docs -serve
```

## Read the Docs

### Automatic Deployment

The documentation is automatically built on Read the Docs when:

- Code is pushed to any branch
- Pull requests are created
- Webhooks are triggered

### Setup Instructions

1. **Connect Repository**:
   - Go to https://readthedocs.org/
   - Import project from GitHub
   - Select the illustris_python repository

2. **Configuration**:
   - File: `.readthedocs.yml`
   - Uses Python 3.11 and uv
   - Builds HTML, PDF, and EPUB formats
   - Available at `https://illustris-python.readthedocs.io/`

3. **Advanced Settings**:
   - Default branch: `main`
   - Default version: `latest`
   - Privacy level: Public

### Build Process

Read the Docs will:

1. Install uv in the build environment
2. Run `uv sync --group docs` to install dependencies
3. Build documentation with Sphinx
4. Generate HTML, PDF, and EPUB formats
5. Deploy to the Read the Docs CDN

## Local Development

### Quick Start

```bash
# Install all dependencies including docs
uv sync --group docs

# Build documentation
uv run illustris -docs -generate

# Serve with live reload
uv run illustris -docs -serve -p 8080
```

### Advanced Options

```bash
# Clean build
rm -rf docs/_build/
uv run illustris -docs -generate

# Check for broken links
uv run sphinx-build -b linkcheck docs/ docs/_build/linkcheck/

# Build specific format
uv run sphinx-build -b html docs/ docs/_build/html/
uv run sphinx-build -b pdf docs/ docs/_build/pdf/
```

## Troubleshooting

### Common Issues

**Build Fails on GitHub Actions**:
- Check the workflow logs in the Actions tab
- Ensure all dependencies are in `pyproject.toml`
- Verify the CLI command works locally

**Read the Docs Build Fails**:
- Check the build logs on readthedocs.org
- Ensure `.readthedocs.yml` is valid
- Test the build locally with the same Python version

**Missing Dependencies**:
```bash
# Add missing packages to docs group
uv add --group docs package-name

# Or edit pyproject.toml directly
[dependency-groups]
docs = [
    "sphinx>=8.2.3",
    "sphinx-rtd-theme>=3.0.0",
    "myst-parser>=4.0.0",
    "new-package>=1.0.0",
]
```

**Broken Links**:
```bash
# Check for broken internal links
uv run sphinx-build -b linkcheck docs/ docs/_build/linkcheck/

# Fix broken references in .rst files
# Update URLs in conf.py
```

### Performance Optimization

**Faster Builds**:
- Use uv instead of pip (already configured)
- Cache dependencies in CI (GitHub Actions caches automatically)
- Minimize extensions in `conf.py`

**Smaller Output**:
- Optimize images in `docs/_static/`
- Use compressed formats for large files
- Enable gzip compression on hosting

## Monitoring

### GitHub Pages

- Status: Repository Settings → Pages
- Analytics: GitHub Insights → Traffic
- Logs: Actions tab → Latest workflow run

### Read the Docs

- Dashboard: https://readthedocs.org/projects/illustris-python/
- Build logs: Builds tab
- Analytics: Admin → Analytics

## Custom Domain (Optional)

### GitHub Pages

1. Add `CNAME` file to `docs/` directory:
   ```
   docs.illustris-python.org
   ```

2. Configure DNS:
   ```
   CNAME docs.illustris-python.org username.github.io
   ```

### Read the Docs

1. Go to Admin → Domains
2. Add custom domain: `docs.illustris-python.org`
3. Configure DNS as instructed

## Security

### GitHub Pages

- HTTPS is enforced automatically
- No sensitive data in documentation
- API keys excluded via `.gitignore`

### Read the Docs

- Public documentation only
- No authentication required
- Secure HTTPS delivery

## Maintenance

### Regular Tasks

- Update dependencies monthly
- Check for broken links quarterly
- Review analytics for popular content
- Update examples with new features

### Version Management

- Tag releases for stable documentation
- Use branch-specific builds for development
- Archive old versions as needed

For questions or issues, check the GitHub repository issues or contact the maintainers. 