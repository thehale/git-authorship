from pathlib import Path
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

        with open(Path(__file__).parent / "fixtures" / "image.PNG", "rb") as f:
            repo.set_file("image.PNG", f.read())
            repo.commit("Second commit", "Bob", "bob@example.com")

        with open(Path(__file__).parent / "fixtures" / "animation.gif", "rb") as f:
            repo.set_file("animation.gif", f.read())
            repo.commit("Third commit", "Susie", "Susie@example.com")

        yield repo


@pytest.fixture
def tmpdirs():
    with TemporaryDirectoryFactory() as factory:
        yield factory


def test_ignore_patterns_dont_appear_in_authorship(
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
