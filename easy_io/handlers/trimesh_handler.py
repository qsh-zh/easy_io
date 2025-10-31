from typing import IO

import trimesh

from easy_io.handlers.base import BaseFileHandler


class TrimeshHandler(BaseFileHandler):
    format: str
    str_like = False

    def load_from_fileobj(self, file: IO[bytes], **kwargs) -> trimesh.Trimesh:
        file = trimesh.load(file_obj=file, file_type=self.format)
        return file

    def dump_to_fileobj(self, obj, file: IO[bytes], **kwargs):
        obj.export(file_obj=file, file_type=self.format)
        return file

    def dump_to_str(self, obj, **kwargs):
        raise NotImplementedError
