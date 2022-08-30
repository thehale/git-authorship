GIT_REPO_PATH = "./cubing.js"
EXCLUDE_DIRS = [".git"]

_CACHED_BLAME_FILE = "./blame.json"

import json
import os
from typing import Dict, List, Optional
from git import Repo


repo = Repo(GIT_REPO_PATH)


def file_blame(path: str):
    blame = repo.blame("HEAD", path, rev_opts=["-M", "-C", "-C", "-C"])
    return (
        [
            [(commit.author.name, commit.author.email), len(lines)]
            for commit, lines in blame
        ]
        if blame
        else []
    )


def folder_blame(path: str) -> Dict:
    print(f"Blaming {path}")
    root, dirs, files = next(os.walk(path))
    return {
        "files": {
            file_name: file_blame(
                os.path.join(root, file_name)[len(GIT_REPO_PATH) + 1 :]
            )
            for file_name in files
        },
        "dirs": {
            dir_name: folder_blame(os.path.join(root, dir_name))
            for dir_name in dirs
            if dir_name not in EXCLUDE_DIRS
        },
    }


def repo_blame():
    if os.path.exists(_CACHED_BLAME_FILE):
        with open(_CACHED_BLAME_FILE) as f:
            return json.load(f)
    else:
        blame = folder_blame(GIT_REPO_PATH)
        with open(_CACHED_BLAME_FILE, "w") as f:
            json.dump(blame, f)
    return blame


#####################################


class ModuleAnalyzer:
    name: str
    parent: str
    blame: List
    submodules: List["ModuleAnalyzer"]

    def __init__(
        self, name: str, parent: str, submodules: List["ModuleAnalyzer"] = None
    ):
        self.name = name
        self.parent = parent
        self.submodules = submodules or []

    def with_blame(self, blame) -> "ModuleAnalyzer":
        self.blame = blame
        return self

    def authorship(self):
        authors = {}
        for submodule in self.submodules:
            for author, lines in submodule.authorship().items():
                authors[author] = authors.get(author, 0) + lines
        return authors

    def flatten(self):
        flat = [self]
        for submodule in self.submodules:
            flat += submodule.flatten()
        return flat


class FileModuleAnalyzer(ModuleAnalyzer):
    def authorship(self):
        NAME = 0  # list idx
        authors = {}
        for author, lines in self.blame:
            authors[author[NAME]] = authors.get(author[NAME], 0) + lines
        return authors


def raw_blame_to_module_analyzer(
    module_name: str, parent_name: str, raw_blame: Dict[str, Dict]
) -> ModuleAnalyzer:
    return ModuleAnalyzer(
        module_name,
        parent_name,
        [
            *[
                FileModuleAnalyzer(
                    f"{module_name}/{file_name}", module_name
                ).with_blame(blame)
                for file_name, blame in raw_blame["files"].items()
            ],
            *[
                raw_blame_to_module_analyzer(
                    f"{module_name}/{dirname}", module_name, dirblame
                )
                for dirname, dirblame in raw_blame["dirs"].items()
            ],
        ],
    )


#####################################


blame = repo_blame()
analyzer = raw_blame_to_module_analyzer("/cubing.js", "", blame)
stats = analyzer.authorship()
print(stats)

#####################################
import plotly.graph_objects as go

modules = analyzer.flatten()
ids = [module.name for module in modules]
labels = [i.split("/")[-1] for i in ids]
parents = [module.parent for module in modules]
values = [1 for module in modules]

fig = go.Figure(
    go.Treemap(
        ids=ids,
        labels=labels,
        parents=parents,
        values=values,
        maxdepth=3,
        root_color="lightgrey",
    )
)

fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
fig.show()
