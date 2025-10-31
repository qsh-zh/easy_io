Overview
========

``easy_io`` provides a unified, pythonic interface for loading and storing
data across multiple storage backends (local filesystem, HTTP/S, S3, and
custom registries) and serialization formats (JSON, YAML, pickle, NumPy
arrays, video tensors, etc.).

Features
--------

- Backend registry inspired by `mmengine` but trimmed for lightweight use.
- Handler registry for tensors, arrays, structured data, YAML, pickle, JSON,
  videos, and more.
- Drop-in helpers (``easy_io.get`` / ``easy_io.put`` / ``easy_io.dump``) that
  mirror built-in I/O semantics while respecting backend-specific options.
- Batteries included: optional extras for ``torch`` video I/O, ``imageio``
  integrations, and ``pynvml``-powered GPU discovery for conditional tests.
- Loguru-backed logging with rank-aware formatting for distributed training
  jobs.

Design Principles
-----------------

- **Pluggable** – add new backends or handlers by registering implementations.
- **Lazy dependencies** – heavy integrations (PyTorch, Trimesh) remain
  optional historically, but the default distribution now includes popular
  adapters for convenience.
- **Typed API** – type hints across the public surface ease IDE integration.

Origins and credits
-------------------

``easy_io`` started as a lightweight wrapper around concepts from
`mmengine <https://github.com/open-mmlab/mmengine>`_ (Apache-2.0 License) and
borrows ideas from the internal ``jam`` tooling lineage. The original prototype
was inspired by the `jammy <https://gitlab.com/qsh.zh/jam/>`_ project (MIT
License); both served as design references for the current backend and handler
registries. The project has since grown to include first-class logging helpers
and reusable pytest utilities to keep GPU-dependent suites tidy.
