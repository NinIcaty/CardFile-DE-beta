# CardFile-DE-beta
A CardFile DE (the pre-Windows 95 Windows DE )  for Linux\n
        IMPORTANT
ADD FOLDERS "WALLPAPERS" and "ICONS"
#INSTRUCTIONS


## Features

- App launcher with card-style UI
- Built-in app editor (edit name, command, icon)
- Drag-and-drop arrangement of app cards
- Desktop wallpaper support
- Window management: minimize, maximize
- Power menu: shutdown, reboot, sleep
- Config saved locally in the same folder
- Fully keyboard accessible (hotkeys for switching windows)

---

## Requirements

- Python 3.13+
- PyQt6
- Linux (Debian-based or Arch-based)
(RedHat should work But not tested)
> ⚠ Note: On Arch, ensure your system libraries are up to date to avoid ICU library issues with PyQt6.

---

## Installation

### Debian / Ubuntu

```bash
# Update package list
sudo apt update

# Install Python3, pip, and PyQt6
sudo apt install python3 python3-pip python3-pyqt6 python3-pyqt6.qtwebengine

# Clone the repository
git clone https://github.com/YourUsername/CardFile-DE.git
cd CardFile-DE

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
git clone https://github.com/YourUsername/CardFile-DE.git
cd CardFile-DE

# Make the main script executable
chmod +x cardfile-shell.py
