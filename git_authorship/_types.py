# Copyright (c) 2024 Joseph Hale
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from pathlib import Path
from typing import Dict
from typing import Iterable
from typing import TypedDict

from typing_extensions import NotRequired


FilePath = Path
Author = str
LineCount = int
License = str


class _Pseudonym(TypedDict):
    author: Author
    license: License


class Config:
    AuthorLicenses = Dict[Author, License]
    """Map of 'Author' -> 'SPDX License'"""
    Pseudonyms = Dict[Path, _Pseudonym]
    """Map of 'Path' -> 'Pseudonym'"""
    IgnoreExtensions = Iterable[str]


class AuthorshipInfo(TypedDict):
    lines: LineCount
    license: NotRequired[License]


Authorship = Dict[Author, AuthorshipInfo]
RepoAuthorship = Dict[FilePath, Authorship]

__all__ = ["FilePath", "Author", "LineCount", "Config", "Authorship", "RepoAuthorship"]
