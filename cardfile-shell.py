#!/usr/bin/env python3
from PyQt6.QtGui import QAction
from PyQt6.QtGui import QIcon, QPixmap, QKeySequence, QAction

import sys, subprocess, shutil, os
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QFileDialog, QMessageBox, QListWidget, QListWidgetItem,
    QInputDialog, QDialog, QLineEdit, QDialogButtonBox
)
from PyQt6.QtGui import QIcon, QPixmap, QKeySequence
from PyQt6.QtCore import Qt, QSize

# -----------------------------
# CONFIGURATION
# -----------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
CONFIG_FILE = SCRIPT_DIR / ".cardfile_apps.txt"
ICONS_DIR = SCRIPT_DIR / "ICONS"
ICONS_DIR.mkdir(exist_ok=True)
WALLPAPERS_DIR = SCRIPT_DIR / "WALLPAPERS"
WALLPAPERS_DIR.mkdir(exist_ok=True)

# -----------------------------
# APP DATA CLASS
# -----------------------------
class AppEntry:
    def __init__(self, name, command, icon=None):
        self.name = name
        self.command = command
        self.icon = icon

    def serialize(self):
        return f"{self.name}|{self.command}|{self.icon or ''}"

    @staticmethod
    def deserialize(line):
        parts = line.strip().split("|")
        if len(parts) >= 2:
            name, command = parts[0], parts[1]
            icon = parts[2] if len(parts) > 2 and parts[2] else None
            return AppEntry(name, command, icon)
        return None

# -----------------------------
# LOAD/SAVE APPS
# -----------------------------
def load_apps():
    apps = []
    if CONFIG_FILE.exists():
        for line in CONFIG_FILE.read_text(encoding="utf-8").splitlines():
            app = AppEntry.deserialize(line)
            if app:
                apps.append(app)
    else:
        # default apps
        for name, cmd in [("Firefox","firefox"), ("Gedit","gedit")]:
            path = shutil.which(cmd)
            if path:
                apps.append(AppEntry(name, path))
    return apps

def save_apps(apps):
    CONFIG_FILE.write_text("\n".join(app.serialize() for app in apps), encoding="utf-8")

# -----------------------------
# EDIT DIALOG
# -----------------------------
class EditDialog(QDialog):
    def __init__(self, app: AppEntry, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit App")
        self.app = app
        self.setFixedSize(300, 200)
        layout = QVBoxLayout(self)

        self.name_edit = QLineEdit(app.name)
        self.cmd_edit = QLineEdit(app.command)

        layout.addWidget(QLabel("Name:"))
        layout.addWidget(self.name_edit)
        layout.addWidget(QLabel("Command:"))
        layout.addWidget(self.cmd_edit)

        icon_btn = QPushButton("Choose Icon")
        icon_btn.clicked.connect(self.choose_icon)
        layout.addWidget(icon_btn)

        self.delete_btn = QPushButton("Delete App")
        self.delete_btn.setStyleSheet("color: red;")
        layout.addWidget(self.delete_btn)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def choose_icon(self):
        icon_path, _ = QFileDialog.getOpenFileName(self, "Choose Icon", str(ICONS_DIR),
                                                   "Images (*.png *.jpg *.svg *.ico)")
        if icon_path:
            self.app.icon = icon_path

    def apply_changes(self):
        self.app.name = self.name_edit.text().strip()
        self.app.command = self.cmd_edit.text().strip()

# -----------------------------
# CARD WIDGET
# -----------------------------
class CardWidget(QWidget):
    def __init__(self, app: AppEntry, launch_callback, edit_callback):
        super().__init__()
        self.app = app
        self.launch_callback = launch_callback
        self.edit_callback = edit_callback

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label = QLabel(app.name)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        self.icon_btn = QPushButton()
        self.icon_btn.setIconSize(QSize(128, 128))
        self.icon_btn.setFixedSize(140, 140)
        self.update_icon()
        self.icon_btn.clicked.connect(lambda: self.launch_callback(app))
        layout.addWidget(self.icon_btn)

        self.edit_btn = QPushButton("Edit")
        self.edit_btn.clicked.connect(lambda: self.edit_callback(app))
        layout.addWidget(self.edit_btn)

        self.setLayout(layout)
        self.setFixedSize(160, 220)

    def update_icon(self):
        if self.app.icon and Path(self.app.icon).exists():
            self.icon_btn.setIcon(QIcon(self.app.icon))
        else:
            self.icon_btn.setIcon(QIcon.fromTheme("application-x-executable"))

# -----------------------------
# MAIN WINDOW / DE
# -----------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cardfile DE")
        self.apps = load_apps()
        self.showFullScreen()

        # Central widget
        self.list_widget = QListWidget()
        self.list_widget.setViewMode(QListWidget.ViewMode.IconMode)
        self.list_widget.setMovement(QListWidget.Movement.Snap)
        self.list_widget.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.list_widget.setSpacing(20)
        self.list_widget.setDragDropMode(QListWidget.DragDropMode.InternalMove)

        # Desktop wallpaper
        self.desktop_label = QLabel()
        self.desktop_label.setScaledContents(True)
        layout = QVBoxLayout()
        layout.addWidget(self.desktop_label)
        layout.addWidget(self.list_widget)

        # Top menu buttons
        self.power_btn = QPushButton("⏻ Power")
        self.power_btn.clicked.connect(self.show_power_menu)
        self.add_btn = QPushButton("Add App")
        self.add_btn.clicked.connect(self.add_app)
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.add_btn)
        top_layout.addStretch()
        top_layout.addWidget(self.power_btn)

        central_layout = QVBoxLayout()
        central_layout.addLayout(top_layout)
        central_layout.addWidget(self.desktop_label)
        central_layout.addWidget(self.list_widget)

        container = QWidget()
        container.setLayout(central_layout)
        self.setCentralWidget(container)

        self.refresh_cards()
        self.load_wallpaper()
        self.setup_hotkeys()

    # -----------------------------
    # Wallpaper
    # -----------------------------
    def load_wallpaper(self):
        wallpapers = list(WALLPAPERS_DIR.glob("*"))
        if wallpapers:
            self.desktop_label.setPixmap(QPixmap(str(wallpapers[0])))

    # -----------------------------
    # Cards
    # -----------------------------
    def refresh_cards(self):
        self.list_widget.clear()
        for app in self.apps:
            item = QListWidgetItem()
            item.setSizeHint(QSize(160, 220))
            widget = CardWidget(app, self.launch_app, self.edit_app_by_ref)
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, widget)

    def launch_app(self, app: AppEntry):
        try:
            subprocess.Popen(app.command.split())
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not launch: {e}")

    def edit_app_by_ref(self, app: AppEntry):
        idx = self.apps.index(app)
        self.edit_app(idx)

    def edit_app(self, idx):
        app = self.apps[idx]
        dlg = EditDialog(app, self)
        dlg.delete_btn.clicked.connect(lambda: self.delete_app(idx, dlg))
        if dlg.exec():
            dlg.apply_changes()
            save_apps(self.apps)
            self.refresh_cards()

    def delete_app(self, idx, dlg):
        if QMessageBox.question(self, "Confirm Delete", "Delete this app?") == QMessageBox.StandardButton.Yes:
            del self.apps[idx]
            save_apps(self.apps)
            self.refresh_cards()
            dlg.reject()

    def add_app(self):
        name, ok = QInputDialog.getText(self, "App Name", "Enter name:")
        if not ok or not name.strip():
            return
        cmd, ok = QInputDialog.getText(self, "Command", "Enter command to run:")
        if not ok or not cmd.strip():
            return
        self.apps.append(AppEntry(name.strip(), cmd.strip()))
        save_apps(self.apps)
        self.refresh_cards()

    # -----------------------------
    # Power Menu
    # -----------------------------
    def show_power_menu(self):
        menu = QMessageBox(self)
        menu.setWindowTitle("Power Options")
        menu.setText("Choose an action:")
        shutdown = menu.addButton("Shutdown", QMessageBox.ButtonRole.AcceptRole)
        reboot = menu.addButton("Reboot", QMessageBox.ButtonRole.AcceptRole)
        sleep = menu.addButton("Sleep", QMessageBox.ButtonRole.AcceptRole)
        cancel = menu.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)
        menu.exec()
        if menu.clickedButton() == shutdown:
            subprocess.Popen(["systemctl", "poweroff"])
        elif menu.clickedButton() == reboot:
            subprocess.Popen(["systemctl", "reboot"])
        elif menu.clickedButton() == sleep:
            subprocess.Popen(["systemctl", "suspend"])

    # -----------------------------
    # Hotkeys (only work inside DE window)
    # -----------------------------
    def setup_hotkeys(self):
        self.shortcut_close = QKeySequence("Meta+X")
        self.shortcut_switch = QKeySequence("Meta+Tab")
        self.addAction(self.create_action("Close Window", self.hotkey_close, self.shortcut_close))
        self.addAction(self.create_action("Switch Window", self.hotkey_switch, self.shortcut_switch))

    def create_action(self, name, func, keyseq):
        action = QAction(name, self)
        action.triggered.connect(func)
        action.setShortcut(keyseq)
        return action

    def hotkey_close(self):
        widget = QApplication.focusWidget()
        if widget and isinstance(widget, QWidget) and widget != self.desktop_label:
            widget.close()

    def hotkey_switch(self):
        # simple focus switch
        self.list_widget.setFocus()

# -----------------------------
# MAIN
# -----------------------------
def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()


