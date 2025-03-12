from test.fixtures import tmp_file

from pytest import raises as assertRaises

from git_authorship.config import load_licenses_config
from git_authorship.exceptions import ConfigException


def test_rejects_csv_with_too_many_columns():
    config = "RANDOM AUTHOR,RANDOM LICENSE,EXTRA COLUMN"
    with tmp_file.with_content(config) as tf:
        with assertRaises(ConfigException):
            load_licenses_config(tf.name)


def test_rejects_csv_with_too_few_columns():
    config = "RANDOM AUTHOR"
    with tmp_file.with_content(config) as tf:
        with assertRaises(ConfigException):
            load_licenses_config(tf.name)


def test_parses_csvs_with_correct_columns():
    config = "Author 1,MIT\nAuthor 2,MPL-2.0"
    with tmp_file.with_content(config) as tf:
        config = load_licenses_config(tf.name)
        assert config == {
            "Author 1": "MIT",
            "Author 2": "MPL-2.0",
        }
