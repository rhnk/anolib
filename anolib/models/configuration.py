from pydantic import BaseModel, Field
from yaml import safe_load, YAMLError
import sys
from pathlib import Path

from anolib.models.alert_channel import AlertChannel
from anolib.models.experiment import Experiment
from anolib.models.input_source import InputSource
from anolib.models.record_set import RecordSet
from anolib.utils.logger import info, error


class Configuration(BaseModel):
    """
    Main configuration class for anomaly detection experiments.
    
    This class manages the configuration for running declarative anomaly detection
    experiments on timeseries data, including record sets, experiments, input sources,
    and alert channels.
    """
    record_sets: dict[str, RecordSet]
    experiments: dict[str, Experiment]
    input_sources: dict[str, InputSource]
    alert_channels: dict[str, AlertChannel] = Field(default_factory=dict)

    def run_experiments(self):
        """Run all configured experiments."""
        # Run experiments
        for name, experiment in self.experiments.items():
            info(f"Processing experiment `{name}`")
            try:
                experiment.run(self.record_sets, self.input_sources, self.alert_channels)
            except Exception as e:
                error(f"Failed to run experiment '{name}': {e}")

    @classmethod
    def init_from_yaml(cls, config_path):
        """
        Initialize Configuration from a YAML file.
        
        Args:
            config_path: Path to the YAML configuration file
            
        Returns:
            Configuration instance
            
        Raises:
            SystemExit: If file doesn't exist or YAML parsing fails
        """
        config_path = Path(config_path)
        if not config_path.exists():
            error(f"Config file not found: {config_path}", exc_info=False)
            sys.exit(1)
        
        try:
            with open(config_path, "r") as config_reader:
                config_dict = safe_load(config_reader)
                return cls(**config_dict)
        except (IOError, OSError) as e:
            error(f"Failed to read config file: {e}", exc_info=False)
            sys.exit(1)
        except YAMLError as e:
            error(f"Failed to parse YAML config: {e}", exc_info=False)
            sys.exit(1)
