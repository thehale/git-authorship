GIT_REPO_PATH = "./cubing.js"
EXCLUDE_DIRS = [".git"]

_CACHED_BLAME_FILE = "./blame.json"

import json
import os
from typing import Dict
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
    blame: Dict[str, "ModuleAnalyzer"]

    def __init__(self, blame: Dict[str, "ModuleAnalyzer"]):
        self.blame = blame

    def authorship(self):
        authors = {}
        for submodule in self.blame.keys():
            for author, lines in self.blame[submodule].authorship().items():
                authors[author] = authors.get(author, 0) + lines
        return authors


class FileModuleAnalyzer(ModuleAnalyzer):
    def authorship(self):
        NAME = 0  # list idx
        authors = {}
        for author, lines in self.blame:
            authors[author[NAME]] = authors.get(author[NAME], 0) + lines
        return authors


def raw_blame_to_module_analyzer(raw_blame: Dict[str, Dict]) -> ModuleAnalyzer:
    return ModuleAnalyzer(
        {
            **{
                submodule: FileModuleAnalyzer(blame)
                for submodule, blame in raw_blame["files"].items()
            },
            **{
                submodule: raw_blame_to_module_analyzer(blame)
                for submodule, blame in raw_blame["dirs"].items()
            },
        }
    )


def author_stats(blame):
    return raw_blame_to_module_analyzer(blame).authorship()


#####################################

blame = repo_blame()
analyzer = raw_blame_to_module_analyzer(blame)
stats = analyzer.authorship()
print(stats)

