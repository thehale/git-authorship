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
[![Joseph Hale's software engineering blog](https://img.shields.io/badge/jhale.dev-black.svg?style=plastic&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNCIgaGVpZ2h0PSI0IiB2aWV3Qm94PSIwIDAgMS4wNTggMS4wNTgiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGcgY29sb3I9IiMwMDAiIHBhaW50LW9yZGVyPSJmaWxsIG1hcmtlcnMgc3Ryb2tlIj48cGF0aCBkPSJNLjY0My43NTJhLjE1Ni4xNTYgMCAwMC0uMTMuMDU5Qy40NzYuODUuNDcuOTE3LjQ2OS45M2EuMDI1LjAyNSAwIDAwLjAyNi4wMjhoLjA2NmEuMDI1LjAyNSAwIDAwLjAyNC0uMDIuMTIuMTIgMCAwMS4wMi0uMDUyQy42MTguODcuNjMyLjg2OS42NTUuODY5aC4xMjJjMC0uMDAyLjA3Ni4wMDcuMTI5LS4wNUEuMTQzLjE0MyAwIDAwLjkyOC43ODcuMDI1LjAyNSAwIDAwLjkwNi43NTJILjY0M3oiIGZpbGw9IiMwNTAiLz48cGF0aCBkPSJNLjM5My40MWEuMDIuMDIgMCAwMC0uMDIuMDJ2LjI2YzAgLjAxMi4wMDEuMDI5LS4wMTQuMDQ0Qy4zMy43NTkuMjgyLjc1LjI2Ny43MzYuMjU3LjcyOC4yNS43MTMuMjQ0LjY4N0EuMDI1LjAyNSAwIDAwLjIyLjY3SC4xNTNhLjAyNC4wMjQgMCAwMC0uMDI1LjAyNmMuMDA0LjA1Mi4wMjUuMDkuMDUxLjExOWEuMTY3LjE2NyAwIDAwLjExMy4wNTJoLjAzNWEuMTg0LjE4NCAwIDAwLjExNS0uMDVBLjE4Mi4xODIgMCAwMC40OS42OTRWLjQzMUEuMDIuMDIgMCAwMC40Ny40MXpNLjc4Ny4zOWEuMDIuMDIgMCAwMC0uMDIuMDJ2LjI0MmMwIC4wMTEuMDA5LjAyLjAyLjAyaC4wNzdhLjAyLjAyIDAgMDAuMDItLjAyVi40MTFhLjAyLjAyIDAgMDAtLjAyLS4wMnpNLjM5My4yMThhLjAyLjAyIDAgMDAtLjAyLjAydi4wNzdjMCAuMDExLjAwOC4wMi4wMi4wMkguNDdhLjAyLjAyIDAgMDAuMDItLjAyVi4yMzhhLjAyLjAyIDAgMDAtLjAyLS4wMnpNLjU5LjFhLjAyLjAyIDAgMDAtLjAyLjAydi41MzJjMCAuMDExLjAwOS4wMi4wMi4wMmguMDc3YS4wMi4wMiAwIDAwLjAyLS4wMlYuMTJBLjAyLjAyIDAgMDAuNjY3LjF6IiBmaWxsPSIjMDBkNDAwIi8+PC9nPjwvc3ZnPg==)](https://jhale.dev)
[![](https://img.shields.io/badge/Follow-thehale-0A66C2?logo=linkedin)](https://www.linkedin.com/comm/mynetwork/discovery-see-all?usecase=PEOPLE_FOLLOWS&followMember=thehale)

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

1. Clone this repository and open it in the included
   [devcontainer](https://code.visualstudio.com/docs/remote/containers).
2. Clone the repository you wish to analyze into the included `repo` folder.
3. Make copies of the files in the `config` folder without the `dist` extension.
4. Run the analyzer with `make run`
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
