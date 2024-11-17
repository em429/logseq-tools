# Logseq Graph Refiner

A tool to help clean up and refine Logseq markdown graphs by removing unnecessary links and identifying empty pages.

## Installation

```bash
pip install .
```

## Usage

```bash
# Basic usage
logseq-refine /path/to/logseq/graph

# Customize minimum content threshold
logseq-refine /path/to/logseq/graph --min-content 10

# Non-interactive mode
logseq-refine /path/to/logseq/graph --no-interactive
```

## Features

- Identifies pages with the most backlinks
- Finds near-empty pages
- Interactive link refinement
- Side-by-side diffs of proposed changes
- User confirmation before applying changes


## TODO:

- Persist the skipped pages for future runs in an easily editable file
- Ability to add to skip list using a config file, so users can add e.g. their full R/books hierarchy
- Add the option to remove the hierarchy (Drafts instead of Resources/Writings/Drafts) and leave only the page name. so three options instead of yes / no: p(age) h(ierarchy) s(kip)