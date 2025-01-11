from tempfile import TemporaryDirectory
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


def test_typical_workflow(snapshot, repo: TemporaryRepository):
    run([repo.dir, "--clone-to", "./tmp", "--no-cache"])

    with open("build/authorship.csv", "r") as f:
        snapshot.assert_match(f.read(), "authorship.csv")


def test_workflow_with_author_licenses(snapshot, repo: TemporaryRepository):
    # fmt: off
    run([ 
        repo.dir,
        "--author-licenses", "./test/fixtures/licensing.csv",
        "--clone-to", "./tmp",
        "--no-cache",
    ])
    # fmt: on

    with open("build/authorship.csv", "r") as f:
        snapshot.assert_match(f.read(), "authorship.csv")
