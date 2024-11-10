# Copyright (c) 2024 Joseph Hale
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from pathlib import Path
from typing import List

from git import Optional


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


__all__ = ["iterfiles", "iterdirs"]
