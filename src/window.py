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

from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import Gdk

@Gtk.Template(resource_path='/io/github/pinkavocadodev/venpatch/window.ui')
class VenpatchWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'VenpatchWindow'

    #label = Gtk.Template.Child()
    repair = Gtk.Template.Child("pillRepair")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.apply_css(self.repair, ".pillRepair{color:#000000; background-color:#ffa500;}")

    def apply_css(self, widget, css):
        provider = Gtk.CssProvider()
        provider.load_from_data(css.encode("utf-8"))

        context = widget.get_style_context()
        context.add_provider(provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
