import os
from src.consts import AppName, PlatformName
from src.base.base_installer import BaseInstaller
from src.installers.claude_desktop.mac.mcp_config_editor import ClaudeDesktopMacMCPConfigEditor
from src.installers.claude_desktop.mac.system_prompt_updater import ClaudeDesktopMacSystemPromptUpdater
from src.installers.claude_desktop.mac.yolo_enabler import ClaudeDesktopMacYOLOEnabler

class ClaudeDesktopMacInstaller(BaseInstaller):

    PLATFORM_NAME = PlatformName.MAC
    APP_NAME = AppName.CLAUDE_DESKTOP

    def __init__(self):
        try:
            super().__init__()
            self.set_objects(ClaudeDesktopMacYOLOEnabler, ClaudeDesktopMacMCPConfigEditor, ClaudeDesktopMacSystemPromptUpdater)
        except Exception as e:
            print(f"Error initializing ClaudeDesktopMacInstaller: {e}")

    def validate(self) -> bool:
        is_valid = super().validate()
        if not is_valid:
            return False
        
        # Check if Claude Desktop is installed
        claude_app_path = "/Applications/Claude.app"
        claude_installed = os.path.exists(claude_app_path)
        if not claude_installed:
            print("Claude Desktop is not installed")
            return False
        
        return True