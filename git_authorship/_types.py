# Copyright (c) 2024 Joseph Hale
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from pathlib import Path
from typing import Dict


FilePath = Path
Author = str
LineCount = int
Authorship = Dict[Author, LineCount]
RepoAuthorship = Dict[FilePath, Authorship]

__all__ = ["FilePath", "Author", "LineCount", "Authorship", "RepoAuthorship"]
