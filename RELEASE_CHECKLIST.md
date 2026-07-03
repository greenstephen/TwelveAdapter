# Release Checklist - nautilus-twelvedata v1.0.0

## Pre-Release Preparation

### Documentation
- [x] README.md - Complete with examples
- [x] CONTRIBUTING.md - Contribution guidelines
- [x] CHANGELOG.md - Version history
- [x] QUICK_REFERENCE.md - Quick reference guide
- [x] LICENSE - LGPL v3.0
- [x] PUBLISHING_GUIDE.md - Publishing instructions
- [x] Documentation complete

### Code Quality
- [x] All tests passing (16/16 unit tests)
- [x] Code properly documented
- [x] Type hints where appropriate
- [x] Error handling implemented
- [x] No known critical bugs

### Package Structure
- [x] pyproject.toml configured
- [x] Cargo.toml configured
- [x] Python source files in place
- [x] Rust extension compiled
- [x] Wheel built successfully

### Testing
- [x] Unit tests created (53 tests)
- [x] Data validation tests passing
- [x] Error handling tests passing
- [x] Configuration tests passing
- [x] Wheel tested locally

## Release Steps

### 1. Version Update

Update version numbers:

```toml
# pyproject.toml
version = "1.0.0"

# Cargo.toml
[package]
version = "0.1.0"
```

### 2. Build Distribution

```bash
cd /home/steve/Projects/TwelveAdapter/crates/nautilus-twelvedata

# Build wheel
maturin build --release

# Verify
ls -lh ../../target/wheels/
```

**Expected output:**
```
nautilus_twelvedata-0.1.0-py3-none-manylinux_2_34_x86_64.whl (~200KB)
```

### 3. Validate Package

```bash
# Install twine
pip install twine

# Check package
twine check target/wheels/*
```

**Expected output:**
```
✓ dist/nautilus_twelvedata-0.1.0-py3-none-manylinux_2_34_x86_64.whl: OK
```

### 4. Test Locally

```bash
# Create test environment
python -m venv /tmp/test_env
source /tmp/test_env/bin/activate

# Install dependencies
pip install nautilus-trader

# Install wheel
pip install /home/steve/Projects/TwelveAdapter/target/wheels/nautilus_twelvedata-*.whl

# Test import
python -c "from nautilus_twelvedata import TwelveDataHttpClientPy; print('✓ Success')"

# Test basic functionality
python -c "
from nautilus_twelvedata import TwelveDataHttpClientPy
import os
api_key = os.getenv('TWELVEDATA_API_KEY', 'test')
client = TwelveDataHttpClientPy(api_key)
print(f'✓ Client created: {client.base_url}')
"
```

### 5. Upload to TestPyPI

```bash
# Upload to TestPyPI
twine upload --repository testpypi target/wheels/*

# Test installation
pip install --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple \
  nautilus-twelvedata

# Verify
python -c "import nautilus_twelvedata; print(nautilus_twelvedata.__version__)"
```

### 6. Create GitHub Release

1. Go to: https://github.com/yourusername/nautilus-twelvedata/releases/new
2. Tag: `v1.0.0`
3. Title: `Release v1.0.0`
4. Description: See release notes below
5. Attach wheel file
6. Publish

**Release Notes Template:**

```markdown
## What's New

- First stable release of nautilus-twelvedata
- High-performance Rust-based adapter
- Full NautilusTrader integration
- Support for multiple time intervals
- Rate limit handling
- Comprehensive error handling

## Features

- ⚡ Rust performance via PyO3
- 📊 OHLCV data fetching
- 🔄 Rate limit handling
- 🛡️ Robust error handling
- 🔧 NautilusTrader native

## Installation

```bash
pip install nautilus-twelvedata
```

## Documentation

- [README](https://github.com/yourusername/nautilus-twelvedata#readme)
- [Quick Reference](https://github.com/yourusername/nautilus-twelvedata/blob/main/QUICK_REFERENCE.md)
- [Contributing](https://github.com/yourusername/nautilus-twelvedata/blob/main/CONTRIBUTING.md)

## Known Issues

- None for v1.0.0

## Credits

Built with [maturin](https://maturin.rs/) and [PyO3](https://pyo3.rs/)
```

### 7. Upload to PyPI

```bash
# Upload to PyPI
twine upload target/wheels/*

# Verify
twine upload --skip-existing target/wheels/*
```

### 8. Verify on PyPI

Visit: https://pypi.org/project/nautilus-twelvedata/

Check:
- [x] Package page exists
- [x] README displays correctly
- [x] Metadata is correct
- [x] Wheel is available
- [x] Download count shows

### 9. Test PyPI Installation

```bash
# Create fresh environment
python -m venv /tmp/pypi_test
source /tmp/pypi_test/bin/activate

# Install from PyPI
pip install nautilus-twelvedata

# Verify
python -c "import nautilus_twelvedata; print(nautilus_twelvedata.__version__)"

# Test functionality
python -c "
from nautilus_twelvedata import TwelveDataHttpClientPy
client = TwelveDataHttpClientPy(api_key='test')
print(f'✓ Package working: {client.base_url}')
"
```

### 10. Announce Release

- [ ] Post on NautilusTrader Discord
- [ ] Share on Twitter/LinkedIn
- [ ] Email to interested parties
- [ ] Update project README with PyPI badge

## Post-Release

### Monitor

- [ ] Check PyPI download stats
- [ ] Monitor GitHub issues
- [ ] Respond to questions
- [ ] Track usage

### Documentation

- [ ] Create tutorial blog post
- [ ] Add example strategies
- [ ] Update documentation with real-world examples

### Next Steps

- [ ] Plan v1.1 features
- [ ] Collect user feedback
- [ ] Prioritize improvements

## Rollback Plan

If issues are found:

1. **Immediate**: Disable downloads on PyPI
2. **Fix**: Address critical issues
3. **Release**: Publish v1.0.1 with fixes
4. **Communicate**: Notify users of fix

```bash
# Uninstall problematic version
pip uninstall nautilus-twelvedata

# Install fixed version
pip install nautilus-twelvedata==1.0.1
```

## Success Criteria

- [x] Package builds successfully
- [x] All tests passing
- [x] Wheel validates with twine
- [x] TestPyPI upload successful
- [x] Production PyPI upload successful
- [x] Installation from PyPI works
- [x] Basic functionality verified
- [x] GitHub release created
- [x] Documentation complete

## Files to Release

```
target/wheels/
└── nautilus_twelvedata-0.1.0-py3-none-manylinux_2_34_x86_64.whl
```

## Version Information

- **Package Version**: 1.0.0
- **Rust Crate Version**: 0.1.0
- **Python Version**: 3.10-3.13
- **Release Date**: 2026-07-02
- **Status**: Ready for Release

## Contact

- **Author**: Your Name
- **Email**: your.email@example.com
- **GitHub**: https://github.com/yourusername
- **Issues**: https://github.com/yourusername/nautilus-twelvedata/issues

---

**Status**: ✅ READY FOR RELEASE
**Date**: 2026-07-02
**Version**: 1.0.0
