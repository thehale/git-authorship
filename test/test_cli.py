from git_authorship.cli import parse_args


def test_default_args():
    args = parse_args([])

    assert args.location == "."
    assert args.clone_to == "./build/repo"
    assert args.branch is None


def test_location():
    args = parse_args(["https://github.com/thehale/git-authorship"])

    assert args.location == "https://github.com/thehale/git-authorship"
    assert args.clone_to == "./build/repo"
    assert args.branch is None


def test_clone_to():
    args = parse_args(["--clone-to", "/tmp/repo"])

    assert args.location == "."
    assert args.clone_to == "/tmp/repo"
    assert args.branch is None


def test_branch():
    args = parse_args(["--branch", "master"])

    assert args.location == "."
    assert args.clone_to == "./build/repo"
    assert args.branch == "master"
