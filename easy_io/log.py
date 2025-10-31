import atexit
import os
import sys
from typing import Any, Optional

import torch.distributed as dist
from loguru._logger import Core, Logger

RANK0_ONLY = True
LEVEL = os.environ.get("EASY_IO_LOG_LEVEL", "INFO")
EASY_LOG_LOG_TAG = os.environ.get("EASY_LOG_LOG_TAG", "EASY_IO")


def make_new_logger(depth: int = 1) -> Logger:
    return Logger(
        core=Core(),
        exception=None,
        depth=depth,
        record=False,
        lazy=False,
        colors=False,
        raw=False,
        capture=True,
        patchers=[],
        extra={},
    )


logger = make_new_logger(depth=1)
atexit.register(logger.remove)


def _add_relative_path(record: dict[str, Any]) -> None:
    start = os.getcwd()
    record["extra"]["relative_path"] = os.path.relpath(record["file"].path, start)


*options, _, extra = logger._options  # type: ignore[attr-defined]
logger._options = (*options, [_add_relative_path], extra)  # type: ignore[assignment]


def init_loguru_stdout() -> None:
    logger.remove()
    datetime_format = get_datetime_format()
    machine_format = get_machine_format()
    message_format = get_message_format()
    logger.add(
        sys.stdout,
        level=LEVEL,
        format=f"{datetime_format}{machine_format}{message_format}",
        filter=_rank0_only_filter,
    )


def init_loguru_file(path: str) -> None:
    datetime_format = get_datetime_format()
    machine_format = get_machine_format()
    message_format = get_message_format()
    logger.add(
        path,
        encoding="utf8",
        level=LEVEL,
        format=f"{datetime_format}{machine_format}{message_format}",
        rotation="100 MB",
        filter=lambda result: _rank0_only_filter(result) or not RANK0_ONLY,
        enqueue=True,
    )


def get_datetime_format() -> str:
    return EASY_LOG_LOG_TAG + " [<green>{time:MM-DD HH:mm:ss}</green>|"


def get_machine_format() -> str:
    machine_format = ""
    rank = 0
    if dist.is_available():  # noqa: SIM102
        if not RANK0_ONLY and dist.is_initialized():
            rank = dist.get_rank()
            world_size = dist.get_world_size()
            machine_format = f"<red>[RANK{rank:<5}/{world_size:<5}]" + "[{process.name:<8}]</red>| "
    return machine_format


def get_message_format() -> str:
    message_format = "<level>{level}</level>|<cyan>{extra[relative_path]}:{line}:{function}</cyan>] {message}"
    return message_format


def _rank0_only_filter(record: Any) -> bool:
    is_rank0 = record["extra"].get("rank0_only", True)
    if _get_rank() == 0 and is_rank0:
        return True
    if not is_rank0:
        record["message"] = f"[RANK {_get_rank()}]" + record["message"]
    return not is_rank0


def trace(message: str, rank0_only: bool = True) -> None:
    logger.opt(depth=1).bind(rank0_only=rank0_only).trace(message)


def debug(message: str, rank0_only: bool = True) -> None:
    logger.opt(depth=1).bind(rank0_only=rank0_only).debug(message)


def info(message: str, rank0_only: bool = True) -> None:
    logger.opt(depth=1).bind(rank0_only=rank0_only).info(message)


def success(message: str, rank0_only: bool = True) -> None:
    logger.opt(depth=1).bind(rank0_only=rank0_only).success(message)


def warning(message: str, rank0_only: bool = True) -> None:
    logger.opt(depth=1).bind(rank0_only=rank0_only).warning(message)


def error(message: str, rank0_only: bool = True) -> None:
    logger.opt(depth=1).bind(rank0_only=rank0_only).error(message)


def critical(message: str, rank0_only: bool = True) -> None:
    logger.opt(depth=1).bind(rank0_only=rank0_only).critical(message)


def exception(message: str, rank0_only: bool = True) -> None:
    logger.opt(depth=1).bind(rank0_only=rank0_only).exception(message)


def _get_rank(group: Optional[dist.ProcessGroup] = None) -> int:
    """Get the rank (GPU device) of the worker.

    Returns:
        rank (int): The rank of the worker.
    """
    rank = 0
    if dist.is_available() and dist.is_initialized():
        rank = dist.get_rank(group)
    return rank


# Execute at import time.
init_loguru_stdout()
