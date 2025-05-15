import time
import os
import tempfile
from uuid import uuid4
from abc import ABC, abstractmethod
from typing import Dict, Any
from .auto_run_enabler import AutoRunEnabler
from .config_updater import ConfigUpdater
from .system_prompt_updater import SystemPromptUpdater
from src.consts import PlatformName, AppName, DOWNLOAD_FILES, ZIP_PASSWORD, INSTALLATION_DIR_NAME
from src.utils.encryption import decrypt_zip
from pathlib import Path

class BaseInstaller(ABC):
    def __init__(self):
        self.config: Dict[str, Any] = {}
        self.auto_run_enabler = None
        self.config_updater = None
        self.prompt_updater = None

    PLATFORM_NAME: PlatformName
    APP_NAME: AppName

    def set_objects(self, auto_run_enabler: AutoRunEnabler, config_updater: ConfigUpdater, prompt_updater: SystemPromptUpdater):
        try:
            self.auto_run_enabler = auto_run_enabler(self.config)
            self.config_updater = config_updater(self.config)
            self.prompt_updater = prompt_updater(self.config)
        except Exception as e:
            print(f"Error setting objects: {e}")
        

    @abstractmethod
    def validate(self) -> bool:
        pass

    @abstractmethod
    def setup(self) -> bool:
        pass

    @abstractmethod
    def uninstall_setup(self) -> bool:
        pass

    def download_application(self) -> bool:
        try:
            zip_filename = DOWNLOAD_FILES[self.APP_NAME][self.PLATFORM_NAME]
            current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            source_zip_path = os.path.join(current_dir, zip_filename)
            home_dir = str(Path.home())
            install_dir = os.path.join(home_dir, INSTALLATION_DIR_NAME)
            final_install_path = os.path.join(install_dir, self.APP_NAME)
            
            if not os.path.exists(source_zip_path):
                return False
                
            if not os.path.exists(install_dir):
                os.makedirs(install_dir, exist_ok=True)
            
            if not os.path.exists(final_install_path):
                os.makedirs(final_install_path, exist_ok=True)
                
            decrypt_zip(source_zip_path, final_install_path, ZIP_PASSWORD)
            self.config["installation_path"] = final_install_path
            return True
                
        except Exception as e:
            print(f"Error downloading {self.APP_NAME}: {e}")
            return False

    def run_installation(self) -> bool:
        if not self.download_application():
            raise ValueError("Download failed. Cannot proceed with installation.")

        if not self.validate():
            raise ValueError("Validation failed. Cannot proceed with installation.")
        
        if not self.setup():
            raise ValueError("Setup failed. Cannot proceed with installation.")
        
        # update the system prompt of the target application
        self.prompt_updater.update_prompt()
        time.sleep(0.5)
        # update the config json of the target application
        self.config_updater.update_config()
        time.sleep(0.5)
        # enable auto-run to make our mcp server autostart in the target application
        self.auto_run_enabler.enable_auto_run()
        time.sleep(0.5)
        return True
    
    def run_uninstallation(self) -> bool:
        if not self.uninstall_setup():
            raise ValueError("Uninstall setup failed. Cannot proceed with uninstallation.")
        
        self.auto_run_enabler.disable_auto_run()
        time.sleep(0.5)
        self.config_updater.remove_config_update()
        time.sleep(0.5)
        self.prompt_updater.remove_prompt_update()
        time.sleep(0.5)
        return True
