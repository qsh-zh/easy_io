<h1 align="center">easy_io</h1>

<p align="center">
  <a href="https://pypi.org/project/py-ezio/">
    <img src="https://img.shields.io/pypi/v/py-ezio?style=for-the-badge" alt="PyPI" />
  </a>
  <a href="https://pypi.org/project/py-ezio/">
    <img src="https://img.shields.io/pypi/l/py-ezio?style=for-the-badge" alt="PyPI - License" />
  </a>
  <a href="https://github.com/qsh-zh/easy_io">
    <img src="https://img.shields.io/badge/-github-grey?style=for-the-badge&logo=github" alt="GitHub code" />
  </a>
  <a href="https://qsh-zh.github.io/easy_io/">
    <img src="https://img.shields.io/badge/docs-gh--pages-blue?style=for-the-badge" alt="Project Docs" />
  </a>
  <a href="https://pypi.org/project/py-ezio/">
    <img src="https://img.shields.io/pypi/pyversions/py-ezio?style=for-the-badge" alt="PyPI - Python Version" />
  </a>
</p>

<p align="center">
  <i>Simple load/dump APIs with pluggable storage backends and rich format handlers.</i>
</p>

## Introduction

`easy_io` provides simple read/write primitives (`easy_io.load` and `easy_io.dump`) backed by pluggable storage engines (local files, HTTP/S endpoints, S3 buckets, and more) and format handlers for common data modalities (text, JSON, YAML, pickle, numpy arrays, etc.).

The project draws inspiration from [mmengine](https://github.com/open-mmlab/mmengine) and the [jammy](https://gitlab.com/qsh.zh/jam/) toolbox while re-packaging the ideas into a focused, backend-oriented IO helper.

## User Guide

### Installation

```bash
pip install py-ezio
```

### Quickstart

```python
import easy_io

print(easy_io.get_text("README.md"))
```

### Common Workflows

#### Local file round-trip

```python
import easy_io

dummy_dict = {"a": 1, "b": 2}

easy_io.dump(dummy_dict, "dummy_dict.pkl")
loaded = easy_io.load("dummy_dict.pkl")

assert loaded == dummy_dict

easy_io.remove("dummy_dict.pkl")
```

#### Configure the S3 backend

```python
import easy_io

easy_io.set_s3_backend(
    backend_args={
        "backend": "s3",
        "path_mapping": None,
        "s3_credential_path": "credentials/abc.secret",
    }
)

for ith, path in enumerate(easy_io.list_dir_or_file("s3://checkpoints/")):
    if ith > 5:
        break
    print(path)

easy_io.copyfile_from_local(
    "pyproject.toml",
    "s3://checkpoints/pyproject.toml",
)
easy_io.remove("s3://checkpoints/pyproject.toml")
```

### CLI helper: `ezio_load`

Installations from PyPI expose an `ezio_load` entry point for quick inspection of
one or more files. Each file is loaded with `easy_io.load` and registered in an
interactive IPython session as `f1`, `f2`, etc.

```bash
ezio_load data/example.pkl
```

You can pass multiple paths (local or remote). When you exit the IPython shell,
the command ends.

## Developer Guide

### Environment Setup

```bash
# 1. Use Python 3.9+ and install uv if it is not already available
pip install uv

# 2. Create an isolated environment (uv uses .venv by default)
uv venv

# 3. Activate the virtual environment
source .venv/bin/activate  # or the Windows/conda equivalent

# 4. Install the core dependencies
uv sync

# Optional: tune logging verbosity for CLI sessions
export EASY_IO_LOG_LEVEL=DEBUG

# Optional: change the log tag prefix shown in log lines
export EASY_LOG_LOG_TAG="MyService"
```

`easy_io.log` prefixes messages with `EASY_LOG_LOG_TAG` (defaults to `EASY_IO`) and
defaults to rank-zero logging when `torch.distributed` is initialized. Set
`easy_io.log.RANK0_ONLY = False` in code if you need messages from every worker.

### Tests and linting

```bash
uv sync --dev
uv run pytest
uv run ruff check
```

### Documentation

```bash
uv sync --group docs
uv run sphinx-build -b html docs docs/_build/html
python -m http.server --directory docs/_build/html 8000
```

Published documentation is available at https://qsh-zh.github.io/easy_io/ once the `Docs` workflow has run (triggered automatically on pushes to `main` or manually via GitHub Actions).

### Release tooling

```bash
uv sync --group release
uv run python -m build
uv run twine check dist/*
```

### Publishing

Publishing to PyPI is automated via GitHub Actions (`.github/workflows/publish.yml`).
Create a PyPI trusted publisher or add the `PYPI_API_TOKEN` repository secret. Then
tag a release using a semantic version (no leading `v`):

```bash
git tag 0.1.0
git push origin 0.1.0
```

Tags must follow the `MAJOR.MINOR.PATCH` pattern (for example, `1.2.3`).

The workflow will build and publish the project with `uv publish`.

For manual publishes:

```bash
uv sync --group release
export UV_PUBLISH_TOKEN="$(pass show pypi/token)"  # or export from your secret manager
uv publish --token "$UV_PUBLISH_TOKEN"
```

### Project Structure

- `pyproject.toml` – project metadata and dependency management (driven by uv)
- `easy_io/` – package source code
- `docs/` – Sphinx sources for the documentation portal

### Contributing

Contributions are welcome! Please open an issue or pull request describing the
change you would like to make. Run the full test and lint suite before submitting
and follow the existing code style. If your change affects user workflows, update
the documentation and add regression tests where practical.
