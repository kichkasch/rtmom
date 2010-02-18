"""
Confirm Authorization Dialog for rtmom

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
import ecore, elementary
import rtmom_net

class AuthorizedDialog(object):
    def __init__(self, main, gui, url):
        self.main = main
        self.gui = gui
        self.box = elementary.Box(self.main.win)
        self.box.size_hint_align_set(-1, -1)
        self.box.show()

        label = elementary.Label(self.main.win)
        label.label_set('<b>%s</>' % ("Authorization"))
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
<b>rtmom</>

Authorization required. Please give me access.

<b>Authorization URL:</> """ + url + """

And click button ones you authorized me.
"""

        entry = elementary.Entry(self.main.win)
        entry.editable_set(False)
        entry.line_wrap_set(True)
        entry.size_hint_align_set(-1, -1)
        entry.entry_set(about.replace('\n', '<br>'))
        box.pack_end(entry)
        entry.show()

        quitbt2 = elementary.Button(self.main.win)
        quitbt2._callback_add('clicked', self.callbackFinished)
        quitbt2.label_set("Authorization finished")
        quitbt2.size_hint_align_set(-1.0, 0.0)
        quitbt2.show()
        self.box.pack_end(quitbt2)
        
        print url
        self.main.pager.content_push(self.box)

        
    def promote(self):
        """
        Part of pager - just tell the main window, it shall promote me now
        """
        self.main.pager.content_promote(self.box)

    def callbackFinished(self, *args):
        """
        Promote application page
        """
        self.gui.returnFromInitialAuthorization()
#        self.main.rtmom_page.promote()
