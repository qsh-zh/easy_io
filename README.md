# easy_io

`easy_io` provides pluggable file backends (local, HTTP/S, S3) and format
handlers for common data types (text, JSON, YAML, pickle, numpy arrays, etc.).
The project draws inspiration from [mmengine](https://github.com/open-mmlab/mmengine)
and the [jammy](https://gitlab.com/qsh.zh/jam/) toolbox while re-packaging
the ideas into a focused, backend-oriented IO helper.

## Environment Setup

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

`easy_io.log` prefixes messages with `EASY_LOG_LOG_TAG` (defaults to
`EASY_IO`) and defaults to rank-zero logging when `torch.distributed` is
initialized. Set `easy_io.log.RANK0_ONLY = False` in code if you need messages
from every worker.

## Quickstart

```bash
uv sync
uv run python -c "import easy_io; print(easy_io.get_text('README.md'))"
```

### Development

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

### Release tooling

```bash
uv sync --group release
uv run python -m build
uv run twine check dist/*
```

### Manual publish (developers)

```bash
uv sync --group release
export UV_PUBLISH_TOKEN="$(pass show pypi/token)"  # orexport from your secret manager
uv publish --token "$UV_PUBLISH_TOKEN"
```

## Publishing

Publishing to PyPI is automated via GitHub Actions (`.github/workflows/publish.yml`).
Create a PyPI trusted publisher or add the `PYPI_API_TOKEN` repository secret. Then
tag a release:

```bash
git tag v0.1.0
git push origin v0.1.0
```

The workflow will build and publish the project with `uv publish`.

## Project Structure

- `pyproject.toml` – project metadata and dependency management (driven by uv)
- `easy_io/` – package source code
- `docs/` – Sphinx sources for the documentation portal
