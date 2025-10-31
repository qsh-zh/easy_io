import json
from typing import IO

import numpy as np

from easy_io.handlers.base import BaseFileHandler


def set_default(obj):
    """Set default json values for non-serializable values.

    It helps convert ``set``, ``range`` and ``np.ndarray`` data types to list.
    It also converts ``np.generic`` (including ``np.int32``, ``np.float32``,
    etc.) into plain numbers of plain python built-in types.
    """
    if isinstance(obj, (set, range)):
        return list(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, np.generic):
        return obj.item()
    raise TypeError(f"{type(obj)} is unsupported for json dump")


class JsonlHandler(BaseFileHandler):
    """Handler for JSON lines (JSONL) files."""

    def load_from_fileobj(self, file: IO[bytes]):
        """Load JSON objects from a newline-delimited JSON (JSONL) file object.

        Returns:
            A list of Python objects loaded from each JSON line.
        """
        data = []
        for line in file:
            line = line.strip()
            if not line:
                continue  # skip empty lines if any
            data.append(json.loads(line))
        return data

    def dump_to_fileobj(self, obj: IO[bytes], file, **kwargs):
        """Dump a list of objects to a newline-delimited JSON (JSONL) file object.

        Args:
            obj: A list (or iterable) of objects to dump line by line.
        """
        kwargs.setdefault("default", set_default)
        for item in obj:
            file.write(json.dumps(item, **kwargs) + "\n")

    def dump_to_str(self, obj, **kwargs):
        """Dump a list of objects to a newline-delimited JSON (JSONL) string."""
        kwargs.setdefault("default", set_default)
        lines = [json.dumps(item, **kwargs) for item in obj]
        return "\n".join(lines)


if __name__ == "__main__":
    from easy_io import easy_io

    easy_io.dump([1, 2, 3], "test.jsonl", file_format="jsonl")
    print(easy_io.load("test.jsonl"))
    easy_io.dump([{"key1": 1, "key2": 2}, {"key1": 3, "key2": 4}], "test.jsonl", file_format="jsonl")
    print(easy_io.load("test.jsonl"))
