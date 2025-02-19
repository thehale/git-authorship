# Copyright (c) 2024 Joseph Hale
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import argparse
import logging
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from typing import Optional
from typing import Union

from git import Repo

from git_authorship import authorship
from git_authorship import export
from git_authorship.config import load_licenses_config
from git_authorship.config import load_pseudonyms_config

log = logging.getLogger(__name__)


@dataclass
class Args:
    location: str
    clone_to: Path
    output: Path
    branch: str
    author_licenses: Optional[Path]
    pseudonyms: Optional[Path]
    use_cache: bool = True


def parse_args(argv=None) -> Args:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "location", nargs="?", default=".", help="The URL/path to repo to analyze"
    )
    parser.add_argument(
        "-o",
        "--output",
        nargs="?",
        default="./build",
        help="The directory to output the reports",
    )
    parser.add_argument(
        "--clone-to", nargs="?", default="./build/repo", help="The path to clone to"
    )
    parser.add_argument(
        "--branch", nargs="?", default=None, help="The branch/revision to checkout"
    )
    parser.add_argument(
        "--author-licenses",
        nargs="?",
        default=None,
        help="The path to a CSV file containing author licenses",
    )
    parser.add_argument(
        "--pseudonyms",
        nargs="?",
        default=None,
        help="The path to a CSV file containing pseudonyms",
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Recompute from scratch, including a re-clone.",
    )

    args = parser.parse_args(argv)

    return _assert_valid_args(
        Args(
            args.location,
            Path(args.clone_to),
            Path(args.output),
            args.branch,
            _parse_file_path(args.author_licenses, "--author-licenses"),
            _parse_file_path(args.pseudonyms, "--pseudonyms"),
            not args.no_cache,
        )
    )


def _assert_valid_args(args: Args):
    if args.output.exists() and args.output.is_file():
        raise ValueError(f"--output cannot be an existing file. Given: {args.output}")
    return args


def _parse_file_path(arg: Optional[str] = None, optname: str = "") -> Optional[Path]:
    if not arg:
        return None
    else:
        if not Path(arg).exists():
            raise FileNotFoundError(arg)
        elif Path(arg).is_dir():
            raise ValueError(f"{optname} cannot be a folder. Given: {arg}")
        else:
            return Path(arg)


def clone_and_checkout(args: Args):
    log.info(
        f"Cloning {args.location} @ {args.branch or '<default>'} to {args.clone_to}"
    )

    if not args.use_cache:
        shutil.rmtree(args.clone_to, ignore_errors=True)

    if not args.clone_to.exists() or not (args.clone_to / ".git").exists():
        Repo.clone_from(args.location, args.clone_to)

    repo = Repo(args.clone_to)

    if args.branch:
        repo.git.checkout(args.branch)

    return repo


def run(args: Union[Args, Iterable[str]]):
    if isinstance(args, Iterable):
        args = parse_args(args)

    repo = clone_and_checkout(args)
    licenses = load_licenses_config(args.author_licenses)
    pseudonyms = load_pseudonyms_config(args.pseudonyms)
    repo_authorship = authorship.for_repo(
        repo,
        licenses=licenses,
        pseudonyms=pseudonyms,
        cache_dir=args.output / "cache",
        use_cache=args.use_cache,
    )
    export.as_treemap(repo_authorship, output=args.output / "authorship.html")
    export.as_json(repo_authorship, output=args.output / "authorship.json")
    export.as_csv(repo_authorship, output=args.output / "authorship.csv")


def main(argv=None):
    logging.getLogger("git_authorship").addHandler(logging.StreamHandler())
    logging.getLogger("git_authorship").setLevel(logging.INFO)

    run(parse_args(argv))
