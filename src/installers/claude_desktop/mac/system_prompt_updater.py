import os
import json
from typing import Dict, Any
from src.base.system_prompt_updater import SystemPromptUpdater

class ClaudeDesktopMacSystemPromptUpdater(SystemPromptUpdater):

    def __init__(self, config: Dict[str, Any]):
        super().__init__()
        self.config = config

    def update_prompt(self) -> bool:
        # TODO: Implement this
        return True
    
    def remove_prompt_update(self) -> bool:
        # TODO: Implement this
        return True
    
    def is_installed(self) -> bool:
        # TODO: Implement this
        return True