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

from gi.repository import Adw, Gtk, GObject, Gdk, GLib

@Gtk.Template(resource_path='/io/github/pinkavocadodev/venpatch/window.ui')
class VenpatchWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'VenpatchWindow'

    usr_data_folder = subprocess.run("echo $HOME", shell = True,capture_output=True, text=True).stdout[:-1] + "/.var/app/io.github.pinkavocadodev.venpatch/data/"

    uninstall = Gtk.Template.Child("pillUninstall")
    repair = Gtk.Template.Child("pillRepair")
    install = Gtk.Template.Child("pillInstall")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_title("VenPatch")
        self.apply_css(self.repair, ".pillRepair{color:#000000; background-color:#ffa500;}")
        self.apply_css(self.install, ".suggested{color:#ffffff; background-color:#3584e4;}")
        self.apply_css(self.uninstall, ".destroy{color:#DD6D6A; background-color:#4B3234;}")
        self.repair.connect("clicked", self.on_click)
        self.install.connect("clicked", self.on_click)
        self.uninstall.connect("clicked", self.on_click)

    def apply_css(self, widget, css):
        provider = Gtk.CssProvider()
        provider.load_from_data(css.encode("utf-8"))

        context = widget.get_style_context()
        context.add_provider(provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def on_click(self, button):
        #Disable button
        self.set_sensitive(False)

        #Force sync execution of repair script
        while GLib.MainContext.default().pending():
           GLib.MainContext.default().iteration(True)

        match button.get_name():
           case "pillRepair":
               GLib.idle_add(self.run_repair)
           case "pillInstall":
               GLib.idle_add(self.run_install)
           case "pillUninstall":
               GLib.idle_add(self.run_uninstall)

        #Re-enable the button
        self.set_sensitive(True)

    #--------------------INSTALL BUTTON-------------------------
    def run_install(self):
        env = os.environ.copy()
        env["DISPLAY"] = ":0"
        process = subprocess.Popen(f"flatpak-spawn --host --env=SUDO_ASKPASS={self.usr_data_folder}askpass.sh sudo -A {self.usr_data_folder}./outfile --install", shell = True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, executable="/bin/bash", env=env)
        stdout, stderr = process.communicate(input='\n')
        print("STDOUT::",stdout)
    #-----------------------------------------------------------

    #--------------------REPAIR BUTTON--------------------------
    def run_repair(self):
        env = os.environ.copy()
        env["DISPLAY"] = ":0"
        process = subprocess.Popen(f"flatpak-spawn --host --env=SUDO_ASKPASS={self.usr_data_folder}askpass.sh sudo -A {self.usr_data_folder}./outfile --repair", shell = True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, executable="/bin/bash", env=env)
        stdout, stderr = process.communicate(input='\n')
        print("STDOUT::",stdout)
    #------------------------------------------------------------

    #--------------------UNINSTALL BUTTON--------------------------
    def run_uninstall(self):
        env = os.environ.copy()
        env["DISPLAY"] = ":0"
        process = subprocess.Popen(f"flatpak-spawn --host --env=SUDO_ASKPASS={self.usr_data_folder}askpass.sh sudo -A {self.usr_data_folder}./outfile --uninstall", shell = True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, executable="/bin/bash", env=env)
        stdout, stderr = process.communicate(input='\n')
        print("STDOUT::",stdout)
    #------------------------------------------------------------

