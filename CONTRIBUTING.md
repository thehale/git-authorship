# Contributing

## Setup

1. Clone this repository: `git clone https://github.com/thehale/git-authorship`
2. Install [Python Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer)
    
    ```
    curl -sSL https://install.python-poetry.org | python3 -
    ```

3. Create a virtual environment and install dependencies
     
     ```
     poetry config virtualenvs.in-project true
     poetry shell
     poetry install
     ```
     
4. Run the test suite with `pytest` to verify that everything works.
5. Have fun with your improvements!


## Preferences

Please use the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) style for your commit messages.


## Publishing Updates

```bash
poetry config pypi-token.pypi your-api-token
poetry publish --build
```