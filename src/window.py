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

import webbrowser

from gi.repository import Adw, Gtk, GLib
from .shared import *
from subprocess import Popen
from os import environ

@Gtk.Template(resource_path='/io/github/pinkavocadodev/venpatch/window.ui')
class VenpatchWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'VenpatchWindow'

    main_box = Gtk.Template.Child("main-box")

    toast_overlay = Gtk.Template.Child("toastOverlay")

    uninstall = Gtk.Template.Child("pillUninstall")
    repair = Gtk.Template.Child("pillRepair")
    install = Gtk.Template.Child("pillInstall")

    usr_data_folder = return_user_data_folder()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_title("VenPatch")
        apply_css(self.repair, ".pillRepair{color:#000000; background-color:#ffa500;}")
        apply_css(self.install, ".suggested{color:#ffffff; background-color:#3584e4;}")
        apply_css(self.uninstall, ".destroy{color:#DD6D6A; background-color:#4B3234;}")
        self.repair.connect("clicked", self.on_click)
        self.install.connect("clicked", self.on_click)
        self.uninstall.connect("clicked", self.on_click)
        log("Main window initialized")
        log(read_conf())

    def on_preferences_action(self, widget, _):
        """Callback for the app.preferences action."""
        dialog = PreferencesDialog(self)
        dialog.present()

    def on_click(self, button):
        #Disable button
        self.set_sensitive(False)
        #Ensure data exists
        GLib.idle_add(initial_setup)
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
        log("on_click(): "+button.get_name())

    #--------------------INSTALL BUTTON-------------------------
    def run_install(self):
        env = os.environ.copy()
        env["DISPLAY"] = ":0"
        process = subprocess.Popen(f"flatpak-spawn --host --env=SUDO_ASKPASS={self.usr_data_folder}askpass.sh sudo -A {self.usr_data_folder}./outfile --install", shell = True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, executable="/bin/bash", env=env)
        if read_conf() == "default":
            stdout, stderr = process.communicate(input='\n')
        else:
            stdout, stderr = process.communicate(input='\x1b[B\n'+read_conf()+'\n')
        exit_code = process.returncode
        if exit_code == 0:
            show_toast(self, "Success!")
        else:
            show_toast(self, "Error!")

        log("run_install, exit code: "+str(exit_code))
    #-----------------------------------------------------------

    #--------------------REPAIR BUTTON--------------------------
    def run_repair(self):
        env = os.environ.copy()
        env["DISPLAY"] = ":0"
        process = subprocess.Popen(f"flatpak-spawn --host --env=SUDO_ASKPASS={self.usr_data_folder}askpass.sh sudo -A {self.usr_data_folder}./outfile --repair", shell = True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, executable="/bin/bash", env=env)
        if read_conf() == "default":
            stdout, stderr = process.communicate(input='\n')
        else:
            stdout, stderr = process.communicate(input='\x1b[B\n'+read_conf()+'\n')
        exit_code = process.returncode
        if exit_code == 0:
            show_toast(self, "Success!")
        else:
            show_toast(self, "Error!")

        log("run_repair, exit code: "+str(exit_code))
    #------------------------------------------------------------

    #--------------------UNINSTALL BUTTON--------------------------
    def run_uninstall(self):
        env = os.environ.copy()
        env["DISPLAY"] = ":0"
        process = subprocess.Popen(f"flatpak-spawn --host --env=SUDO_ASKPASS={self.usr_data_folder}askpass.sh sudo -A {self.usr_data_folder}./outfile --uninstall", shell = True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, executable="/bin/bash", env=env)
        if read_conf() == "default":
            stdout, stderr = process.communicate(input='\n')
        else:
            stdout, stderr = process.communicate(input='\x1b[B\n'+read_conf()+'\n')
        exit_code = process.returncode
        if exit_code == 0:
            show_toast(self, "Success!")
        else:
            show_toast(self, "Error!")

        log("run_uninstall, exit code: "+str(exit_code))
    #------------------------------------------------------------

class PreferencesDialog(Adw.PreferencesWindow):
    usr_data_folder = return_user_data_folder()

    toast_overlay = Adw.ToastOverlay()

    save_config_btn = Adw.ButtonRow()
    def __init__(self, parent):
        super().__init__()
        self.set_title("Preferences")
        self.set_transient_for(parent)
        self.set_default_size(300, 400)
        self.set_resizable(False)

        page = Adw.PreferencesPage()
        group1 = Adw.PreferencesGroup(title="Vencord")
        self.group2 = Adw.PreferencesGroup(title="General settings")

        updateVencord = Adw.ButtonRow()
        updateVencord.set_name("updateVencord")
        updateVencord.set_title("Update Vencord Installer binary")
        updateVencord.connect("activated", self.on_click)
        updateVencord.get_style_context().add_class("updateVencord")

        self.config_entry_row = Adw.EntryRow()
        self.config_entry_row.set_title("Custom Discord Path")

        is_custom_path = Adw.SwitchRow()
        is_custom_path.set_title("Use custom path for Discord")
        switch = is_custom_path.get_activatable_widget()
        switch.connect("notify::active", self.on_switch_toggled)

        self.save_config_btn = Adw.ButtonRow()
        self.save_config_btn.set_name("saveConfig")
        self.save_config_btn.set_title("Save Path")
        self.save_config_btn.connect("activated", self.on_click)

        updateVenPatch = Adw.ButtonRow()
        updateVenPatch.set_title("Check for updates for VenPatch")
        updateVenPatch.connect("activated", self.on_click)
        updateVenPatch.get_style_context().add_class("updateVenPatch")

        apply_css(updateVencord, ".updateVencord{background-color:#613583;color:#dc8add;}")
        apply_css(updateVenPatch, ".updateVenPatch{background-color:#613583;color:#dc8add;}")
        group1.add(updateVencord)
        self.group2.add(updateVenPatch)
        self.group2.add(is_custom_path)
        page.add(self.group2)
        page.add(group1)

        is_default = True
        if read_conf() != "default":
            is_default = False
            self.config_entry_row.set_text(read_conf())

        is_custom_path.set_active(not is_default)
        self.normalize_toggle(is_custom_path.get_active())

        # Add the toast overlay to the window
        group1.add(self.toast_overlay)
        self.add(page)
        log("PreferencesDialog initialized")

    def normalize_toggle(self, state):
        if state:
            self.group2.add(self.config_entry_row)
            self.group2.add(self.save_config_btn)
        else:
            set_conf("default")
            self.group2.remove(self.config_entry_row)
            self.group2.remove(self.save_config_btn)

    def on_switch_toggled(self, switch, param):
        state = switch.get_active()
        self.normalize_toggle(state)

    def on_click(self, button):
        #Force async execution of script
        while GLib.MainContext.default().pending():
           GLib.MainContext.default().iteration(True)

        match button.get_name():
           case "updateVencord":
               self.set_sensitive(False)
               GLib.idle_add(initial_setup)
               GLib.idle_add(self.run_update)
               self.set_sensitive(True)
               show_toast(self, "Done!")
           case "updateVenPatch":
               self.run_redirect()
           case "saveConfig":
               set_conf(self.config_entry_row.get_text())
               log("Set new path: "+self.config_entry_row.get_text())

    def run_redirect(self):
        webbrowser.open("https://github.com/PinkAvocadoDev/VenPatch/releases/latest")
        log("run_redirect()")

    def run_update(self):
        delete = subprocess.Popen(f"rm {self.usr_data_folder}outfile", shell = True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, executable="/bin/bash")
        initial_setup()
        log("run_update()")


