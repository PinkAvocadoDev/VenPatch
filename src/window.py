# window.py
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
import subprocess
import os

from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib

@Gtk.Template(resource_path='/io/github/pinkavocadodev/venpatch/window.ui')
class VenpatchWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'VenpatchWindow'

    usr_data_folder = subprocess.run("echo $HOME", shell = True,capture_output=True, text=True).stdout[:-1] + "/.var/app/io.github.pinkavocadodev.venpatch/data/"
    #label = Gtk.Template.Child()
    repair = Gtk.Template.Child("pillRepair")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.apply_css(self.repair, ".pillRepair{color:#000000; background-color:#ffa500;}")
        self.repair.connect("clicked", self.on_repair)
        self.initial_setup()

    def initial_setup(self):
        #Generate askpass.sh file
        with open(self.usr_data_folder + "askpass.sh", "w") as ask:
            ask.write('''\
#!/bin/bash
zenity --password --title "Sudo permission required"''')

        chmod_askpass = subprocess.run("chmod +x $HOME/.var/app/io.github.pinkavocadodev.venpatch/data/askpass.sh", shell = True,capture_output=True, text=True, executable="/bin/bash")

        #Generate install.sh script
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

        if not os.path.isfile(self.usr_data_folder + "outfile") :
            print("Downloading")
            venc_installer_run = subprocess.run("flatpak-spawn --host $HOME/.var/app/io.github.pinkavocadodev.venpatch/data/./install.sh", shell = True,capture_output=True, text=True, executable="/bin/bash")

    def apply_css(self, widget, css):
        provider = Gtk.CssProvider()
        provider.load_from_data(css.encode("utf-8"))

        context = widget.get_style_context()
        context.add_provider(provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def on_repair(self, button):
        #Disable button
        self.repair.set_sensitive(False)

        while GLib.MainContext.default().pending():
            GLib.MainContext.default().iteration(True)
        GLib.idle_add(self.run_repair)

        #re-enable button
        self.repair.set_sensitive(True)

    def run_repair(self):
        env = os.environ.copy()
        env["DISPLAY"] = ":0"
        process = subprocess.Popen(f"flatpak-spawn --host --env=SUDO_ASKPASS=$HOME/.var/app/io.github.pinkavocadodev.venpatch/data/askpass.sh sudo -A $HOME/.var/app/io.github.pinkavocadodev.venpatch/data/./outfile --repair", shell = True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, executable="/bin/bash", env=env)
        stdout, stderr = process.communicate(input='\n')
        print("STDOUT::",stdout)

