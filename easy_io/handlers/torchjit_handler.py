try:
    import torch
except ImportError:
    torch = None

from easy_io.handlers.base import BaseFileHandler


class TorchJitHandler(BaseFileHandler):
    str_like = False

    def load_from_fileobj(self, file, **kwargs):
        return torch.jit.load(file, **kwargs)

    def dump_to_fileobj(self, obj, file, **kwargs):
        torch.jit.save(obj, file, **kwargs)

    def dump_to_str(self, obj, **kwargs):
        raise NotImplementedError
