import time
import os
import json
from abc import ABC
from typing import Dict, Any
from .auto_run_enabler import AutoRunEnabler
from .config_updater import ConfigUpdater
from .system_prompt_updater import SystemPromptUpdater
from src.consts import PlatformName, AppName, DOWNLOAD_FILES, ZIP_PASSWORD, INSTALLATION_DIR_NAME
from src.utils.encryption import decrypt_zip
from pathlib import Path
from src.utils.os_utils import get_current_os
from src.utils.os_utils import OperatingSystem
from src.utils.logger import get_logger

# Create a logger for this module
logger = get_logger(__name__)

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
            logger.debug(f"Setting up objects for {self.APP_NAME}")
            logger.debug("Initializing auto run enabler")
            self.auto_run_enabler = auto_run_enabler(self.config)
            logger.debug("Initializing config updater")
            self.config_updater = config_updater(self.config)
            logger.debug("Initializing prompt updater")
            self.prompt_updater = prompt_updater(self.config)
            logger.info(f"Successfully initialized all objects for {self.APP_NAME}")
        except Exception as e:
            logger.error(f"Error setting objects: {e}")
        

    def validate(self) -> bool:
        vlaid_os = get_current_os() == OperatingSystem.MAC
        if not vlaid_os:
            logger.error(f"the os is not valid expected {OperatingSystem.MAC} but got {get_current_os()}")
            return False
        return True
        
    def is_client_installed(self) -> bool:
        logger.debug(f"Checking if {self.APP_NAME} is installed")
        
        #Check is supervisor-server is installed in config file
        if not os.path.exists(self.config_updater.config_file_path):
            logger.debug(f"Config file not found: {self.config_updater.config_file_path}")
            logger.info(f"{self.APP_NAME} is not installed")
            return False
        
        logger.debug(f"Config file found: {self.config_updater.config_file_path}")
        
        try:
            #Check if the config file is valid
            with open(self.config_updater.config_file_path, "r") as f:
                config = json.load(f)
            
            #if config include "supervisor-server" in the "clients" array
            if "supervisor-server" in config.get("mcpServers", []):
                logger.info(f"{self.APP_NAME} is installed")
                return True
            
            logger.info(f"{self.APP_NAME} is not installed")
            return False
            
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Error reading config file for {self.APP_NAME}: {e}")
            return False


    def download_application(self) -> bool:
        try:
            logger.info(f"Starting download process for {self.APP_NAME}")
            zip_filename = DOWNLOAD_FILES[self.APP_NAME][self.PLATFORM_NAME]
            current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            source_zip_path = os.path.join(current_dir, zip_filename)
            home_dir = str(Path.home())
            install_dir = os.path.join(home_dir, INSTALLATION_DIR_NAME)
            final_install_path = os.path.join(install_dir, self.APP_NAME)
            
            logger.debug(f"Source zip path: {source_zip_path}")
            logger.debug(f"Installation directory: {final_install_path}")
            
            if not os.path.exists(source_zip_path):
                logger.error(f"Source zip file not found: {source_zip_path}")
                return False
                
            if not os.path.exists(install_dir):
                logger.info(f"Creating installation directory: {install_dir}")
                os.makedirs(install_dir, exist_ok=True)
            
            if not os.path.exists(final_install_path):
                logger.info(f"Creating final installation path: {final_install_path}")
                os.makedirs(final_install_path, exist_ok=True)
                
            logger.info(f"Decrypting and extracting {zip_filename}")
            decrypt_zip(source_zip_path, final_install_path, ZIP_PASSWORD)
            self.config["installation_path"] = final_install_path
            logger.info(f"Successfully downloaded and extracted {self.APP_NAME}")
            return True
                
        except Exception as e:
            logger.error(f"Error downloading {self.APP_NAME}: {e}")
            return False

    def run_installation(self) -> bool:
        logger.info(f"Starting installation process for {self.APP_NAME}")
        
        if not self.download_application():
            logger.error("Download failed. Cannot proceed with installation.")
            raise ValueError("Download failed. Cannot proceed with installation.")

        if not self.validate():
            logger.error("Validation failed. Cannot proceed with installation.")
            raise ValueError("Validation failed. Cannot proceed with installation.")
        
        logger.info("Download and validation completed successfully")
        
        # update the system prompt of the target application
        logger.info("Updating system prompt")
        self.prompt_updater.update_prompt()
        time.sleep(0.5)
        
        # update the config json of the target application
        logger.info("Updating configuration")
        self.config_updater.update_config()
        time.sleep(0.5)
        
        # enable auto-run to make our mcp server autostart in the target application
        logger.info("Enabling auto-run")
        self.auto_run_enabler.enable_auto_run()
        time.sleep(0.5)
        
        logger.info(f"Installation process completed successfully for {self.APP_NAME}")
        return True
    
    def run_uninstallation(self) -> bool:
        logger.info(f"Starting uninstallation process for {self.APP_NAME}")
        
        logger.info("Disabling auto-run")
        self.auto_run_enabler.disable_auto_run()
        time.sleep(0.5)
        
        logger.info("Removing configuration updates")
        self.config_updater.remove_config_update()
        time.sleep(0.5)
        
        logger.info("Removing system prompt updates")
        self.prompt_updater.remove_prompt_update()
        time.sleep(0.5)
        
        logger.info(f"Uninstallation process completed successfully for {self.APP_NAME}")
        return True
