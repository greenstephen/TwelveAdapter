# PyPI Publishing Guide

## Overview

This guide explains how to publish the `nautilus-twelvedata` package to PyPI.

## Prerequisites

### 1. Create PyPI Account

- Go to https://pypi.org/
- Create an account (if you don't have one)
- Verify your email address

### 2. Create API Token

1. Go to https://pypi.org/manage/account/token/
2. Click "Add API token"
3. Select "Entire project"
4. Copy the token (starts with `pypi-`)
5. **Save it securely** - you won't be able to see it again!

### 3. Configure twine

Create `~/.pypirc`:

```ini
[pypi]
username = __token__
password = pypi-YOUR_TOKEN_HERE
```

Or use environment variable:

```bash
export TWINE_PASSWORD=pypi-YOUR_TOKEN_HERE
```

## Building the Package

### Build Wheels

```bash
# Install build tools
pip install maturin twine build

# Build wheels for all platforms
cd /home/steve/Projects/TwelveAdapter/crates/nautilus-twelvedata
maturin build --release

# Or build from project root
cd /home/steve/Projects/TwelveAdapter
maturin build --release
```

This creates wheels in `target/wheels/`:

```
nautilus_twelvedata-0.1.0-py3-none-manylinux_2_34_x86_64.whl
```

### Build Source Distribution

```bash
# For source distribution
maturin sdist --out dist/
```

## Testing Locally

### Install from Wheel

```bash
# Create test environment
python -m venv test_env
source test_env/bin/activate

# Install nautilus-trader first
pip install nautilus-trader

# Install from wheel
pip install /path/to/nautilus_twelvedata-0.1.0-py3-none-manylinux_2_34_x86_64.whl

# Test import
python -c "from nautilus_twelvedata import TwelveDataHttpClientPy; print('Success!')"
```

### Test with twine

```bash
# Check package
twine check dist/*
```

## Uploading to PyPI

### Upload to TestPyPI (Recommended First)

```bash
# Install twine
pip install twine

# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Or with explicit credentials
twine upload --repository testpypi \
  --username __token__ \
  --password pypi-YOUR_TOKEN \
  dist/*
```

### Test on TestPyPI

```bash
# Create test environment
python -m venv test_env
source test_env/bin/activate

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple \
  nautilus-twelvedata

# Test
python -c "import nautilus_twelvedata; print(nautilus_twelvedata.__version__)"
```

### Upload to Production PyPI

```bash
# Upload to PyPI
twine upload dist/*

# Or with explicit credentials
twine upload \
  --username __token__ \
  --password pypi-YOUR_TOKEN \
  dist/*
```

## Verify Publication

### Check on PyPI

Visit: https://pypi.org/project/nautilus-twelvedata/

### Install from PyPI

```bash
# Create new environment
python -m venv new_env
source new_env/bin/activate

# Install from PyPI
pip install nautilus-twelvedata

# Verify
python -c "import nautilus_twelvedata; print(nautilus_twelvedata.__version__)"
```

## Common Issues

### Issue: Permission Denied

**Solution**: Make sure you're using an API token, not your password.

### Issue: File Already Exists

**Solution**: Increment the version number in `Cargo.toml` or `pyproject.toml`.

### Issue: Invalid Distribution

**Solution**: Run `twine check dist/*` to validate before uploading.

### Issue: Missing Dependencies

**Solution**: Ensure `pyproject.toml` lists all dependencies correctly.

## Version Management

### Bump Version

Update version in:
1. `pyproject.toml`
2. `Cargo.toml`
3. `CHANGELOG.md`

```toml
# pyproject.toml
version = "1.0.1"
```

```toml
# Cargo.toml
[package]
version = "0.1.1"
```

### Semantic Versioning

- **MAJOR** (1.0.0 → 2.0.0): Breaking changes
- **MINOR** (1.0.0 → 1.1.0): New features, backward compatible
- **PATCH** (1.0.0 → 1.0.1): Bug fixes

## Publishing Checklist

- [ ] Update version number
- [ ] Update CHANGELOG.md
- [ ] Run tests: `python run_tests.py`
- [ ] Build wheels: `maturin build --release`
- [ ] Check package: `twine check dist/*`
- [ ] Upload to TestPyPI
- [ ] Test on TestPyPI
- [ ] Upload to PyPI
- [ ] Verify on PyPI
- [ ] Update GitHub release
- [ ] Announce to community

## Automated Publishing (GitHub Actions)

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Install Rust
        uses: actions-rs/toolchain@v1
        with:
          toolchain: stable
      
      - name: Install Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Build wheel
        run: |
          pip install maturin
          maturin build --release
      
      - name: Upload to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          password: ${{ secrets.PYPI_API_TOKEN }}
```

## Security

### Protect API Tokens

- Never commit tokens to git
- Use environment variables
- Rotate tokens periodically
- Use separate tokens for TestPyPI and PyPI

### .gitignore

Make sure `.gitignore` includes:

```
.env
*.pem
*.key
```

## Support

- **PyPI Help**: https://pypi.org/help/
- **twine Docs**: https://twine.readthedocs.io/
- **maturin Docs**: https://maturin.rs/

## Quick Reference

```bash
# Build
maturin build --release

# Check
twine check dist/*

# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Upload to PyPI
twine upload dist/*

# Install locally
pip install dist/nautilus_twelvedata-*.whl

# Test import
python -c "from nautilus_twelvedata import TwelveDataHttpClientPy"
```

---

**Ready to Publish?** Follow the checklist above!
