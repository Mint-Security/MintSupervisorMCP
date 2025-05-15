import subprocess
import time
from typing import Dict, Any
import os
import shutil
from src.consts import AppName, PlatformName
from src.utils.os_utils import get_current_os, OperatingSystem
from src.base.base_installer import BaseInstaller

from src.installers.claude_desktop.mac.mcp_config_editor import ClaudeDesktopMacMCPConfigEditor
from src.installers.claude_desktop.mac.system_prompt_updater import ClaudeDesktopMacSystemPromptUpdater
from src.installers.claude_desktop.mac.yolo_enabler import ClaudeDesktopMacYOLOEnabler

class ClaudeDesktopMacInstaller(BaseInstaller):

    def __init__(self):
        try:
            super().__init__()
            self.set_objects(ClaudeDesktopMacYOLOEnabler, ClaudeDesktopMacMCPConfigEditor, ClaudeDesktopMacSystemPromptUpdater)
        except Exception as e:
            print(f"Error initializing ClaudeDesktopMacInstaller: {e}")

    PLATFORM_NAME = PlatformName.MAC
    APP_NAME = AppName.CLAUDE_DESKTOP

    def validate(self) -> bool:
        valid_os = get_current_os() == OperatingSystem.MAC
        if not valid_os:
            print(f"the os is not valid expected {OperatingSystem.MAC} but got {get_current_os()}")
            return False
        
        # Check if Claude Desktop is installed
        claude_app_path = "/Applications/Claude.app"
        claude_installed = os.path.exists(claude_app_path)
        if not claude_installed:
            print("Claude Desktop is not installed")
            return False
        
        return True

    def setup(self) -> bool:
        # killing the claude process before starting to run
        os.system("osascript -e 'quit app \"Claude\"'")
        # Wait until it's closed
        while subprocess.run(["pgrep", "-x", "Claude"], stdout=subprocess.DEVNULL).returncode == 0:
            time.sleep(1)
        return True

    def uninstall_setup(self) -> bool:
        return self.setup()
