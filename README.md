# hubtracktw

A command-line tool for inspecting GitHub repositories. It queries the GitHub REST API and renders a formatted dashboard with language distribution, activity timeline, community metrics and release information directly in the terminal.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Design Decisions](#design-decisions)
- [License](#license)

---

## Overview

hubtracktw accepts a repository identifier (either `owner/repo` or a full GitHub URL), fetches data from multiple GitHub API endpoints concurrently, and presents the results as a rich terminal dashboard. The output includes:

- **Language distribution** -- byte-level breakdown of the top 6 languages with visual progress bars.
- **Activity timeline** -- last push date, repository creation date and default branch.
- **Community metrics** -- star count, fork count, open issues and contributor count.
- **Release info** -- latest release tag, when available.

## Architecture

The project follows a layered architecture with clear separation of concerns:

```
CLI Layer (cli.py)        --> User interaction, input parsing, terminal rendering
Client Layer (client.py)  --> HTTP communication with the GitHub REST API
Model Layer (models.py)   --> Domain data structures (dataclasses)
Service Layer (services.py) --> Business logic (extensible)
```

Data flows in a single direction: the CLI layer delegates to the client, which returns typed model objects. The CLI then formats and renders the data. There is no coupling between the HTTP layer and the presentation layer.

## Tech Stack

| Component        | Technology                                   |
|------------------|----------------------------------------------|
| Language         | Python 3.10+                                 |
| CLI Framework    | [Typer](https://typer.tiangolo.com/)         |
| Terminal Rendering | [Rich](https://rich.readthedocs.io/)       |
| HTTP Client      | [HTTPX](https://www.python-httpx.org/)      |
| Build System     | setuptools                                   |
| Packaging        | PEP 621 (`pyproject.toml`)                  |

**Why these choices:**

- **Typer** provides type-safe argument parsing built on top of Click, with automatic help generation and shell completion.
- **Rich** enables structured terminal output (tables, panels, progress bars) without external dependencies on ncurses or similar libraries.
- **HTTPX** offers a modern, async-capable HTTP client with timeout control and full type annotations -- a direct improvement over `requests` for typed Python codebases.

## Requirements

- Python >= 3.10
- A network connection to reach `api.github.com`
- (Optional) A GitHub personal access token for higher rate limits

To authenticate, export your token before running the tool:

```bash
export GITHUB_TOKEN=ghp_yourtoken
```

The client reads `GITHUB_TOKEN` from the environment automatically.

## Installation

```bash
git clone https://github.com/luqastw/hubtracktw.git
cd hubtracktw
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

After installation, the `hubtracktw` command is available in the active virtual environment.

## Usage

The tool accepts either the `owner/repo` shorthand or a full GitHub URL:

```bash
hubtracktw track torvalds/linux
```

```bash
hubtracktw track https://github.com/torvalds/linux
```

A quick connectivity check is also available:

```bash
hubtracktw ping
```

## Project Structure

```
hubtracktw/
  pyproject.toml              # Project metadata and dependencies (PEP 621)
  src/
    hubtracktw/
      __init__.py
      cli.py                  # Typer application, input parsing and Rich rendering
      client.py               # GitHubClient -- typed HTTP wrapper over the GitHub REST API
      models.py               # Repo dataclass -- domain model with full type annotations
      services.py             # Service layer (extensible)
  tests/
    __init__.py
```

## Design Decisions

**Typed domain models over raw dicts** -- API responses are mapped into `@dataclass` objects (`Repo`) at the client boundary. This ensures that the rest of the application works with validated, well-typed data instead of unstructured dictionaries.

**Single-responsibility modules** -- Each module has one job: `client.py` handles HTTP, `models.py` defines data structures, `cli.py` owns presentation. This makes the codebase easy to extend (e.g., adding a new data source or output format) without modifying unrelated code.

**Graceful degradation** -- Optional API data (contributors, latest release) is fetched in isolated try/except blocks. If an endpoint fails or is unavailable, the dashboard still renders with the data that succeeded.

**Human-readable formatting** -- Large numbers are abbreviated (`1.2k`, `3.4M`) and timestamps are displayed as relative time (`3d ago`, `2mo ago`) for quick scanning.

## License

Distributed under the [MIT License](LICENSE).
