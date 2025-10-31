Backend Reference
=================

.. currentmodule:: easy_io.backends

Registry
--------

.. autodata:: backends
   :annotation: Dict[str, Type[BaseStorageBackend]]

.. autodata:: prefix_to_backends
   :annotation: Dict[str, Type[BaseStorageBackend]]

.. autofunction:: register_backend


Concrete Backends
-----------------

Base interface
~~~~~~~~~~~~~~

.. autoclass:: BaseStorageBackend
   :members:
   :show-inheritance:

Local filesystem
~~~~~~~~~~~~~~~~

.. autoclass:: LocalBackend
   :members:
   :show-inheritance:

Amazon S3 / MinIO
~~~~~~~~~~~~~~~~~

.. autoclass:: Boto3Backend
   :members:
   :show-inheritance:

HTTP(S)
~~~~~~~

.. autoclass:: HTTPBackend
   :members:
   :show-inheritance:

MSC (object storage)
~~~~~~~~~~~~~~~~~~~~

.. autoclass:: MSCBackend
   :members:
   :show-inheritance:
