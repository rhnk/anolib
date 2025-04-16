# anolib
Run declarative anomaly detection experiments on timeseries data

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
