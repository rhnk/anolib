import argparse
import logging

from yaml import safe_load

from anolib.models.configuration import Configuration
from anolib.utils.logger import debug


def main():
    # set root logger level
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(
        prog="anolib",
        description="Run declarative anomaly detection experiments on timeseries data",
    )
    parser.add_argument("--config-file", help="Experiment config yaml file path")
    args = parser.parse_args()

    config_reader = open(args.config_file, "r")
    # TODO: validate yaml
    config_dict = safe_load(config_reader)

    # Parse config
    config = Configuration(**config_dict)
    debug(config)
    config.run_experiments()


if __name__ == "__main__":
    main()
