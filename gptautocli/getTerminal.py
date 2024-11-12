

import os
import platform

def get_terminal_type():
    # Check for terminal types on Linux
    if platform.system() == 'Linux':
        if os.path.exists('/usr/bin/gnome-terminal'):
            return 'gnome-terminal'
        elif os.path.exists('/usr/bin/konsole'):
            return 'konsole'
        elif os.path.exists('/usr/bin/xterm'):
            return 'xterm'
        else:
            return 'unknown'
    # Check for terminal on macOS
    elif platform.system() == 'Darwin':
        if os.path.exists('/Applications/iTerm.app'):
            return 'iterm'
        elif os.path.exists('/Applications/Utilities/Terminal.app'):
            return 'mac_terminal'
        # zsh is the default shell on macOS
        elif os.path.exists('/bin/zsh'):
            return 'zsh'
        else:
            return 'unknown'
    # Return a generic terminal type for Windows
    elif platform.system() == 'Windows':
        return 'cmd'
    else:
        return 'unknown'

def is_powershell():
    # Check if the shell is PowerShell
    return 'pwsh' in os.getenv('SHELL', '').lower() or 'powershell' in os.getenv('SHELL', '').lower()

def get_os_type():
    return platform.system()