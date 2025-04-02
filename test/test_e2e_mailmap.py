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


def test_mailmap_considred_in_authorship(
    snapshot, repo: TemporaryRepository, tmpdirs: TemporaryDirectoryFactory
):
    repo.set_file("greeting.txt", "Hello, world!  \n")
    repo.commit("Initial commit", "Alice", "alice@example.com")

    repo.append_file("greeting.txt", "Hello, everyone!\n")
    repo.commit("Second commit", "Aliz", "user+1234@no-reply.github.com")

    repo.set_file(
        ".mailmap", "Alice <alice@example.com> <user+1234@no-reply.github.com>\n"
    )
    repo.commit("Add mailmap", "Susie", "Susie@example.com")

    # fmt: off
    run([
        repo.dir, 
        "--clone-to", tmpdirs.new(),
        "--output", (output := tmpdirs.new()),
    ])
    # fmt: on

    with open(f"{output}/authorship.csv", "r") as f:
        snapshot.assert_match(f.read(), "authorship.csv")
