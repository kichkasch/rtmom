"""
Main module for GUI of rtmom

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
import ecore, elementary    # , evas
import rtmom

class MainWindow:

    def destroy(self, obj, *args, **kargs):
        elementary.exit()

    def _initToolbar(self, mainbox):
        toolbar = elementary.Toolbar(mainbox)
        toolbar.size_hint_align_set(-1.0, 0)
        mainbox.pack_end(toolbar)
        toolbar.show()
        self.toolbar_items = []
        for i in rtmom.getCategories(self._connection):
            icon = None
            self.toolbar_items.append(toolbar.item_add(icon, i, self._toolbarCallback))
#        self.toolbar_items[0].select()

    def _initContent(self, mainbox):
        scroller = elementary.Scroller(mainbox)
        scroller.bounce_set(0, 0)
        scroller.size_hint_weight_set(1.0, 1.0)
        scroller.size_hint_align_set(-1.0, -1.0)
        mainbox.pack_end(scroller)
        scroller.show()        

        contentBox = elementary.Box(mainbox)
        contentBox.size_hint_weight_set(1.0, -1.0)
        scroller.content_set(contentBox)
        contentBox.show()
        
        self.list = elementary.List(mainbox)
        self.list.size_hint_weight_set(1.0, 1.0)
        self.list.size_hint_align_set(-1.0, -1.0)
        contentBox.pack_end(self.list)
        self.list.show()
        

    def _initButtons(self, mainbox):
        box_btns = elementary.Box(mainbox)
        box_btns.horizontal_set(True)
        box_btns.homogenous_set(True)
        box_btns.size_hint_align_set(-1.0, 0)
        mainbox.pack_end(box_btns)
        box_btns.show()

        btn_completed = elementary.Button(mainbox)
        btn_completed.label_set('Completed')
        btn_completed.size_hint_weight_set(1, 0)
        btn_completed.size_hint_align_set(-1, 0)
#        btn_light.callback_clicked_add(self.main.show_light_page)
        box_btns.pack_end(btn_completed)
        btn_completed.show()

        btn_details = elementary.Button(mainbox)
        btn_details.label_set('Details')
        btn_details.size_hint_weight_set(1, 0)
        btn_details.size_hint_align_set(-1, 0)
#        btn_details.callback_clicked_add(self.main.show_about_page)
        box_btns.pack_end(btn_details)
        btn_details.show()

        btn_update = elementary.Button(mainbox)
        btn_update.label_set('Update')
        btn_update.size_hint_weight_set(1, 0)
        btn_update.size_hint_align_set(-1, 0)
#        btn_details.callback_clicked_add(self.main.show_about_page)
        box_btns.pack_end(btn_update)
        btn_update.show()

        btn_quit = elementary.Button(mainbox)
        btn_quit._callback_add('clicked', self.destroy)
        btn_quit.label_set(("Quit"))
        btn_quit.size_hint_weight_set(1, 0)
        btn_quit.size_hint_align_set(-1, 0)        
        box_btns.pack_end(btn_quit)
        btn_quit.show()
        
        
    def __init__(self, connection):
        self._connection = connection
        
        self.win = elementary.Window("rtmom", elementary.ELM_WIN_BASIC)
        self.win.title_set(("rtmom"))
        self.win.callback_destroy_add(self.destroy)

        #add background to main window
        bg = elementary.Background(self.win)
        self.win.resize_object_add(bg)
        bg.size_hint_weight_set(1.0, 1.0)
        bg.size_hint_min_set(200,300)
        bg.show()

        mainbox = elementary.Box(self.win)
        mainbox.size_hint_weight_set(1.0, 1.0)
        self.win.resize_object_add(mainbox)
        mainbox.show()
        self._mainbox = mainbox

        self._initToolbar(mainbox)
        self._initContent(mainbox)
        self._initButtons(mainbox)
        self.win.show()
        
        self.toolbar_items[0].select()        
#        self._updateList(rtmom.getCategories(self._connection)[0])


    def _updateList(self, category = None, filter = ""):
        self.list.clear()
        for task in rtmom.getTasks(self._connection, category, filter):
            label = elementary.Label(self._mainbox)
            label.scale_set(1)
            label.label_set('%s' % task)
            self.list.item_append(task, label, None, None, None)
            self.list.go()
        
# EVENTS
    def _toolbarCallback(self, *args):
        toolbar, entry = args
        index = self.toolbar_items.index(entry)
        print ("Selected category: %s" %(rtmom.getCategories(self._connection)[index]))
        self._updateList(rtmom.getCategories(self._connection)[index])

def getConnection():
    """
    Todo: Implement gui based dialog here
    """
    return rtmom.getConnection()

def initAndRun():
    conn = getConnection()
    elementary.init()
    MainWindow(conn)
    elementary.run()
    elementary.shutdown()
