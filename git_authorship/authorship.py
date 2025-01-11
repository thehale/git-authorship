# Copyright (c) 2024 Joseph Hale
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import csv
import json
import logging
from collections import defaultdict
from pathlib import Path
from typing import Optional

from git import Repo

from ._pathutils import iterfiles
from ._types import Authorship
from ._types import AuthorshipInfo
from ._types import RepoAuthorship
from git_authorship import export

EXCLUDE_DIRS = [".git"]

log = logging.getLogger(__name__)


def for_repo(
    repo: Repo,
    *,
    license_file: Optional[Path] = None,
    cache_dir: Path = Path("build/cache"),
    use_cache: bool = True,
) -> RepoAuthorship:
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
      ".": { "author1": {"lines": 100}, "author2": {"lines": 200} },
      "./folder1": { "author1": {"lines": 50}, "author2": {"lines": 150} },
      "./folder1/file1.txt": { "author1": {"lines": 25}, "author2": {"lines": 150} },
      "./folder1/file2.txt": { "author1": {"lines": 25} },
      "./folder2": { "author1": {"lines": 50}, "author2": {"lines": 50} },
      "./folder2/file1.txt": { "author1": {"lines": 25}, "author2": {"lines": 25} },
      "./folder2/file2.txt": { "author1": {"lines": 25}, "author2": {"lines": 25} },
    }
    ```

    """
    cache_key = cache_dir / f"{repo.head.commit.hexsha}.json"

    if use_cache and cache_key.exists():
        with open(cache_key, "r") as f:
            return {Path(k): v for k, v in (json.load(f) or {}).items()}
    else:
        data = _compute_repo_authorship(repo)
        data = _augment_author_licenses(data, license_file)
        cache_key.parent.mkdir(exist_ok=True, parents=True)
        export.as_json(data, cache_key)
        return data


def for_file(repo: Repo, path: Path) -> Authorship:
    """
    Calculates how many lines each author has contributed to a file

    e.g. For a file with the following contents:

    ```
    line 1  (author 1)
    line 2  (author 2)
    line 3  (author 1)
    line 4  (author 2)
    line 5  (author 1)
    ```

    The returned authorship would be:
    ```
    {
      "author1": {"lines": 3},
      "author2": {"lines": 2},
    }
    ```
    """
    log.info(f"Blaming {path}")
    try:
        raw_blame = repo.blame("HEAD", str(path), rev_opts=["-M", "-C", "-C", "-C"])
        blame = [
            (f"{commit.author.name} <{commit.author.email}>", len(lines))
            for commit, lines in (raw_blame or [])
        ]

        authorship: Authorship = defaultdict(_AuthorshipInfo)
        for author, lines in blame:
            authorship[author]["lines"] += lines
    except FileNotFoundError as e:
        log.warning(f"Failed to blame {path}: {e}")
        authorship = {}

    return authorship


def _compute_repo_authorship(repo: Repo) -> RepoAuthorship:
    root = Path(repo.working_dir)
    filepaths = [
        Path(str(f)[len(str(root)) + 1 :])
        for f in iterfiles(root, exclude=[root / d for d in EXCLUDE_DIRS])
    ]
    file_authorships = {path: for_file(repo, path) for path in filepaths}

    repo_authorship: RepoAuthorship = defaultdict(lambda: defaultdict(_AuthorshipInfo))
    for file, authorship in file_authorships.items():
        parts = f"./{file}".split("/")
        for i in range(len(parts)):
            cur = "/".join(parts[: i + 1])
            for author, info in authorship.items():
                repo_authorship[Path(cur)][author]["lines"] += info["lines"]

    return repo_authorship


def _augment_author_licenses(
    repo_authorship: RepoAuthorship, licenses_path: Optional[Path] = None
) -> RepoAuthorship:
    if licenses_path:
        with open(licenses_path, "r") as f:
            reader = csv.reader(f)
            licenses = {row[0]: row[1] for row in reader}

        for path, authorship in repo_authorship.items():
            for author in authorship.keys():
                if author in licenses:
                    repo_authorship[path][author]["license"] = licenses[author]

    return repo_authorship


def _AuthorshipInfo() -> AuthorshipInfo:
    return {"lines": 0}


__all__ = ["file", "repo"]
