#!/bin/bash
# Cardfile Session Script

# --- 1. Set wallpaper ---
# You can change "default.jpg" to any in the wallpapers/ folder
feh --bg-scale "$HOME/CardFile/wallpapers/default.jpg" &

# --- 2. Start hotkey daemon ---
# Needs sxhkd installed
sxhkd -c "$HOME/CardFile/sxhkdrc" &

# --- 3. Start window manager ---
# You need a WM to manage windows (Cardfile is a shell, not a WM).
# Openbox is lightweight and good for this.
openbox-session &

# --- 4. Start the Cardfile shell ---
python3 "$HOME/CardFile/cardfile-shell.py"

