# Copyright (c) 2022 Joseph Hale
# 
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

run:
	python ./git_authorship/authorship_analyzer.py

.PHONY: test
test:
	poetry run pytest

license-check:
	poetry export --format=requirements.txt --output=requirements.txt
	poetry run liccheck
	rm requirements.txt