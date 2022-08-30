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


def author_stats(blame):
    NAME = 0  # list idx
    authors = {}
    for file_entry in blame["files"].values():
        for author, lines in file_entry:
            authors[author[NAME]] = authors.get(author[NAME], 0) + lines
    for folder in blame["dirs"].keys():
        for author, lines in author_stats(blame["dirs"][folder]).items():
            authors[author] = authors.get(author, 0) + lines
    return authors


blame = repo_blame()
stats = author_stats(blame)
print(stats)
