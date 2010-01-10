"""
About Dialog for rtmom

Elementary based client for "Remember the Milk" (http://www.rememberthemilk.com/) written in Python. 

Copyright (C) 2010 Michael Pilgermann <kichkasch@gmx.de>
http://github.com/kichkasch/rtmom

rtmom is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

rtmom is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with rtmom.  If not, see <http://www.gnu.org/licenses/>.
"""
from config import *
import ecore, elementary

class AboutDialog(object):
    def __init__(self, main):
        self.main = main
        self.box = elementary.Box(self.main.win)
        self.box.size_hint_align_set(-1, -1)
        self.box.show()

        label = elementary.Label(self.main.win)
        label.label_set('<b>%s %s</>' % (APP_NAME, APP_VERSION))
        label.size_hint_align_set(0.5, 0.5)
        self.box.pack_end(label)
        label.show()

        scroller = elementary.Scroller(self.main.win)
        scroller.bounce_set(False, True)
        scroller.size_hint_weight_set(1.0, 1.0)
        scroller.size_hint_align_set(-1.0, -1.0)
        self.box.pack_end(scroller)
        scroller.show()

        box = elementary.Box(self.main.win)
        box.size_hint_weight_set(1, 1)
        scroller.content_set(box)
        box.show()

        about  = """\
<b>rtmom</> Elementary based client for "Remember the Milk" (http://www.rememberthemilk.com/) written in Python.

<b>Copyright</> 2010 Michael Pilgermann

<b>Licensed</> under the GNU GPL v3

<b>Homepage</> http://freshmeat.net/projects/rtmom

"""

        entry = elementary.Entry(self.main.win)
        entry.editable_set(False)
        entry.line_wrap_set(True)
        entry.size_hint_align_set(-1, -1)
        entry.entry_set(about.replace('\n', '<br>'))
        box.pack_end(entry)
        entry.show()

        quitbt2 = elementary.Button(self.main.win)
        quitbt2._callback_add('clicked', self.callbackQuit)
        quitbt2.label_set("Close")
        quitbt2.size_hint_align_set(-1.0, 0.0)
        quitbt2.show()
        box.pack_end(quitbt2)

        self.main.pager.content_push(self.box)

        
    def promote(self):
        """
        Part of pager - just tell the main window, it shall promote me now
        """
        self.main.pager.content_promote(self.box)

    def callbackQuit(self, *args):
        """
        Promote application page
        """
        self.main.rtmom_page.promote()
        
