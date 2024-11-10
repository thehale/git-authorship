# Copyright (c) 2024 Joseph Hale
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import json
from pathlib import Path

import plotly.graph_objects as go

from ._types import RepoAuthorship


def as_treemap(authorship: RepoAuthorship, output: Path = Path("authorship.html")):
    ids = [str(file) for file in authorship.keys()]
    parents = [
        str(file.parent) if str(file) != "." else "" for file in authorship.keys()
    ]
    values = [sum(authors.values()) for authors in authorship.values()]
    labels = [file.name for file in authorship.keys()]
    descriptions = [
        "<br>Authors:<br> - "
        + "<br> - ".join(f"{author}: {lines}" for author, lines in authorship.items())
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


def as_json(authorship: RepoAuthorship, output: Path = Path("authorship.json")):
    with open(output, "w") as f:
        json.dump({str(path): authors for path, authors in authorship.items()}, f)


__all__ = ["as_treemap", "as_json"]
