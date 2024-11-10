# Copyright (c) 2024 Joseph Hale
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import logging

from git_authorship.cli import main


if __name__ == "__main__":
    logging.getLogger("git_authorship").addHandler(logging.StreamHandler())
    logging.getLogger("git_authorship").setLevel(logging.INFO)

    main()
