# Logseq Graph Refiner

A CLI tool to help clean up and optimize your Logseq graph by removing unnecessary backlinks.

## Features

- Scan Logseq markdown pages
- Identify pages with excessive backlinks
- Interactive link removal
- Configurable refinement criteria

## Installation

```bash
pip install .
```

## Usage

```bash
logseq-refine --pages-dir /path/to/logseq/pages
```

### Options

- `--pages-dir`: Directory containing Logseq markdown pages (default: current directory)
- `--max-backlinks`: Maximum number of backlinks to consider for refinement (default: 5)
- `--max-content-lines`: Maximum content lines for a page to be considered for refinement (default: 3)


### TODO
- filter out logseq/bak dir fully
- change max-backlinks to min-backlinks
- add actual file editing and saving capability, not just preview
- remove syntax highlighting and display the diff side by side, with only the diff part green/red!