from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from pathlib import Path
from src.consts import MINT_SECTION_START, MINT_SECTION_END

class SystemPromptUpdater(ABC):
    """
    Base class for updating the system prompt of the target application
    to enable our MCP server to "hook" into the application's functionality.
    """

    @staticmethod       
    def wrap_prompt(prompt: str) -> str:
        return f"{MINT_SECTION_START}\n{prompt}\n{MINT_SECTION_END}"

    @abstractmethod
    def update_prompt(self) -> bool:
        pass

    @abstractmethod
    def remove_prompt_update(self) -> bool:
        pass

    @abstractmethod
    def is_installed(self) -> bool:
        pass