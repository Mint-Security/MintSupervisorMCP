from abc import ABC, abstractmethod
import os
import json
from src.consts import AGENT_ID
from src.utils.logger import get_logger
# Create a logger for this module
logger = get_logger(__name__)   


class ConfigUpdater(ABC):
    """
    Base class for updating the configuraiton of the target software,
    to include the new MCP servers we want to add.
    """

    @property
    @abstractmethod
    def config_file_path(self) -> str:
        """Path to the application's config file. Must be implemented by subclasses."""
        pass

    def update_config(self) -> bool:
        try:
            # Read the config file
            with open(self.config_file_path, 'r', encoding='utf-8', errors='ignore') as f:
                config = json.load(f)
            
            # Create or update MCP servers configuration
            if 'mcpServers' not in config:
                config['mcpServers'] = {}
            
            installation_path = self.config.get("installation_path", "")
            if not installation_path:
                return False

            # Add our supervisor tool server
            supervisor_config = {
                "command": self.node_finder.get_node_path(),
                "args": [
                    os.path.join(installation_path + "/compiled/dist/", "server.js"),
                ],
                "env": {
                    "AGENT_ID": f"claude_code_{AGENT_ID}"
                }
            }
            
            # Insert supervisor-server as the first key in mcpServers
            from collections import OrderedDict
            mcp_servers = config['mcpServers']
            new_mcp_servers = OrderedDict()
            new_mcp_servers["supervisor-server"] = supervisor_config
            for k, v in mcp_servers.items():
                if k != "supervisor-server":
                    new_mcp_servers[k] = v
            config['mcpServers'] = new_mcp_servers
            
            # Write the updated config back
            with open(self.config_file_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4)
                
            return True
            
        except Exception as e:
            print(f"Error updating Claude Code MCP configuration: {str(e)}")
            return False 
        

    def remove_config_update(self) -> bool:
        try:
            # Read the config file
            with open(self.config_file_path, 'r', encoding='utf-8', errors='ignore') as f:
                config = json.load(f)
            
            # Remove supervisor server if it exists
            if 'mcpServers' in config and "supervisor-server" in config['mcpServers']:
                del config['mcpServers']["supervisor-server"]
            
            # Write the updated config back
            with open(self.config_file_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4)
                
            return True
            
        except Exception as e:
            print(f"Error removing supervisor config from Claude Desktop: {str(e)}")
            return False
        
    def is_installed(self) -> bool:
        if not os.path.exists(self.config_file_path):
            return False
        try:
            with open(self.config_file_path, 'r', encoding='utf-8', errors='ignore') as f:
                config = json.load(f)
            return "supervisor-server" in config.get("mcpServers", [])
        except (json.JSONDecodeError, IOError, UnicodeDecodeError) as e:
            logger.error(f"Error reading config file: {e}")
            return False