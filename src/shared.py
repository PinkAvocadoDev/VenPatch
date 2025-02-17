# shared.py
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

#Contains any shared functions between .py scripts

import os
import subprocess

def initial_setup():
    #DESCRIPTION: check if necessary files are present, if not, creates/downloads them
    #Generate askpass.sh file
    if not os.path.isfile(return_user_data_folder() + "askpass.sh") :
        print("Generating askpass.sh")
        with open(return_user_data_folder() + "askpass.sh", "w") as ask:
            ask.write('''\
#!/bin/bash
zenity --password --title "Sudo permission required"''')

    chmod_askpass = subprocess.run("chmod +x $HOME/.var/app/io.github.pinkavocadodev.venpatch/data/askpass.sh", shell = True,capture_output=True, text=True, executable="/bin/bash")

    #Generate install.sh script
    if not os.path.isfile(return_user_data_folder() + "install.sh") :
        print("Generating install.sh")
        with open(return_user_data_folder() + "install.sh", 'w') as ins:
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
    if not os.path.isfile(return_user_data_folder() + "outfile") :
        print("DEBUG: Downloading Outfile")
        venc_installer_run = subprocess.run("flatpak-spawn --host $HOME/.var/app/io.github.pinkavocadodev.venpatch/data/./install.sh", shell = True,capture_output=True, text=True, executable="/bin/bash")

def return_user_data_folder():
    usr_data_folder = subprocess.run("echo $HOME", shell = True,capture_output=True, text=True).stdout[:-1] + "/.var/app/io.github.pinkavocadodev.venpatch/data/"
    return usr_data_folder
