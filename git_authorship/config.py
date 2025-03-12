import csv
from pathlib import Path
from typing import Iterable
from typing import Optional
from typing import Tuple

from ._types import Author
from ._types import Config
from ._types import License


def _licenses_reader(path: Path) -> Iterable[Tuple[Author, License]]:
    with open(path, "r") as f:
        reader = csv.reader(f)
        for idx, row in enumerate(reader):
            yield row[0], row[1]


def load_licenses_config(path: Optional[Path] = None) -> Config.AuthorLicenses:
    if path:
        return {row[0]: row[1] for row in _licenses_reader(path)}
    else:
        return {}
