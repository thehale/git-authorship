import argparse
import logging
from dataclasses import dataclass
from pathlib import Path

from git import Repo

from git_authorship import authorship
from git_authorship import export

log = logging.getLogger(__name__)


@dataclass
class Args:
    location: str
    clone_to: str
    branch: str


def parse_args(argv=None) -> Args:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "location", nargs="?", default=".", help="The URL/path to repo to analyze"
    )
    parser.add_argument(
        "--clone-to", nargs="?", default="./build/repo", help="The path to clone to"
    )
    parser.add_argument(
        "--branch", nargs="?", default=None, help="The branch/revision to checkout"
    )

    args = parser.parse_args(argv)
    return Args(args.location, args.clone_to, args.branch)


def clone_and_checkout(args: Args):
    log.info(f"Cloning {args.location} @ {args.branch} to {args.clone_to}")

    if not Path(args.clone_to).exists():
        Repo.clone_from(args.location, args.clone_to)

    repo = Repo(args.clone_to)

    if args.branch:
        repo.git.checkout(args.branch)

    return repo


def run(args: Args):
    repo = clone_and_checkout(args)
    repo_authorship = authorship.for_repo(repo)
    export.as_treemap(repo_authorship)
    export.as_json(repo_authorship)
    export.as_csv(repo_authorship)


def main(argv=None):
    run(parse_args(argv))
