Handler Reference
=================

.. currentmodule:: easy_io.handlers

Registry
--------

.. autodata:: file_handlers
   :annotation: Dict[str, Type[BaseFileHandler]]

.. autofunction:: register_handler


Concrete Handlers
-----------------

.. autoclass:: BaseFileHandler
   :members:
   :show-inheritance:

.. autoclass:: JsonHandler
   :members:
   :show-inheritance:

.. autoclass:: PickleHandler
   :members:
   :show-inheritance:

.. autoclass:: YamlHandler
   :members:
   :show-inheritance:
