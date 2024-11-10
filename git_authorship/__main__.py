# Copyright (c) 2024 Joseph Hale
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import argparse
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional
import plotly.graph_objects as go
import json

from git import Repo

EXCLUDE_DIRS = [".git"]


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("location", nargs="?", default=".")
    parser.add_argument("--clone-to", nargs="?", default="./repo/git_authorship")
    # TODO --branch (to analyze a specific branch)
    return parser.parse_args()


def ensure_cloned_and_pulled(location: str, clone_to: str):
    if not Path(clone_to).exists():
        Repo.clone_from(location, clone_to)
    else:
        Repo(clone_to).git.pull()

    return Repo(clone_to)


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


FilePath = Path
Author = str
LineCount = int
Authorship = Dict[Author, LineCount]
RepoAuthorship = Dict[FilePath, Authorship]


def file_authorship(repo: Repo, path: Path) -> Authorship:
    raw_blame = repo.blame("HEAD", str(path), rev_opts=["-M", "-C", "-C", "-C"])
    blame = [
        (f"{commit.author.name} <{commit.author.email}>", len(lines))
        for commit, lines in (raw_blame or [])
    ]

    authorship = defaultdict(int)
    for author, lines in blame:
        authorship[author] += lines

    return authorship


def repo_authorship(repo: Repo) -> RepoAuthorship:
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
    file_authorships = {path: file_authorship(repo, path) for path in filepaths}

    repo_authorship: RepoAuthorship = defaultdict(lambda: defaultdict(int))
    for file, authorship in file_authorships.items():
        parts = f"./{file}".split("/")
        for i in range(len(parts)):
            cur = "/".join(parts[: i + 1])
            for author, lines in authorship.items():
                repo_authorship[Path(cur)][author] += lines

    return repo_authorship


def export_treemap(authorship: RepoAuthorship, output: Path = Path("authorship.html")):
    ids = [str(file) for file in authorship.keys()]
    parents = [
        str(file.parent) if str(file) != "." else "" for file in authorship.keys()
    ]
    values = [sum(authors.values()) for authors in authorship.values()]
    labels = [file.name for file in authorship.keys()]
    descriptions = [
        "<br>Authors:<br> - "
        + "<br> - ".join(f"{author}: {lines}" for author, lines in authorship.items())
        for authorship in authorship.values()
    ]

    fig = go.Figure(
        go.Treemap(
            ids=ids,
            labels=labels,
            parents=parents,
            values=values,
            maxdepth=3,
            branchvalues="total",
            text=descriptions,
            hovertemplate="%{label}<br><br>%{value} lines<br>%{text}",
            root_color="lightgrey",
        )
    )

    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    fig.write_html(output)


def export_json(authorship: RepoAuthorship, output: Path = Path("authorship.json")):
    with open(output, "w") as f:
        json.dump({str(path): authors for path, authors in authorship.items()}, f)


if __name__ == "__main__":
    args = parse_args()
    repo = ensure_cloned_and_pulled(args.location, args.clone_to)
    authorship = repo_authorship(repo)
    export_treemap(authorship)
    export_json(authorship)
