# main.py
#
# Copyright 2025 PinkAvocadoDev
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

from gi.repository import Gtk, Gio, Adw, GLib
from .window import VenpatchWindow
from .shared import *

class VenpatchApplication(Adw.Application):
    """The main application singleton class."""

    usr_data_folder = return_user_data_folder()

    def __init__(self):
        super().__init__(
            application_id="io.github.pinkavocadodev.venpatch",
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
        )
        self.create_action("quit", lambda *_: self.quit(), ["<primary>q"])
        self.create_action("about", self.on_about_action)
        log("Application initialized")

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        win = self.props.active_window
        if not win:
            win = VenpatchWindow(application=self)
        self.create_action("preferences", win.on_preferences_action)
        initial_setup()
        win.present()

    def on_about_action(self, widget, _):
        """Callback for the app.about action."""
        about = Adw.AboutWindow(
            transient_for=self.props.active_window,
            application_name="VenPatch",
            application_icon="io.github.pinkavocadodev.venpatch",
            developer_name="PinkAvocadoDev",
            version="1.0.0",
            developers=["PinkAvocadoDev https://github.com/PinkAvocadoDev"],
            copyright="© 2025 PinkAvocadoDev",
        )
        about.add_credit_section("Vencord", ["Vendicated https://github.com/Vendicated"])
        about.present()
        log("About screen initialized")

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

def main(version):
    """The application's entry point."""
    log("START")
    app = VenpatchApplication()
    return app.run(sys.argv)
