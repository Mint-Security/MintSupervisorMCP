import os
import json
from typing import Dict, Any
from src.base.config_updater import ConfigUpdater
from src.utils.node_finder.mac import NodeFinderMac
from src.utils.logger import get_logger

# Create a logger for this module
logger = get_logger(__name__)

class CursorMacMCPConfigEditor(ConfigUpdater):
    CONFIG_FILE_PATH = "~/.cursor/mcp.json"

    def __init__(self, config: Dict[str, Any]):
        super().__init__()
        self.config = config
        self.node_finder = NodeFinderMac()

    @property
    def config_file_path(self) -> str:
        logger.info("config_file_path property called")
        config_path = os.path.expanduser(self.CONFIG_FILE_PATH)
        if not os.path.exists(config_path):
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            with open(config_path, "w") as file:
                json.dump({}, file, indent=4)
            logger.info(f"Config file {config_path} created")
            
        return config_path