from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class ConfigUpdater(ABC):
    """
    Base class for updating the configuraiton of the target software,
    to include the new MCP servers we want to add.
    """

    @abstractmethod
    def update_config(self) -> bool:
        pass

    @abstractmethod
    def remove_config_update(self) -> bool:
        pass