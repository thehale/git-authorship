from pathlib import Path

from pytest import raises as assertRaises

from git_authorship.cli import parse_args


def test_default_args():
    args = parse_args([])

    assert args.location == "."
    assert args.clone_to == Path("./build/repo")
    assert args.output == Path("build")
    assert args.branch is None
    assert args.author_licenses is None
    assert args.use_cache is True


def test_location():
    args = parse_args(["https://github.com/thehale/git-authorship"])
    assert args.location == "https://github.com/thehale/git-authorship"


def test_clone_to():
    args = parse_args(["--clone-to", "/tmp/repo"])
    assert args.clone_to == Path("/tmp/repo")


def test_branch():
    args = parse_args(["--branch", "master"])
    assert args.branch == "master"


def test_author_licenses_nonexistent_path():
    with assertRaises(FileNotFoundError):
        parse_args(["--author-licenses", "nonexistent.csv"])


def test_author_licenses_rejects_folder_path():
    with assertRaises(ValueError, match="--author-licenses cannot be a folder"):
        parse_args(["--author-licenses", str(Path(__file__).parent)])


def test_author_licenses_existing_path():
    args = parse_args(["--author-licenses", "test/fixtures/licensing.csv"])
    assert args.author_licenses == Path("test/fixtures/licensing.csv")


def test_no_authorship_cache():
    args = parse_args(["--no-cache"])
    assert args.use_cache is False


def test_output_path():
    args = parse_args(["--output", "somewhere_else"])
    assert args.output == Path("somewhere_else")


def test_output_path_short_option():
    args = parse_args(["-o", "somewhere_else"])
    assert args.output == Path("somewhere_else")


def test_output_path_rejects_existing_file_path():
    with assertRaises(ValueError, match="--output cannot be an existing file"):
        parse_args(["-o", __file__])
