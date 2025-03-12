import tempfile
from contextlib import contextmanager


@contextmanager
def with_content(content: str):
    with tempfile.NamedTemporaryFile("w") as tf:
        tf.write(content)
        tf.flush()
        yield tf
