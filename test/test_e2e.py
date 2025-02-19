from tempfile import TemporaryDirectory
from test.fixtures.tmp_dir_factory import TemporaryDirectoryFactory
from test.fixtures.tmp_repo import TemporaryRepository

import pytest

from git_authorship.cli import run


@pytest.fixture
def repo():
    with TemporaryDirectory() as d:
        repo = TemporaryRepository(d)

        repo.set_file("greeting.txt", "Hello, world!\n")
        repo.commit("Initial commit", "Alice", "alice@example.com")

        repo.append_file("greeting.txt", "Excited to be here!\n")
        repo.commit("Second commit", "Bob", "bob@example.com")

        yield repo


@pytest.fixture
def tmpdirs():
    with TemporaryDirectoryFactory() as factory:
        yield factory


def test_typical_workflow(
    snapshot, repo: TemporaryRepository, tmpdirs: TemporaryDirectoryFactory
):
    # fmt: off
    run([
        repo.dir, 
        "--clone-to", tmpdirs.new(),
        "--output", (output := tmpdirs.new())
    ])
    # fmt: on

    with open(f"{output}/authorship.csv", "r") as f:
        snapshot.assert_match(f.read(), "authorship.csv")


def test_workflow_with_author_licenses(
    snapshot, repo: TemporaryRepository, tmpdirs: TemporaryDirectoryFactory
):
    # fmt: off
    run([ 
        repo.dir,
        "--clone-to", tmpdirs.new(),
        "--author-licenses", "./test/fixtures/licensing.csv",
        "--output", (output := tmpdirs.new()),
    ])
    # fmt: on

    with open(f"{output}/authorship.csv", "r") as f:
        snapshot.assert_match(f.read(), "authorship.csv")


def test_workflow_with_pseudonyms(
    snapshot, repo: TemporaryRepository, tmpdirs: TemporaryDirectoryFactory
):
    # fmt: off
    run([ 
        repo.dir,
        "--clone-to", tmpdirs.new(),
        "--pseudonyms", "./test/fixtures/pseudonyms.csv",
        "--output", (output := tmpdirs.new()),
    ])
    # fmt: on

    with open(f"{output}/authorship.csv", "r") as f:
        snapshot.assert_match(f.read(), "authorship.csv")
