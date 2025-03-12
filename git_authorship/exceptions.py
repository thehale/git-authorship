class GitAuthorshipException(Exception):
    """Top-level exception for Git Authorship"""


class ConfigException(GitAuthorshipException):
    """Thrown for malformed configs"""


class AuthorLicensesConfigException(ConfigException):
    """Thrown for malformed author licenses configs"""
