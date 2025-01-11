from git_authorship.cli import Args
from git_authorship.cli import run


def test_full_workflow(snapshot):
    run(
        Args(
            location="https://github.com/thehale/git-authorship",
            clone_to="./build/test/e2e",
            branch="b655cc6c634a52660d3d2e87f9978343c92aa998",
            author_licenses_path=None,
            use_cache=False,
        )
    )

    with open("build/authorship.csv", "r") as f:
        snapshot.assert_match(f.read(), "authorship.csv")


def test_full_workflow_with_author_licenses(snapshot):
    run(
        Args(
            location="https://github.com/thehale/git-authorship",
            clone_to="./build/test/e2e",
            branch="b655cc6c634a52660d3d2e87f9978343c92aa998",
            author_licenses_path="./test/fixtures/licensing.csv",
            use_cache=False,
        )
    )

    with open("build/authorship.csv", "r") as f:
        snapshot.assert_match(f.read(), "authorship.csv")
