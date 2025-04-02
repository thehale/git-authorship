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
</div>

```bash
pip install git-authorship

git-authorship https://github.com/USERNAME/REPOSITORY

# Open build/authorship.html in a web browser
```
<div align="center">

![GIF demonstrating an interactive report of the authors of the cubing library
cubing.js](https://github.com/thehale/git-authorship/blob/master/docs/git-authorship-demo-cubingjs.gif?raw=true)

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

## Other Features

### Mailmaps

When an author changes his/her commit name or email, that author will appear
multiple times in the authorship report.

To reduce that noise, add [a standard `.mailmap`
file](https://git-scm.com/docs/git-blame/2.15.4#_mapping_authors) to the root of
your git repository.

_.mailmap_
```
Proper Name <commit@email.xx>
<proper@email.xx> <commit@email.xx>
Proper Name <proper@email.xx> <commit@email.xx>
Proper Name <proper@email.xx> Commit Name <commit@email.xx>
```

### Ignore Revs

Automated tools (e.g. linters/formatters) which change many lines can lead to
authorship being attributed to the individual who ran the tool instead of the
original author.

However, if you identify the formatting commits and list their full commit SHAs
in a file, Git Authorship can correctly attribute the original author. The
default file is `.git-blame-ignore-revs`, placed at the root of the repository.

_.git-blame-ignore-revs_
```
# Run automated formatter
9c6927b59791eb71cce0a84d8c88fa14d5235fa8

# Run automated linter
ba09bf70676fb13891d15236951450b2f1aa9f3b
```

You can specify an alternate location via the `--ignore-revs-file` option
(resolved relative to the repository root).

```bash
git-authorship REPO_URL --ignore-revs-file .nonstandard-ignore-revs-file
```

### Author Licenses

You can include OSS licensing information for each author via a `.csv` file. 
The `author-name` will be matched to the values shown in the generated
authorship report.

_licensing.csv_ 
```
author-name,license-SPDX-id
```

<sub>A list of SPDX license identifiers can be found at [spdx.org/licenses](https://spdx.org/licenses)</sub>

Then tell the CLI about the authorship file (resolved relative to your current
working directory)

```bash
git-authorship REPO_URL --author-licenses licensing.csv
```

### Pseudonyms
If certain files are being attributed to an unexpected author (e.g. if a
contributor copied code from another project, the `blame` would show the
contributor instead of the original author), you can manually override the
`blame` and licensing information.

_pseudonyms.csv_
```
target-path,actual-author,license-SPDX-id
```
<sub>A list of SPDX license identifiers can be found at [spdx.org/licenses](https://spdx.org/licenses)</sub>

> [!NOTE]
> `target-path` can refer to either a specific file or an entire folder which will be attributed to `actual-author` under the named software license.


Then tell the CLI about the pseudonyms file (resolved relative to your current
working directory)

```bash
git-authorship REPO_URL --pseudonyms pseudonyms.csv
```

## License
Copyright (c) 2022-2024 Joseph Hale, All Rights Reserved

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
