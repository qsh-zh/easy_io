import numpy as np

import easy_io
from easy_io.test_utils import RunIf

S3_CREDENTIAL_PATH = "credentials/abc.secret"
# from pathlib import Path
# S3_CREDENTIAL_PATH = str(Path("~/dpdata/dir_data/s3/s3_training.secret").expanduser().resolve())


def setup_s3():
    easy_io.set_s3_backend(
        backend_args={
            "backend": "s3",
            "path_mapping": None,
            "s3_credential_path": S3_CREDENTIAL_PATH,
        }
    )


@RunIf(requires_file=S3_CREDENTIAL_PATH)
def test_s3_backend():
    setup_s3()
    for ith, _ in enumerate(easy_io.list_dir_or_file("s3://checkpoints-us-east-1/")):
        if ith > 5:
            break

    easy_io.copyfile_from_local("pyproject.toml", "s3://checkpoints-us-east-1/pyproject.toml")
    easy_io.remove("s3://checkpoints-us-east-1/pyproject.toml")


@RunIf(requires_file=S3_CREDENTIAL_PATH)
def test_s3_dump():
    setup_s3()
    if easy_io.exists("s3://checkpoints-us-east-1/dummy_dict.pkl"):
        easy_io.remove("s3://checkpoints-us-east-1/dummy_dict.pkl")

    dummy_dict = {"a": 1, "b": 2}
    easy_io.dump(dummy_dict, "s3://checkpoints-us-east-1/dummy_dict.pkl")
    dummy_np = np.array([1, 2, 3])
    easy_io.dump(dummy_np, "s3://checkpoints-us-east-1/dummy_np.npy")

    easy_io.remove("s3://checkpoints-us-east-1/dummy_dict.pkl")
    easy_io.remove("s3://checkpoints-us-east-1/dummy_np.npy")

    # write a large file
    dummy_large_file = np.random.rand(10000000).tobytes()
    easy_io.dump(dummy_large_file, "s3://checkpoints-us-east-1/dummy_large_file.bin")
    load_dummy_large_file = easy_io.load("s3://checkpoints-us-east-1/dummy_large_file.bin")
    assert dummy_large_file == load_dummy_large_file

    # write a large file with fast backend
    easy_io.dump(dummy_large_file, "s3://checkpoints-us-east-1/dummy_large_file.bin", fast_backend=True)
    load_dummy_large_file = easy_io.load("s3://checkpoints-us-east-1/dummy_large_file.bin", fast_backend=True)
    assert dummy_large_file == load_dummy_large_file
    easy_io.remove("s3://checkpoints-us-east-1/dummy_large_file.bin")


def test_local_backend():
    num_files = len(list(easy_io.list_dir_or_file(".")))
    assert num_files > 0

    if easy_io.exists("dummy_dict.pkl"):
        easy_io.remove("dummy_dict.pkl")

    dummy_dict = {"a": 1, "b": 2}
    easy_io.dump(dummy_dict, "dummy_dict.pkl")
    load_dict = easy_io.load("dummy_dict.pkl")
    for key in dummy_dict:
        assert dummy_dict[key] == load_dict[key]

    if easy_io.exists("dummy_dict.pkl"):
        easy_io.remove("dummy_dict.pkl")
