# GitHub Workflows

This directory contains GitHub Actions workflows for automatically building Python wheel packages.

## Available Workflows

### 1. `build-wheels.yml` - Complete Build Pipeline
A comprehensive workflow that:
- Builds wheels for multiple Python versions (3.8, 3.9, 3.10, 3.11)
- Handles package dependencies correctly
- Tests wheel installations
- Includes optional publishing to TestPyPI
- Runs on push to main/master/develop branches and pull requests

### 2. `build-simple.yml` - Simple Build
A simplified workflow that:
- Builds wheels for both packages using Python 3.11
- Tests basic imports
- Uploads artifacts for download
- Runs on push to main/master branches and pull requests

## Packages Built

Both workflows build wheel files for:

1. **smart-choice** (`smart-choice/`)
   - Decision analysis library using decision trees
   - Built using existing `setup.py`

2. **smart_server** (`smart_server/`)
   - FastAPI server for decision analysis
   - Depends on smart-choice package
   - Uses automatically generated `setup.py`

## Workflow Triggers

The workflows are triggered on:
- Push to `main`, `master`, or `develop` branches
- Pull requests to `main` or `master` branches

## Artifacts

After successful builds, wheel files are uploaded as GitHub artifacts:
- `smart-choice-wheel` / `smart-choice-packages-py{version}`
- `smart_server-wheel` / `smart_server-packages-py{version}`

## Publishing (Optional)

The complete workflow includes commented sections for publishing to TestPyPI. To enable:

1. Uncomment the publishing steps in `build-wheels.yml`
2. Add `TESTPYPI_API_TOKEN` to your repository secrets
3. The packages will be automatically published when pushing to the main branch

## Dependencies

The build process handles dependencies correctly:
1. smart-choice is built first
2. smart-choice is installed locally
3. smart_server is built with smart-choice available as a dependency

## Testing

Both workflows include basic testing:
- Wheel installation verification
- Import testing to ensure packages load correctly
- Version information display where available