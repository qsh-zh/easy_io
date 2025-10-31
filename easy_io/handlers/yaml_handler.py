import yaml

try:
    from yaml import CDumper as Dumper  # type: ignore[attr-defined]
    from yaml import CLoader as Loader  # type: ignore[attr-defined]
except ImportError:
    from yaml import Dumper, Loader  # type: ignore[assignment]

from easy_io.handlers.base import BaseFileHandler  # isort:skip


class YamlHandler(BaseFileHandler):
    def load_from_fileobj(self, file, **kwargs):
        kwargs.setdefault("Loader", Loader)
        return yaml.safe_load(file, **kwargs)

    def dump_to_fileobj(self, obj, file, **kwargs):
        kwargs.setdefault("Dumper", Dumper)
        yaml.dump(obj, file, **kwargs)

    def dump_to_str(self, obj, **kwargs):
        kwargs.setdefault("Dumper", Dumper)
        return yaml.dump(obj, **kwargs)
