from tempfile import TemporaryDirectory
from typing import List


class TemporaryDirectoryFactory:
    """
    A factory for creating temporary directories. Can be used as a context manager.

    Usage:

    ```python
    with TemporaryDirectoryFactory() as factory:
        dir1 = factory.new()
        dir2 = factory.new()

        # ...
    ```

    Upon leaving the context, all directories created with `new` and their contents are
    removed.
    """

    def __init__(self):
        self.tmpdirs: List[TemporaryDirectory] = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        for tmpdir in self.tmpdirs:
            tmpdir.cleanup()

    def new(self):
        tmpdir = TemporaryDirectory()
        self.tmpdirs.append(tmpdir)
        return tmpdir.name


__all__ = ["TemporaryDirectoryFactory"]
