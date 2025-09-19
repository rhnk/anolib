import argparse
import logging
import sys
from pathlib import Path

from yaml import safe_load, YAMLError

from anolib.models.configuration import Configuration
from anolib.utils.logger import debug, error


def main():
    """
    Main entry point for the anolib CLI.
    
    Parses command line arguments, loads configuration from YAML file,
    and runs anomaly detection experiments.
    """
    # set root logger level
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(
        prog="anolib",
        description="Run declarative anomaly detection experiments on timeseries data",
    )
    parser.add_argument("--config", help="Experiment config yaml file path", required=True)
    args = parser.parse_args()

    # Check if config file exists
    config_path = Path(args.config)
    if not config_path.exists():
        error(f"Config file not found: {config_path}", exc_info=False)
        sys.exit(1)

    try:
        with open(args.config, "r") as config_reader:
            config_dict = safe_load(config_reader)
    except (IOError, OSError) as e:
        error(f"Failed to read config file: {e}", exc_info=False)
        sys.exit(1)
    except YAMLError as e:
        error(f"Failed to parse YAML config: {e}", exc_info=False)
        sys.exit(1)

    try:
        # Parse config
        config = Configuration(**config_dict)
        debug(config)
        config.run_experiments()
    except Exception as e:
        error(f"Failed to run experiments: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
