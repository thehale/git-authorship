<!--
 Copyright (c) 2022 Joseph Hale
 
 This Source Code Form is subject to the terms of the Mozilla Public
 License, v. 2.0. If a copy of the MPL was not distributed with this
 file, You can obtain one at http://mozilla.org/MPL/2.0/.
-->

<div align="center">

# Git-Authorship

Interactive reports showing who wrote each line of code in your git repository.

<!-- BADGES -->
[![](https://badgen.net/github/license/thehale/git-authorship)](https://github.com/thehale/git-authorship/blob/master/LICENSE)
[![](https://badgen.net/badge/icon/Sponsor/pink?icon=github&label)](https://github.com/sponsors/thehale)
[![Joseph Hale's software engineering blog](https://jhale.dev/badges/website.svg)](https://jhale.dev)
[![](https://jhale.dev/badges/follow.svg)](https://www.linkedin.com/comm/mynetwork/discovery-see-all?usecase=PEOPLE_FOLLOWS&followMember=thehale)

![GIF demonstrating an interactive report of the authors of the cubing library
cubing.js](./docs/git-authorship-demo-cubingjs.gif)

</div>

## Why?

Copyright is a thing, and whoever wrote the code in your repository holds an
exclusive copyright over it unless an agreement has been made otherwise. 

While `git-authorship` does not help with managing copyright agreements from
contributors (see
[cla-assistant](https://github.com/cla-assistant/cla-assistant) and its
corresponding [GitHub
Action](https://github.com/contributor-assistant/github-action) for that
functionality), it does help you clearly identify who your contributors are and
the exact lines of code they wrote.

To support libraries undergoing re-licensing, `git-authorship` includes config
files for labelling the licenses under which contributors have shared their code.

## Quickstart

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
     
4. Clone the repository you wish to analyze into the included `repo` folder.
5. Make copies of the files in the `config` folder without the `dist` extension.
6. Run the analyzer with `make run`
    - The first run will take a while as it computes an accurate `git blame` for
      every file in your repository. At the end of the run, a cached blame file
      will be generated in the `build` directory to speed up future runs.

## Other Features

### Author Licenses
If you want to include information about the OSS license offered by each
contributor, simply add a line for each author to `config/author-licenses.txt`
in the following format:

```
author-name|license-SPDX-id
```

The `author-name` will be matched to the values shown in the generated
authorship report.

_A list of SPDX license identifiers can be found here:
https://spdx.org/licenses/_


### Pseudonyms
If certain files are being attributed to an unexpected author (e.g. if a
contributor copied code from another project, the `blame` would show the
contributor instead of the original author), you can manually override the
`blame` and licensing information using the `config/pseudonyms.txt` file. Use
one line per override in the following format:

```
target-path|actual-author|actual-email|license-SPDX-id
```

All files with a file path containing `target-path` as a substring will be
attributed to the named `actual-author` under the named software license.

_A list of SPDX license identifiers can be found here:
https://spdx.org/licenses/_

## License
Copyright (c) 2022 Joseph Hale, All Rights Reserved

Provided under the terms of the [Mozilla Public License, version 2.0](./LICENSE)

<details>

<summary><b>What does the MPL-2.0 license allow/require?</b></summary>

### TL;DR

You can use files from this project in both open source and proprietary
applications, provided you include the above attribution. However, if
you modify any code in this project, or copy blocks of it into your own
code, you must publicly share the resulting files (note, not your whole
program) under the MPL-2.0. The best way to do this is via a Pull
Request back into this project.

If you have any other questions, you may also find Mozilla's [official
FAQ](https://www.mozilla.org/en-US/MPL/2.0/FAQ/) for the MPL-2.0 license
insightful.

If you dislike this license, you can contact me about negotiating a paid
contract with different terms.

**Disclaimer:** This TL;DR is just a summary. All legal questions
regarding usage of this project must be handled according to the
official terms specified in the `LICENSE` file.

### Why the MPL-2.0 license?

I believe that an open-source software license should ensure that code
can be used everywhere.

Strict copyleft licenses, like the GPL family of licenses, fail to
fulfill that vision because they only permit code to be used in other
GPL-licensed projects. Permissive licenses, like the MIT and Apache
licenses, allow code to be used everywhere but fail to prevent
proprietary or GPL-licensed projects from limiting access to any
improvements they make.

In contrast, the MPL-2.0 license allows code to be used in any software
project, while ensuring that any improvements remain available for
everyone.

</details>
