How-To Guides
=============

This section collects practical recipes that expand on the high-level
overview and quickstart. Each topic highlights a common scenario and
links directly to the utility or backend code in ``easy_io``.


Configure Storage Backends
--------------------------

Most production deployments mix several storage systems. The snippets
below demonstrate how to blend local paths, HTTP downloads, and S3
buckets in a single process.

Local and HTTP
~~~~~~~~~~~~~~

.. code-block:: python

   from easy_io import get, get_local_path

   # Read a file from the local filesystem
   text = get("workspace/README.md")

   # Stream a remote artifact but operate on the downloaded temporary file
   with get_local_path("https://datasets.example.com/imagenet/labels.txt") as tmp:
       with open(tmp, "r", encoding="utf-8") as handle:
           labels = [line.strip() for line in handle]

S3 With Explicit Credentials
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``easy_io`` separates backend configuration from I/O helpers. Register an
S3 backend once and subsequent calls will reuse the client:

.. code-block:: python

   from easy_io import set_s3_backend, put_text, list_dir_or_file

   set_s3_backend(
       backend_args={
           "backend": "s3",
           "s3_credential_path": "~/.config/easy-io/s3.secret",
           "path_mapping": None,
       }
   )

   put_text("hello", "s3://demo-bucket/examples/hello.txt")

   for key in list_dir_or_file("s3://demo-bucket/examples/", list_file=True, recursive=True):
       print(key)


Customising Logging
-------------------

The ``easy_io.log`` module wraps ``loguru`` so that distributed jobs share
consistent formatting. Environment variables control the defaults:

``EASY_IO_LOG_LEVEL``
   One of ``TRACE``, ``DEBUG``, ``INFO`` (default), ``SUCCESS``, ``WARNING``,
   ``ERROR``, or ``CRITICAL``.

``EASY_LOG_LOG_TAG``
   Prefix appended to the timestamp column. Useful for multi-service logs.

Advanced consumers may call the helpers directly:

.. code-block:: python

   from easy_io import log

   log.init_loguru_stdout()           # reset sinks for interactive notebooks
   log.info("Warmup complete")
   log.debug("Detailed trace", rank0_only=False)

   # Persist to disk while preserving rank-aware filtering
   log.init_loguru_file("/tmp/easy-io.log")


GPU-Aware Test Suites
---------------------

``easy_io.test_utils`` provides a ``RunIf`` decorator for parametrised
skipping. Combine it with ``pytest`` marks to ensure GPU-heavy tests run
only on machines that satisfy hardware and dependency constraints.

.. code-block:: python

   import numpy as np
   import pytest

   from easy_io import load, dump
   from easy_io.test_utils import RunIf


   @pytest.mark.integration
   @RunIf(min_gpus=1, supported_arch=["H100", "A100"], requires_package=["torch"])
   def test_fast_video_roundtrip(tmp_path):
       frames, metadata = load("s3://datasets/demo/clip.mp4")
       dump(frames, tmp_path / "roundtrip.mp4", format="mp4", fps=metadata.get("fps", 30))


Command Execution Helpers
-------------------------

Need a resilient subprocess runner for your CI scripts or stress tests?
``easy_io.test_utils.run_command`` retries shell commands and surfaces
clear diagnostics after the final attempt fails.

.. code-block:: python

   from easy_io.test_utils import run_command

   result = run_command("aws s3 ls s3://demo-bucket --recursive", max_retry_counter=5)
   print(result.stdout)

   # Prevent hard failures in exploratory notebooks
   run_command("make flaky-target", is_raise=False)
