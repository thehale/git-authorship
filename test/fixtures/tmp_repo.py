from pathlib import Path
from typing import List
from typing import Tuple
from typing import Union

from git import Actor
from git import Repo

Message = str
AuthorName = str
AuthorEmail = str

CommitMessage = Tuple[Message, AuthorName, AuthorEmail]

FilePath = str
FileContent = Union[List[str], str]
Change = Tuple[FilePath, FileContent]


class TemporaryRepository:
    def __init__(self, directory: str):
        self._repo = Repo.init(directory)
        self._index = self._repo.index

    @property
    def dir(self):
        return self._repo.working_dir

    @property
    def branch(self) -> str:
        return self._repo.active_branch.name

    def set_file(self, path: str, content: Union[str, List[str], bytes]):
        """
        Updates a file in the repository to the given content, creating it if necessary.
        """
        if isinstance(content, bytes):
            with open(Path(self.dir) / path, "wb") as f:
                f.write(content)
        elif isinstance(content, list):
            with open(Path(self.dir) / path, "w") as f:
                f.write("\n".join(content))
        elif isinstance(content, str):
            with open(Path(self.dir) / path, "w") as f:
                f.write(content)

        self._index.add(path)

    def append_file(self, path: str, content: Union[str, List[str]]):
        if isinstance(content, list):
            content = "\n".join(content)

        with open(Path(self.dir) / path, "a") as f:
            f.write(content)

        self._index.add(path)

    def commit(self, message: str, author_name: str, author_email: str):
        author = Actor(author_name, author_email)
        commit = self._index.commit(message, author=author)
        return commit
