"""
Details Dialog for rtmom

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
import rtmom

class DetailDialog(object):
    """
    Implementation of dialog for displaying details for a single task
    """
    def __init__(self, main, task):
        self.main = main
        self.box = elementary.Box(self.main.win)
        self.box.size_hint_align_set(-1, -1)
        self.box.show()

        label = elementary.Label(self.main.win)
        label.label_set('<b>task details</>')
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

        about  = """<i>""" + rtmom.getExtractor().replaceCharactersBefore(task.name) + """</>

<b>Due:</> """ + rtmom.getExtractor().replaceCharactersBefore(task.task.due) + """
<b>Time estimate:</> """ + rtmom.getExtractor().replaceCharactersBefore(task.task.estimate) + """
<b>Tags:</> """ + rtmom.getExtractor().replaceCharactersBefore(rtmom.getExtractor().extractTags(task)) + """
<b>URL:</> """ + rtmom.getExtractor().replaceCharactersBefore(task.url) + """
<b>Notes:</>"""

        entry = elementary.Entry(self.main.win)
        entry.editable_set(False)
        entry.line_wrap_set(True)
        entry.size_hint_align_set(-1, -1)
        entry.entry_set(rtmom.getExtractor().replaceCharactersAfter(about))
        box.pack_end(entry)
        entry.show()

        notesList = []
        if not isinstance(task.notes, list):    # no note at all
            if isinstance(task.notes.note, list):
                for noteEntry in task.notes.note:              
                    notesList.append(noteEntry)                    
            else:
                notesList.append(task.notes.note)
                
        for note in notesList:
            about = rtmom.getExtractor().formatNote(note)
            frame_cats = elementary.Frame(self.main.win)
            frame_cats.label_set(note.created)
            frame_cats.size_hint_align_set(-1, -1)
            box.pack_end(frame_cats)
            frame_cats.show()

            box_cats = elementary.Box(self.main.win)
            frame_cats.content_set(box_cats)
            box_cats.show()
            
            entry = elementary.Entry(self.main.win)
            entry.editable_set(False)
            entry.line_wrap_set(True)
            entry.size_hint_align_set(-1, -1)
            entry.entry_set(about)
            box_cats.pack_end(entry)
            entry.show()            
            

        box_btns = elementary.Box(self.main.win)
        box_btns.horizontal_set(True)
        box_btns.homogenous_set(True)
        box_btns.size_hint_align_set(-1.0, 0)
        self.box.pack_end(box_btns)
        box_btns.show()
        
        btn_completed = elementary.Button(self.main.win)
        btn_completed.label_set('Mark Completed')
        btn_completed.size_hint_weight_set(1, 0)
        btn_completed.size_hint_align_set(-1, 0)
# btn_light.callback_clicked_add(self.main.show_light_page)
        box_btns.pack_end(btn_completed)
        btn_completed.show()
        
        quitbt2 = elementary.Button(self.main.win)
        quitbt2._callback_add('clicked', self.callbackQuit)
        quitbt2.label_set("Close")
        quitbt2.size_hint_weight_set(1, 0)
        quitbt2.size_hint_align_set(-1.0, 0.0)
        quitbt2.show()
        box_btns.pack_end(quitbt2)

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
        
