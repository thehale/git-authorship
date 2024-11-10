# Copyright (c) 2024 Joseph Hale
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from contextlib import contextmanager
from os import PathLike
from pathlib import Path
from typing import IO
from typing import List
from typing import Union

from git import Optional

Writeable = Union[PathLike, str, IO]


@contextmanager
def io_handle(path: Writeable):
    if isinstance(path, PathLike) or isinstance(path, str):
        with open(path, "w") as io_handle:
            yield io_handle
    else:
        yield path


def iterfiles(dir: Path, exclude: Optional[List[Path]] = None):
    exclude = exclude or []
    for path in dir.iterdir():
        if path.is_file():
            yield path
        elif path.is_dir() and path not in exclude:
            yield from iterfiles(path)


def iterdirs(dir: Path, exclude: Optional[List[Path]] = None):
    exclude = exclude or []
    for path in dir.iterdir():
        if path.is_file():
            continue
        elif path.is_dir() and path not in exclude:
            yield path
            yield from iterdirs(path)


__all__ = ["Writeable", "io_handle", "iterfiles", "iterdirs"]
