# Copyright (c) 2024 Joseph Hale
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Dict

import plotly.graph_objects as go

from ._pathutils import io_handle
from ._pathutils import Writeable
from ._types import Authorship
from ._types import RepoAuthorship


def as_treemap(
    authorship: RepoAuthorship, output: Writeable = Path("build/authorship.html")
):
    """
    Exports the authorship as an interactive treemap (in an HTML file)

    Args:
        authorship (RepoAuthorship): The authorship to export
        output (Union[PathLike, IO]): The output file path or handle.
            If a path, it will be open and closed. Handles are left open.
    """
    ids = [str(file) for file in authorship.keys()]
    parents = [
        str(file.parent) if str(file) != "." else "" for file in authorship.keys()
    ]
    values = [
        sum(info["lines"] for info in authors.values())
        for authors in authorship.values()
    ]
    labels = [file.name for file in authorship.keys()]

    def author_list(authorship: Authorship):
        return "<br>Authors:<br> - " + "<br> - ".join(
            f"{author}: {info['lines']}" for author, info in authorship.items()
        )

    def license_list(authorship: Authorship):
        licensing: Dict[str, int] = defaultdict(int)
        for _, info in authorship.items():
            licensing[info.get("license", "Unknown")] += info["lines"]
        return "<br>Licenses:<br> - " + "<br> - ".join(
            f"{license}: {lines}" for license, lines in licensing.items()
        )

    descriptions = [
        f"{author_list(authorship)}<br>{license_list(authorship)}"
        for authorship in authorship.values()
    ]

    fig = go.Figure(
        go.Treemap(
            ids=ids,
            labels=labels,
            parents=parents,
            values=values,
            maxdepth=3,
            branchvalues="total",
            text=descriptions,
            hovertemplate="%{label}<br><br>%{value} lines<br>%{text}",
            root_color="lightgrey",
        )
    )

    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    fig.write_html(output)


def as_json(
    authorship: RepoAuthorship, output: Writeable = Path("build/authorship.json")
):
    """
    Exports the authorship in JSON format

    Args:
        authorship (RepoAuthorship): The authorship to export
        output (Union[PathLike, IO]): The output file path or handle.
            If a path, it will be open and closed. Handles are left open.
    """
    with io_handle(output) as f:
        json.dump({str(path): authors for path, authors in authorship.items()}, f)


def as_csv(
    authorship: RepoAuthorship, output: Writeable = Path("build/authorship.csv")
):
    """
    Exports the authorship in CSV format

    Args:
        authorship (RepoAuthorship): The authorship to export
        output (Union[PathLike, IO]): The output file path or handle.
            If a path, it will be open and closed. Handles are left open.
    """
    with io_handle(output) as f:
        writer = csv.writer(f)
        writer.writerow(["path", "author", "lines", "license"])
        for path, authors in sorted(authorship.items(), key=lambda x: x[0]):
            for author, info in sorted(
                authors.items(), key=lambda x: x[1]["lines"], reverse=True
            ):
                writer.writerow([path, author, info["lines"], info.get("license")])


__all__ = ["as_treemap", "as_json", "as_csv"]
