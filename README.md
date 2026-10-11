# Python API Test Framework

API tests for JSONPlaceholder posts and Rick and Morty characters, using Python
3.14+, uv, pytest, requests, JSON Schema validation, and Allure reports.

## Getting started

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then:

```bash
git clone https://github.com/batmanova2021/python-api-test-framework.git
cd python-api-test-framework
uv sync --locked
cp .env.example .env
uv run pytest
```

uv creates `.venv` and installs the Python version in `.python-version` when
needed. `uv.lock` records exact dependency versions; commit it whenever dependencies
change. To upgrade dependencies, run `uv lock --upgrade` and `uv sync --locked`,
then run the quality checks and tests below.

## Configuration

Copy `.env.example` to `.env` to customize either API URL or `API_TIMEOUT`
(a positive number of seconds, default 10). Environment variables override `.env`.
The two APIs have independent settings:

- `JSONPLACEHOLDER_BASE_URL`: defaults to `https://jsonplaceholder.typicode.com`.
- `RICK_AND_MORTY_BASE_URL`: defaults to `https://rickandmortyapi.com/api`.
- `API_TIMEOUT`: applied to every HTTP request.

CLI options override these settings for one run:

```bash
uv run pytest -m rickandmorty --api-timeout 20 \
  --rick-and-morty-base-url https://rickandmortyapi.com/api
uv run pytest -m jsonplaceholdertest \
  --jsonplaceholder-base-url https://jsonplaceholder.typicode.com
```

Tests use the public services' sample data, so alternate URLs must provide the
same contracts and data. API tests need internet access; service outages or data
changes can cause failures.

## Test suites

| Command | Coverage |
| --- | --- |
| `uv run pytest` | All API and local framework tests |
| `uv run pytest -m smoke` | Health checks for both APIs |
| `uv run pytest -m regression` | Headers, post schema, character filters, pagination |
| `uv run pytest -m jsonplaceholdertest` | Original JSONPlaceholder suite |
| `uv run pytest -m rickandmorty` | Original Rick and Morty suite |
| `uv run pytest -m unit` | Framework checks without network access |
| `uv run pytest -n auto` | All tests in parallel |

The existing test paths and API markers are preserved. Shared fixtures in
`tests/conftest.py` manage HTTP clients and schema validation. `config/` holds
environment settings and the HTTP client; `schemas/` contains JSON contracts.

## Code quality

```bash
uv run ruff check .
uv run ruff format --check .
uv run pylint tests/ config/ --fail-under=8.0
uv run mypy
uv run pytest -m unit
```

Use `uv run ruff format .` to apply formatting. mypy checks the typed framework
code in `config/`. In PyCharm, select `.venv/bin/python` (Windows:
`.venv/Scripts/python.exe`) as the project interpreter; the shared run
configurations use it instead of the old machine-specific Windows path.

## Reports

pytest writes Allure results to `allure-results/`, including the request URL,
query parameters, timeout, status, and response body (up to 5,000 characters).
Install [Allure Commandline](https://allurereport.org/docs/install/) to view HTML:

```bash
allure generate allure-results --clean -o allure-report
allure open allure-report
```

Remove old `allure-results/` before a fresh local report to avoid mixing runs.

## GitHub Actions

The `API Tests` workflow runs Ruff, Pylint, mypy, and local framework tests as a
quality gate before the API suite. It uses cached uv installs and
`uv sync --locked` to keep CI dependencies reproducible.

- Pull requests and pushes to `main` or `master` run smoke tests.
- Daily runs at 07:00 UTC (02:00 EST / 03:00 EDT) run regression tests.
- **Actions → API Tests → Run workflow** allows `smoke`, `regression`, or `all`.
- API jobs upload Allure raw results, HTML reports, and JUnit XML even after
  test failures. Artifacts are retained for 14 days.

Configure the same three environment settings under **Settings → Secrets and
variables → Actions → Variables** to customize CI. Dependabot opens weekly
updates for uv dependencies and GitHub Actions.

This modernization follows the structure of the
[student reference repo](https://github.com/nadiaalexqa/python-api-test-framework)
while retaining this repository's two API suites.
