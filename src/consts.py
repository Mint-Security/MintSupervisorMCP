ZIP_PASSWORD = "qpcrnAeFJv4lGO3tazEM9bvzoBB23uCj"
INSTALLATION_DIR_NAME = "MintSecurity"
AGENT_ID = "4a7c6329-0e35-4715-b352-6acf605e2d8e"

# System prompt section markers
MINT_SECTION_START = "<!-- MINT_SECURITY_START -->"
MINT_SECTION_END = "<!-- MINT_SECURITY_END -->"
# Folders to remove during uninstallation
UNINSTALL_FOLDERS = [
    "~/.mint",
    "~/MintSecurity"
]

class PlatformName:
    MAC = "mac"
    LINUX = "linux"
    WINDOWS = "windows"

class AppName:
    CURSOR = "cursor"
    CLAUDE_CODE = "claude-code"
    CLAUDE_DESKTOP = "claude-desktop"
    WINDSURF = "windsurf"

DOWNLOAD_URLS = {
    AppName.CURSOR: {
        PlatformName.MAC: "cursor-mac.zip",
        PlatformName.LINUX: "cursor-linux.zip",
        PlatformName.WINDOWS: "cursor-windows.zip"
    },
    AppName.CLAUDE_CODE: {
        PlatformName.MAC: "claude-code-mac.zip",
        PlatformName.LINUX: "claude-code-linux.zip",
        PlatformName.WINDOWS: "claude-code-windows.zip"
    },
    AppName.CLAUDE_DESKTOP: {
        PlatformName.MAC: "claude-desktop-mac.zip",
        PlatformName.LINUX: "claude-desktop-linux.zip",
        PlatformName.WINDOWS: "claude-desktop-windows.zip"
    },
    AppName.WINDSURF: {
        PlatformName.MAC: "windsurf-mac.zip",
        PlatformName.LINUX: "windsurf-linux.zip",
        PlatformName.WINDOWS: "windsurf-windows.zip"
    }
}

DOWNLOAD_FILES = {
    AppName.CURSOR: {
        PlatformName.MAC: "default.zip",
        PlatformName.LINUX: "cursor-linux.zip",
        PlatformName.WINDOWS: "cursor-windows.zip"
    },
    AppName.CLAUDE_CODE: {
        PlatformName.MAC: "default.zip",
        PlatformName.LINUX: "claude-code-linux.zip",
        PlatformName.WINDOWS: "claude-code-windows.zip"
    },
    AppName.CLAUDE_DESKTOP: {
        PlatformName.MAC: "claude-desktop.zip",
        PlatformName.LINUX: "claude-desktop-linux.zip",
        PlatformName.WINDOWS: "claude-desktop-windows.zip"
    },
    AppName.WINDSURF: {
        PlatformName.MAC: "default.zip",
        PlatformName.LINUX: "windsurf-linux.zip",
        PlatformName.WINDOWS: "windsurf-windows.zip"
    }
}
