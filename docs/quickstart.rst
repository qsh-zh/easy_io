Quickstart
==========

Environment setup
-----------------

.. code-block:: bash

   # Python 3.9+ and uv are required for the documented workflows
   pip install uv

   # Create and activate an isolated environment managed by uv
   uv venv
   source .venv/bin/activate

   # Install the core dependency set
   uv sync

   # Optional: enable GPU-aware utilities used in the examples below
   uv pip install pynvml

Set ``EASY_IO_LOG_LEVEL`` when you want more verbose diagnostics from
``easy_io.log`` (defaults to ``INFO``)::

   export EASY_IO_LOG_LEVEL=DEBUG

Set ``EASY_LOG_LOG_TAG`` to customize the log prefix (defaults to ``EASY_IO``)::

   export EASY_LOG_LOG_TAG=MyService

Installation
------------

.. code-block:: bash

   uv sync

Small example
-------------

.. code-block:: python

   import easy_io

   easy_io.put_text("hello", "examples/hello.txt")
   assert easy_io.get_text("examples/hello.txt") == "hello"

S3 with credentials in ``backend_args``:

.. code-block:: python

   backend = {
       "access_key": "***",
       "secret_key": "***",
       "endpoint_url": "https://s3.example.com",
   }
   easy_io.put(b"payload", "s3://bucket/key.bin", backend_args=backend)

Backend selection
-----------------

``easy_io`` chooses a backend based on the URI prefix or an explicit ``backend``
argument. The snippet below demonstrates how to pin the local backend even for
paths that resemble URLs.

.. code-block:: python

   from easy_io import FileClient

   client = FileClient(backend="disk")
   path = client.put_text("temporary", "results/output.txt")
   assert path.endswith("output.txt")

   with client.get_local_path("https://example.com/weights.bin") as tmp:
       print(f"Downloaded weights to {tmp}")

Command-line helpers
--------------------

You can expose recurring workflows via console scripts (see
``[project.scripts]`` in :doc:`changelog`).

Development tasks
-----------------

.. code-block:: bash

   uv sync --group dev
   uv run ruff check
   uv run pytest

Documentation site
------------------

.. code-block:: bash

   uv sync --group docs
   uv run sphinx-build -b html docs docs/_build/html

Release tooling
---------------

.. code-block:: bash

   uv sync --group release
   uv run python -m build
   uv run twine check dist/*


Testing recipes
---------------

``easy_io.test_utils`` offers decorators and helpers that keep GPU-dependent
tests and external service calls manageable. After installing ``pynvml`` you
can opt-in to tests that require specific accelerators or minimum dependency
versions.

.. code-block:: python

   import pytest

   from easy_io import dump, load
   from easy_io.test_utils import RunIf


   @pytest.mark.slow
   @RunIf(min_gpus=1, supported_arch=["H100", "A100"], requires_package="torch")
   def test_video_roundtrip(tmp_path):
       frames, metadata = load("s3://datasets/demo/clip.mp4")
       dump(frames, tmp_path / "roundtrip.mp4", format="mp4", fps=metadata.get("fps", 30))
