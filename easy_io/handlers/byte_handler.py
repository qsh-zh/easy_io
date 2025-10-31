from typing import IO

from easy_io.handlers.base import BaseFileHandler


class ByteHandler(BaseFileHandler):
    str_like = False

    def load_from_fileobj(self, file: IO[bytes], **kwargs):
        file.seek(0)
        # extra all bytes and return
        return file.read()

    def dump_to_fileobj(
        self,
        obj: bytes,
        file: IO[bytes],
        **kwargs,
    ):
        # write all bytes to file
        file.write(obj)

    def dump_to_str(self, obj, **kwargs):
        raise NotImplementedError
