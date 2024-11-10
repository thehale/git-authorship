# Copyright (c) 2024 Joseph Hale
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import argparse
from pathlib import Path

from git import Repo

from git_authorship import authorship
from git_authorship import export


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "location", nargs="?", default=".", help="The URL/path to repo to analyze"
    )
    parser.add_argument(
        "--clone-to", nargs="?", default="./repo", help="The path to clone to"
    )
    parser.add_argument(
        "--branch", nargs="?", default=None, help="The branch/revision to checkout"
    )
    return parser.parse_args()


def ensure_cloned_and_pulled(location: str, clone_to: str):
    if not Path(clone_to).exists():
        Repo.clone_from(location, clone_to)
    else:
        Repo(clone_to).git.pull()

    return Repo(clone_to)


if __name__ == "__main__":
    args = parse_args()
    repo = ensure_cloned_and_pulled(args.location, args.clone_to)
    if args.branch:
        repo.git.checkout(args.branch)
    repo_authorship = authorship.for_repo(repo)
    export.as_treemap(repo_authorship)
    export.as_json(repo_authorship)
