from pathlib import Path

from pytest import raises as assertRaises

from git_authorship.cli import parse_args


def test_default_args():
    args = parse_args([])

    assert args.location == "."
    assert args.clone_to == "./build/repo"
    assert args.branch is None
    assert args.author_licenses_path is None
    assert args.use_authorship_cache is True


def test_location():
    args = parse_args(["https://github.com/thehale/git-authorship"])
    assert args.location == "https://github.com/thehale/git-authorship"


def test_clone_to():
    args = parse_args(["--clone-to", "/tmp/repo"])
    assert args.clone_to == "/tmp/repo"


def test_branch():
    args = parse_args(["--branch", "master"])
    assert args.branch == "master"


def test_author_licenses_nonexistent_path():
    with assertRaises(FileNotFoundError):
        parse_args(["--author-licenses", "nonexistent.csv"])


def test_author_licenses_existing_path():
    args = parse_args(["--author-licenses", "test/fixtures/licensing.csv"])
    assert args.author_licenses_path == Path("test/fixtures/licensing.csv")


def test_no_authorship_cache():
    args = parse_args(["--no-authorship-cache"])

    assert args.use_authorship_cache is False
