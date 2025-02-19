from pathlib import Path
from test.fixtures import tmp_file

from pytest import raises as assertRaises

from git_authorship.config import load_pseudonyms_config
from git_authorship.exceptions import ConfigException


def test_rejects_csv_with_too_many_columns():
    config = "RANDOM PATH,RANDOM AUTHOR,RANDOM LICENSE,EXTRA COLUMN"
    with tmp_file.with_content(config) as tf:
        with assertRaises(ConfigException):
            load_pseudonyms_config(tf.name)


def test_rejects_csv_with_too_few_columns():
    config = "RANDOM PATH"
    with tmp_file.with_content(config) as tf:
        with assertRaises(ConfigException):
            load_pseudonyms_config(tf.name)


def test_parses_csvs_with_correct_columns():
    config = "/path1,Author 1 <author1@example.com>,MIT\n/path2,Author 2,MPL-2.0"
    with tmp_file.with_content(config) as tf:
        config = load_pseudonyms_config(tf.name)
        assert config == {
            Path("/path1"): {
                "author": "Author 1 <author1@example.com>",
                "license": "MIT",
            },
            Path("/path2"): {"author": "Author 2", "license": "MPL-2.0"},
        }
