# shared.py
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

#Contains any shared functions between .py scripts

import json
import logging
import subprocess
import os

from gi.repository import Gtk, Adw, GObject

logging.basicConfig(level=logging.DEBUG)

def return_user_data_folder():
    usr_data_folder = subprocess.run("echo $HOME", shell = True,capture_output=True, text=True).stdout[:-1] + "/.var/app/io.github.pinkavocadodev.venpatch/data/"
    return usr_data_folder

usr_data_folder = return_user_data_folder()

def initial_setup():
    #DESCRIPTION: check if necessary files are present, if not, creates/downloads them
    #Generate config.json
    if not os.path.isfile(usr_data_folder + "config.json"):
        log("initial_setup(): Generating config.json <the settings have been reset!>")
        with open(usr_data_folder + "config.json", "w") as conf:
            conf.write('''\
{"discordPath": "default"}''')

    #Generate askpass.sh file
    if not os.path.isfile(usr_data_folder + "askpass.sh") :
        log("initial_setup(): Generating askpass.sh")
        with open(usr_data_folder + "askpass.sh", "w") as ask:
            ask.write('''\
#!/bin/bash
zenity --password --title "Sudo permission required"''')

    chmod_askpass = subprocess.run("chmod +x $HOME/.var/app/io.github.pinkavocadodev.venpatch/data/askpass.sh", shell = True,capture_output=True, text=True, executable="/bin/bash")

    #Generate install.sh script
    if not os.path.isfile(usr_data_folder + "install.sh") :
        log("initial_setup(): Generating install.sh")
        with open(usr_data_folder + "install.sh", 'w') as ins:
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
    if not os.path.isfile(usr_data_folder + "outfile") :
        log("initial_setup(): Downloading Outfile <Vencord installer binary>")
        venc_installer_run = subprocess.run("flatpak-spawn --host $HOME/.var/app/io.github.pinkavocadodev.venpatch/data/./install.sh", shell = True,capture_output=True, text=True, executable="/bin/bash")

def show_toast(win, message):
        toast = Adw.Toast.new(message)
        toast.set_timeout(5)
        win.toast_overlay.add_toast(toast)

def apply_css(widget, css):
        provider = Gtk.CssProvider()
        provider.load_from_data(css.encode("utf-8"))

        context = widget.get_style_context()
        context.add_provider(provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

def read_conf():
    if not is_conf_available():
        initial_setup()
    config = open(usr_data_folder + "config.json")
    jsonParsed = json.load(config)
    return jsonParsed["discordPath"]

def set_conf(conf):
    if not is_conf_available():
        initial_setup()
    jsonConf = {"discordPath" : conf}
    with open(usr_data_folder + "config.json", "w") as conf:
            conf.write(json.dumps(jsonConf))

def is_conf_available():
    if os.path.isfile(usr_data_folder + "config.json"):
        return True
    return False

def log(message):
    logging.debug(message)
