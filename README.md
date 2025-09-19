# anolib
Run declarative anomaly detection experiments on timeseries data

## Features
- Declarative configuration via YAML files
- Support for CSV and Excel data sources
- Remote CSV file support via URLs
- Built-in anomaly detection conditions
- Flexible alert channels for notifications

## Installation
```sh
pip install git+https://github.com/rhnk/anolib.git
```

## Getting started
### via import
```python
from anolib.models.configuration import Configuration
config = Configuration.init_from_yaml('config-sample.yml')
config.run_experiments()
```

### via cli
```sh
anolib --config config-sample.yml
```

## Developer Setup

To set up a development environment, use [uv](https://github.com/astral-sh/uv):

1. **Install uv (if not already installed):**
   ```sh
   pip install uv
   ```

2. **Create and activate a virtual environment:**
   ```sh
   uv venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```sh
   uv pip install -e '.[dev]'
   ```

4. **Run tests:**
   ```sh
   uv pip install pytest
   pytest
   ```

5. **Format and lint code:**
   ```sh
   uv pip install black flake8
   black .
   flake8 .
   ```

6. **Install pre-commit hooks (optional):**
   ```sh
   uv pip install pre-commit
   pre-commit install
   ```
