SHELL = bash

install:
# Get the `hercules` binary
	@echo This script will require SUDO to succeed. Consider running its commands yourself.
	wget https://github.com/src-d/hercules/releases/download/v10.7.2/hercules.linux_amd64.gz
	gunzip hercules.linux_amd64.gz
# Get the `labours` binary
	apt install libjpeg-dev zlib1g-dev
	apt install gfortran libopenblas-dev liblapack-dev
	python -m venv .venv
	source .venv/bin/activate
	pip install labours

analyze:
# git clone https://github.com/cubing/cubing.js.git
# ./hercules --burndown --burndown-people cubing.js >> cubingjs-authors.yaml
# ./hercules --burndown --burndown-people cubing.js --people-dict=./people-license-dict >> cubingjs-authors-licenses.yaml
	./hercules --burndown --burndown-files cubing.js >> cubingjs-files.yaml

report:
	source .venv/bin/activate
	labours -m ownership -i cubingjs-authors-licenses.yaml -o cubingjs-authors-licenses.png
	labours -m ownership -i cubingjs-authors.yaml -o cubingjs-authors.png
	labours -m burndown-file -i cubingjs-files.yaml -o cubingjs-files.png