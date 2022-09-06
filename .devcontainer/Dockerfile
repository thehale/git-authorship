FROM thehale/python-poetry:1.2.0-py3.8-slim
ARG PROJECT_FOLDER_NAME
ENV PROJECT_ROOT_DIR=/workspaces/$PROJECT_FOLDER_NAME

RUN apt update \
    && apt install git make --assume-yes --no-install-recommends

WORKDIR $PROJECT_ROOT_DIR
ENV PATH="$PROJECT_ROOT_DIR/.venv/bin:$PATH"
