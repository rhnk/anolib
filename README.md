# anolib
Run declarative anomaly detection experiments on timeseries data

## Installation

## Getting started
### via import
```python
from anolib.models.configuration import Config
config = Configuration.init_from_yaml('config-sample.yml')
config.run_experiments()
```

### via cli
```sh
anolib --config config-sample.yml
```
