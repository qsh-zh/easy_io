import os
import tempfile
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path
from typing import Union
from urllib.parse import urlparse
from urllib.request import urlopen

from easy_io.backends.base_backend import BaseStorageBackend


class HTTPBackend(BaseStorageBackend):
    """HTTP and HTTPS storage bachend."""

    @staticmethod
    def _validate_url(filepath: str) -> None:
        parsed = urlparse(filepath)
        if parsed.scheme not in {"http", "https"}:
            raise ValueError("HTTPBackend only supports http and https URLs")

    def get(self, filepath: str) -> bytes:
        """Read bytes from a given ``filepath``.

        Args:
            filepath (str): Path to read data.

        Returns:
            bytes: Expected bytes object.

        Examples:
            >>> backend = HTTPBackend()
            >>> backend.get('http://path/of/file')
            b'hello world'
        """
        self._validate_url(filepath)
        return urlopen(filepath).read()  # noqa: S310

    def get_text(self, filepath, encoding="utf-8") -> str:
        """Read text from a given ``filepath``.

        Args:
            filepath (str): Path to read data.
            encoding (str): The encoding format used to open the ``filepath``.
                Defaults to 'utf-8'.

        Returns:
            str: Expected text reading from ``filepath``.

        Examples:
            >>> backend = HTTPBackend()
            >>> backend.get_text('http://path/of/file')
            'hello world'
        """
        self._validate_url(filepath)
        return urlopen(filepath).read().decode(encoding)  # noqa: S310

    @contextmanager
    def get_local_path(self, filepath: str) -> Generator[Union[str, Path], None, None]:
        """Download a file from ``filepath`` to a local temporary directory,
        and return the temporary path.

        ``get_local_path`` is decorated by :meth:`contxtlib.contextmanager`. It
        can be called with ``with`` statement, and when exists from the
        ``with`` statement, the temporary path will be released.

        Args:
            filepath (str): Download a file from ``filepath``.

        Yields:
            Iterable[str]: Only yield one temporary path.

        Examples:
            >>> backend = HTTPBackend()
            >>> # After existing from the ``with`` clause,
            >>> # the path will be removed
            >>> with backend.get_local_path('http://path/of/file') as path:
            ...     # do something here
        """
        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(self.get(filepath))
                temp_path = temp_file.name
            if temp_path is None:
                raise RuntimeError("Failed to create temporary file for HTTP download")
            yield temp_path
        finally:
            if temp_path is not None and os.path.exists(temp_path):
                os.remove(temp_path)
