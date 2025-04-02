from tempfile import TemporaryDirectory
from test.fixtures.tmp_dir_factory import TemporaryDirectoryFactory
from test.fixtures.tmp_repo import TemporaryRepository

import pytest

from git_authorship.cli import run


@pytest.fixture
def repo():
    with TemporaryDirectory() as d:
        repo = TemporaryRepository(d)
        yield repo


@pytest.fixture
def tmpdirs():
    with TemporaryDirectoryFactory() as factory:
        yield factory


def test_ignored_revs_dont_appear_in_authorship(
    snapshot, repo: TemporaryRepository, tmpdirs: TemporaryDirectoryFactory
):

    repo.set_file("greeting.txt", "Hello, world!  \n")
    repo.commit("Initial commit", "Alice", "alice@example.com")

    repo.set_file("greeting.txt", "Hello, world!\n")
    commit = repo.commit("Lint: Remove trailing space", "Bob", "bob@example.com")

    repo.set_file(".git-blame-ignore-revs", f"{commit.hexsha}\n")
    repo.commit("Ignore commit", "Susie", "Susie@example.com")

    # fmt: off
    run([
        repo.dir, 
        "--clone-to", tmpdirs.new(),
        "--output", (output := tmpdirs.new()),
    ])
    # fmt: on

    with open(f"{output}/authorship.csv", "r") as f:
        snapshot.assert_match(f.read(), "authorship.csv")


def test_custom_ignored_revs_file_dont_appear_in_authorship(
    snapshot, repo: TemporaryRepository, tmpdirs: TemporaryDirectoryFactory
):

    repo.set_file("greeting.txt", "Hello, world!  \n")
    repo.commit("Initial commit", "Alice", "alice@example.com")

    repo.set_file("greeting.txt", "Hello, world!\n")
    commit = repo.commit("Lint: Remove trailing space", "Bob", "bob@example.com")

    repo.set_file(".abnormal-ignore-revs", f"{commit.hexsha}\n")
    repo.commit("Ignore commit", "Susie", "Susie@example.com")

    # fmt: off
    run([
        repo.dir, 
        "--clone-to", tmpdirs.new(),
        "--output", (output := tmpdirs.new()),
        "--ignore-revs-file", ".abnormal-ignore-revs",
    ])
    # fmt: on

    with open(f"{output}/authorship.csv", "r") as f:
        snapshot.assert_match(f.read(), "authorship.csv")
