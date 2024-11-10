# Copyright (c) 2024 Joseph Hale
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import logging
from collections import defaultdict
from pathlib import Path

from git import Repo

from ._pathutils import iterfiles
from ._types import Authorship
from ._types import RepoAuthorship

EXCLUDE_DIRS = [".git"]

log = logging.getLogger(__name__)


def for_file(repo: Repo, path: Path) -> Authorship:
    log.info(f"Blaming {path}")
    raw_blame = repo.blame("HEAD", str(path), rev_opts=["-M", "-C", "-C", "-C"])
    blame = [
        (f"{commit.author.name} <{commit.author.email}>", len(lines))
        for commit, lines in (raw_blame or [])
    ]

    authorship: Authorship = defaultdict(int)
    for author, lines in blame:
        authorship[author] += lines

    return authorship


def for_repo(repo: Repo) -> RepoAuthorship:
    """
    Calculates how many lines each author has contributed to the repo, with breakdowns
    by folder and file.

    e.g. For a repo with the following structure:

    ```
    .
    ├── folder1
    │   ├── file1.txt  (author1: 25 lines, author2: 150 lines)
    │   └── file2.txt  (author1: 25 lines)
    ├── folder2
    │   ├── file1.txt  (author1: 25 lines, author2: 25 lines)
    │   └── file2.txt  (author1: 25 lines, author2: 25 lines)
    ```

    The result will be

    ```
    {
      ".": { "author1": 100, "author2": 200 },
      "./folder1": { "author1": 50, "author2": 150 },
      "./folder1/file1.txt": { "author1": 25, "author2": 150 },
      "./folder1/file2.txt": { "author1": 25 },
      "./folder2": { "author1": 50, "author2": 50 },
      "./folder2/file1.txt": { "author1": 25, "author2": 25 },
      "./folder2/file2.txt": { "author1": 25, "author2": 25 },
    }
    ```

    """
    root = Path(repo.working_dir)
    filepaths = [
        Path(str(f)[len(str(root)) + 1 :])
        for f in iterfiles(root, exclude=[root / d for d in EXCLUDE_DIRS])
    ]
    file_authorships = {path: for_file(repo, path) for path in filepaths}

    repo_authorship: RepoAuthorship = defaultdict(lambda: defaultdict(int))
    for file, authorship in file_authorships.items():
        parts = f"./{file}".split("/")
        for i in range(len(parts)):
            cur = "/".join(parts[: i + 1])
            for author, lines in authorship.items():
                repo_authorship[Path(cur)][author] += lines

    return repo_authorship


__all__ = ["file", "repo"]
