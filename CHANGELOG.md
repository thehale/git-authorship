# Changelog

## 0.4.0 (2025-03-12)

With this release, `git-authorship` once again has all the features it had in version `0.0.0`, but now much more usable and maintainable.

**Features**
  - Restore `--pseudonyms` feature (previously removed in `0.1.0`)
  - Add `--version` option to CLI
  - Validate config files more strictly (i.e. provide more helpful error messages by failing early)
  - Include descriptions of CSV config columns in CLI `--help` text
  
**Fixes**
  - Output correct results when rerunning authorship with new configs on a previously analyzed revision.
  
**Maintenance**
  - Any modifications to the raw `blame` results are now conducted in separate `augment`ation steps to improve maintainability.

## 0.3.0 (2025-02-18)

**Features**
  - Allow re-cloning the repository in `--no-cache` mode
  - Allow saving reports to custom `--output` folder

**Fixes**
  - Enable cloning into an existing, empty directory

**Maintenance**
  - Improved performance of end-to-end tests

## 0.2.0 (2025-01-10)

**Features**
  - Restored ability to report `--author-licenses` (previously removed in `0.1.0`)

**Maintenance**
  - Add testing instructions to CONTRIBUTING.md

## 0.1.5 (2024-11-09)

**Documentation**
  - Restore alt-text on PyPI

## 0.1.4 (2024-11-09)

**Documentation**
  - Remove alt-text in attempt to render feature image on PyPI

## 0.1.3 (2024-11-09)

**Fixes**
  - Show logs when running via the CLI
  - Enable running `git-authorship` CLI directly after a `pip install`

**Maintenance**
  - Add setup instructions to CONTRIBUTING.md

## 0.1.2 (2024-11-09)

**Documentation**
  - Include README on PyPI

**Maintenance**
  - Document how to publish updates to PyPI

## 0.1.1 (2024-11-09)

**Maintenance**
  - Correctly exclude dependencies unauthorized OSS licenses

## 0.1.0 (2024-11-09)

Overhauled the project to dramatically improve usability.

**Features**
  - Added a CLI: `git-authorship https://github.com/USERNAME/REPOSITORY`
    - Target a specific `--branch` or revision
    - `--clone-to` a specific location.
  - Add CSV export
  - Add JSON export

**Maintenance**
  - Added extensive unit/end-to-end tests to validate functionality.
  - Broke up the single file script into multiple mini modules.
  
**BREAKING CHANGES**
To make the overhaul more manageable, several features were dropped in this initial release.
 - Removed "Author Licensing" feature
 - Removed "Pseudonyms" feature

## 0.0.0 (2023-02-07)

Created a single-file script to analyze git authorship information.