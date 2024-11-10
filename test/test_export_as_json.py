from io import StringIO
from pathlib import Path

from git_authorship import export


def test_converts_paths_to_strings():
    authorship = {Path("./path"): {"author <email>": 1}}
    output = StringIO()

    export.as_json(authorship, output=output)

    assert output.getvalue() == '{"path": {"author <email>": 1}}'


def test_writes_to_file(tmp_path):
    authorship = {Path("./path"): {"author <email>": 1}}

    export.as_json(authorship, output=tmp_path / "test.json")

    with open(tmp_path / "test.json") as f:
        assert f.read() == '{"path": {"author <email>": 1}}'
