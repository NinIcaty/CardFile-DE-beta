# CardFile-DE-beta
A CardFile DE (the pre-Windows 95 Windows DE )  for Linux\n

### Instructions
## Features

- App launcher with card-style UI
- Built-in app editor (edit name, command, icon)
- Wallpaper support
- Power menu: shutdown, reboot, sleep
- Config saved locally in the same folder
- Fully keyboard accessible (hotkeys for switching windows)
(yea nothing much)
---

## Requirements

- Python 3.13+
- PyQt6
- Linux (Debian-based or Arch-based)
> ⚠ RedHat should work But not tested

> ⚠ Note: On Arch, ensure your system libraries are up to date to avoid ICU library issues with PyQt6.

---
## Parameters
At the moment there are only two parameters 
# -wallpaper 
You need to add path to the Image for the wallpaper
# -wallpaper-none
Disables wallpaper
## Recomendations
-Alacarte if you are using this on top of GNOME

-GDM if you want to use this as a stand alone DE
## Installation

### Debian / Ubuntu

```bash
# Update package list
sudo apt update

# Install Python3, pip, and PyQt6
sudo apt install python3 python3-pip python3-pyqt6 python3-pyqt6.qtwebengine

# Clone the repository
git clone https://github.com/NinIcaty/CardFile-DE-beta.git
cd CardFile-DE-beta

# Make the main script executable
chmod +x cardfile-shell.py
```



### Arch / Manjaro
```
# Update your system (recommended)
sudo pacman -Syu

# Install Python3 and PyQt6
sudo pacman -S python python-pyqt6 python-pyqt6-sip

# Clone the repository
git clone https://github.com/NinIcaty/CardFile-DE-beta.git
cd CardFile-DE-beta

# Make the main script executable
chmod +x cardfile-shell.py
