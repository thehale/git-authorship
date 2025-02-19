import csv
from pathlib import Path
from typing import Iterable
from typing import Optional
from typing import Tuple

from ._types import Author
from ._types import Config
from ._types import License
from git_authorship.exceptions import AuthorLicensesConfigException
from git_authorship.exceptions import PseudonymsConfigException


def _licenses_reader(path: Path) -> Iterable[Tuple[Author, License]]:
    with open(path, "r") as f:
        reader = csv.reader(f)
        for idx, row in enumerate(reader):
            if (count := len(row)) != 2:
                raise AuthorLicensesConfigException(
                    f"Two (2) columns expected, but {path} @ line {idx} has {count} column(s)"
                )
            yield row[0], row[1]


def load_licenses_config(path: Optional[Path] = None) -> Config.AuthorLicenses:
    if path:
        return {author: license for author, license in _licenses_reader(path)}
    else:
        return {}


def _pseudonyms_reader(path: Path) -> Iterable[Tuple[Path, Author, License]]:
    with open(path, "r") as f:
        reader = csv.reader(f)
        for idx, row in enumerate(reader):
            if (count := len(row)) != 3:
                raise PseudonymsConfigException(
                    f"Three (3) columns expected, but {path} @ line {idx} has {count} column(s)"
                )
            yield Path(row[0]), row[1], row[2]


def load_pseudonyms_config(path: Optional[Path] = None) -> Config.Pseudonyms:
    if path:
        return {
            path: {"author": author, "license": license}
            for path, author, license in _pseudonyms_reader(path)
        }
    else:
        return {}


__all__ = ["load_licenses_config", "load_pseudonyms_config"]
