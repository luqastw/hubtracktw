# hubtracktw

A CLI tool for analyzing GitHub repositories. Displays codebase language distribution, activity info, stars, forks, issues and latest release in a formatted dashboard.

## Requirements

- Python >= 3.10

## Installation

```bash
git clone https://github.com/your-user/hubtracktw.git
cd hubtracktw
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Usage

```bash
hubtracktw analyze owner/repo
```

Example:

```bash
hubtracktw analyze torvalds/linux
```
