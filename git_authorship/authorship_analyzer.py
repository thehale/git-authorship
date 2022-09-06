# Copyright (c) 2022 Joseph Hale
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import json
import os
from typing import Dict
from typing import List
from typing import Optional

from git import Repo

# Global Configuration
GIT_REPO_BASE_PATH = "./repo"
AUTHOR_LICENSE_FILE = "./config/author-licenses.txt"
PSEUDONYMS_FILE = "./config/pseudonyms.txt"
EXCLUDE_DIRS = [".git"]


def _load_pseudonyms(path: str):
    cache = {}
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                module, author, email, license = line.strip().split("|")
                cache[module] = {
                    "author": author,
                    "email": email,
                    "license": license,
                }
    return cache


def _load_author_licenses(path: str):
    cache = {}
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                author, license = line.strip().split("|")
                cache[author] = license
    return cache


def _get_git_repo_path(base_path: str):
    _root, dirs, _files = next(os.walk(base_path))
    return os.path.join(base_path, dirs[0])


# Internal Configuration
_GIT_REPO_PATH = _get_git_repo_path(GIT_REPO_BASE_PATH)
_BUILT_BLAME_FILE = "./build/blame.json"
_BUILT_HTML_FILE = "./build/authorship.html"
_PSEUDONYMS_CACHE = _load_pseudonyms(PSEUDONYMS_FILE)
_AUTHOR_LICENSE_CACHE = _load_author_licenses(AUTHOR_LICENSE_FILE)


repo = Repo(_GIT_REPO_PATH)


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
                os.path.join(root, file_name)[len(_GIT_REPO_PATH) + 1 :]
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
    if os.path.exists(_BUILT_BLAME_FILE):
        with open(_BUILT_BLAME_FILE) as f:
            return json.load(f)
    else:
        blame = folder_blame(_GIT_REPO_PATH)
        with open(_BUILT_BLAME_FILE, "w") as f:
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

    def licensing(self):
        licenses = {}
        for submodule in self.submodules:
            for license, lines in submodule.licensing().items():
                licenses[license] = licenses.get(license, 0) + lines
        return licenses

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
            name = self.__author_override() or author[NAME]
            authors[name] = authors.get(name, 0) + lines
        return authors

    def __author_override(self) -> Optional[str]:
        for override_path, override in _PSEUDONYMS_CACHE.items():
            if override_path in self.name:
                return override["author"]
        return None

    def licensing(self):
        NAME = 0  # list idx
        licenses = {}
        for author, lines in self.blame:
            license = self.__license_override() or _AUTHOR_LICENSE_CACHE.get(
                author[NAME], "???"
            )
            licenses[license] = licenses.get(license, 0) + lines
        return licenses

    def __license_override(self) -> Optional[str]:
        # Note, uses the first matching entry.
        # Consider using the longest matching entry instead.
        for override_path, override in _PSEUDONYMS_CACHE.items():
            if override_path in self.name:
                return override["license"]
        return None


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
analyzer = raw_blame_to_module_analyzer(_GIT_REPO_PATH, "", blame)
stats = analyzer.authorship()
print(stats)


#####################################


import plotly.graph_objects as go

modules = analyzer.flatten()
ids = [module.name for module in modules]
labels = [i.split("/")[-1] for i in ids]
parents = [module.parent for module in modules]
values = [sum(module.authorship().values()) for module in modules]


def authorship_str(module: ModuleAnalyzer) -> str:
    authors = module.authorship()
    return "<br>Authors:<br> - " + "<br> - ".join(
        f"{author}: {lines}" for author, lines in authors.items()
    )


def licensing_str(module: ModuleAnalyzer) -> str:
    licenses = module.licensing()
    return "<br>Licenses:<br> - " + "<br> - ".join(
        f"{license}: {lines}" for license, lines in licenses.items()
    )


def info_str(module: ModuleAnalyzer) -> str:
    return f"{authorship_str(module)}<br>{licensing_str(module)}"


fig = go.Figure(
    go.Treemap(
        ids=ids,
        labels=labels,
        parents=parents,
        values=values,
        maxdepth=3,
        branchvalues="total",
        text=[info_str(module) for module in modules],
        hovertemplate="%{label}<br><br>%{value} lines<br>%{text}",
        root_color="lightgrey",
    )
)

fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
fig.write_html(_BUILT_HTML_FILE)
