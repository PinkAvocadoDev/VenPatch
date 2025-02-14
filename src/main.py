# main.py
#
# Copyright 2025 Andrea
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
import gi
import os
import subprocess

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, Gio, Adw
from .window import VenpatchWindow


class VenpatchApplication(Adw.Application):
    """The main application singleton class."""

    usr_data_folder = subprocess.run("echo $HOME", shell = True,capture_output=True, text=True).stdout[:-1] + "/.var/app/io.github.pinkavocadodev.venpatch/data/"

    def __init__(self):
        super().__init__(
            application_id="io.github.pinkavocadodev.venpatch",
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
        )
        self.create_action("quit", lambda *_: self.quit(), ["<primary>q"])
        self.create_action("about", self.on_about_action)
        self.create_action('preferences', self.on_preferences_action)
        self.initial_setup()

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        win = self.props.active_window
        if not win:
            win = VenpatchWindow(application=self)
        win.present()

    def on_preferences_action(self, widget, _):
        """Callback for the app.preferences action."""
        print('app.preferences action activated')

    def on_about_action(self, widget, _):
        """Callback for the app.about action."""
        about = Adw.AboutWindow(
            transient_for=self.props.active_window,
            application_name="VenPatch",
            application_icon="io.github.pinkavocadodev.venpatch",
            developer_name="Andrea",
            version="0.1.0",
            developers=["Andrea"],
            copyright="© 2025 Andrea",
        )
        about.present()

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)

    def initial_setup(self):
        #Generate askpass.sh file
        if not os.path.isfile(self.usr_data_folder + "askpass.sh") :
            print("Generating askpass.sh")
            with open(self.usr_data_folder + "askpass.sh", "w") as ask:
                ask.write('''\
#!/bin/bash
zenity --password --title "Sudo permission required"''')

        chmod_askpass = subprocess.run("chmod +x $HOME/.var/app/io.github.pinkavocadodev.venpatch/data/askpass.sh", shell = True,capture_output=True, text=True, executable="/bin/bash")

        #Generate install.sh script
        if not os.path.isfile(self.usr_data_folder + "install.sh") :
            print("Generating install.sh")
            with open(self.usr_data_folder + "install.sh", 'w') as ins:
                ins.write('''\
#!/bin/bash
data_dir="${XDG_DATA_HOME:-$HOME/.var/app/}/io.github.pinkavocadodev.venpatch/data/outfile"
curl -sS https://github.com/Vendicated/VencordInstaller/releases/latest/download/VencordInstallerCli-Linux \
--output $data_dir \
--location \
--fail
chmod +x "${XDG_DATA_HOME:-$HOME/.var/app/}/io.github.pinkavocadodev.venpatch/data/outfile"''')

        chmod_installer = subprocess.run("chmod +x $HOME/.var/app/io.github.pinkavocadodev.venpatch/data/install.sh", shell = True,capture_output=True, text=True, executable="/bin/bash")

        #Download VencordInstaller
        if not os.path.isfile(self.usr_data_folder + "outfile") :
            print("Downloading")
            venc_installer_run = subprocess.run("flatpak-spawn --host $HOME/.var/app/io.github.pinkavocadodev.venpatch/data/./install.sh", shell = True,capture_output=True, text=True, executable="/bin/bash")


def main(version):
    """The application's entry point."""
    app = VenpatchApplication()
    return app.run(sys.argv)
