"""Adapted from:

https://github.com/PyTorchLightning/pytorch-lightning/blob/master/tests/helpers/runif.py
"""

import importlib.metadata
import subprocess
import sys
from pathlib import Path
from typing import Any, Optional, Union

import pynvml
import pytest
import torch
from loguru import logger
from packaging.version import Version
from pytest import MarkDecorator


def get_gpu_architecture():
    """
    Retrieves the GPU architecture of the available GPUs.

    Returns:
        str: The GPU architecture, which can be "H100", "A100", or "Other".
    """
    try:
        pynvml.nvmlInit()
        device_count = pynvml.nvmlDeviceGetCount()
        for i in range(device_count):
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            model_name = pynvml.nvmlDeviceGetName(handle)
            if isinstance(model_name, bytes):
                model_name = model_name.decode("utf-8")
            print(f"GPU {i}: Model: {model_name}")

            # Check for specific models like H100 or A100
            if "H100" in model_name or "H200" in model_name:
                return "H100"
            elif "A100" in model_name:
                return "A100"
            elif "L40S" in model_name:
                return "L40S"
            elif "B200" in model_name:
                return "B200"
    except pynvml.NVMLError as error:
        print(f"Failed to get GPU info: {error}")
    finally:
        pynvml.nvmlShutdown()

    # return "Other" incase of non hopper/ampere or error
    return "Other"


class RunIf:
    """RunIf wrapper for conditional skipping of tests.

    Fully compatible with ``@pytest.mark``.

    Example
    -------

    .. code-block:: python

        @RunIf(min_torch="1.8")
        @pytest.mark.parametrize("arg1", [1.0, 2.0])
        def test_wrapper(arg1):
            assert arg1 > 0
    """

    def __new__(  # noqa: C901
        cls,
        min_gpus: int = 0,
        min_torch: Optional[str] = None,
        max_torch: Optional[str] = None,
        min_python: Optional[str] = None,
        supported_arch: Optional[list[str]] = None,
        requires_file: Optional[Union[str, list[str]]] = None,
        requires_package: Optional[Union[str, list[str]]] = None,
        **kwargs: dict[Any, Any],
    ) -> MarkDecorator:
        """Creates a new `@RunIf` `MarkDecorator` decorator.

        :param min_gpus: Min number of GPUs required to run test.
        :param min_torch: Minimum pytorch version to run test.
        :param max_torch: Maximum pytorch version to run test.
        :param min_python: Minimum python version required to run test.
        :param requires_file: File or list of files required to run test.
        :param requires_package: Package name or list of package names required to be installed to run test.
        :param kwargs: Native `pytest.mark.skipif` keyword arguments.
        """
        conditions = []
        reasons = []

        if min_gpus:
            conditions.append(torch.cuda.device_count() < min_gpus)
            reasons.append(f"GPUs>={min_gpus}")

        if min_torch:
            torch_version = importlib.metadata.version("torch")
            conditions.append(Version(torch_version) < Version(min_torch))
            reasons.append(f"torch>={min_torch}")

        if max_torch:
            torch_version = importlib.metadata.version("torch")
            conditions.append(Version(torch_version) >= Version(max_torch))
            reasons.append(f"torch<{max_torch}")

        if min_python:
            py_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
            conditions.append(Version(py_version) < Version(min_python))
            reasons.append(f"python>={min_python}")

        if supported_arch:
            if isinstance(supported_arch, str):
                supported_arch = [supported_arch]
            gpu_arch = get_gpu_architecture()
            conditions.extend([gpu_arch not in supported_arch])
            reasons.append(f"supported_arch arch={','.join(supported_arch)}")

        if requires_file:
            if isinstance(requires_file, str):
                requires_file = [requires_file]
            conditions.extend([not Path(file).exists() for file in requires_file])
            reasons.append(f"requires file={','.join(requires_file)}")

        if requires_package:
            if isinstance(requires_package, str):
                requires_package = [requires_package]
            for package in requires_package:
                try:
                    __import__(package)
                except ImportError:
                    conditions.extend([True])
                    reasons.append(f"Package {package} is not installed.")

        reasons = [rs for cond, rs in zip(conditions, reasons) if cond]
        return pytest.mark.skipif(
            condition=any(conditions),
            reason=f"Requires: [{' + '.join(reasons)}]",
            **kwargs,
        )


def run_command(
    cmd: str, max_retry_counter: int = 3, is_raise: bool = True, capture_output: bool = True
) -> subprocess.CompletedProcess:
    """Runs a shell command with the ability to retry upon failure.

    Parameters:
    - cmd (str): The shell command to run.
    - max_retry_counter (int): Maximum number of retries if the command fails.
    - is_raise (bool): Whether to raise an exception and exit the program if the command fails after all retries.
    - capture_output (bool): Whether to capture the output of the command.

    Returns:
    - subprocess.CompletedProcess: The result of the command execution.
    """

    retry_counter = 0
    while retry_counter < max_retry_counter:
        try:
            result = subprocess.run(cmd, shell=True, capture_output=capture_output, text=True, check=False)  # noqa: S602

            # Check if the command was successful (returncode = 0)
            if result.returncode == 0:
                return result

            retry_counter += 1
            logger.debug(
                f"Retry {retry_counter}/{max_retry_counter}: Command '{cmd}' failed with error"
                f" code {result.returncode}. Error message: {result.stderr.strip()}"
            )

        except Exception as e:  # pylint: disable=broad-except
            retry_counter += 1
            logger.debug(f"Retry {retry_counter}/{max_retry_counter}: Command '{cmd}' raised an exception: {e}")

    # If reached here, all retries have failed
    error_message = (
        f"Command '{cmd}' failed after {max_retry_counter} retries. Error code: {result.returncode}. "
        f"Error message: {result.stderr.strip()}"
    )
    if is_raise:
        raise RuntimeError(error_message)

    logger.critical(error_message)
    return result
