"""
GUI of rtmom

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

ACTIONS = {"1completed": "Mark Selected Task Completed", "0details": "Show Task Details", "8update": "Update tasks from net", "9about":"About rtmom"}
"""ACTIONS for Event Handlers; numbers indicating the order they do appear in the action drop down"""

import ecore, elementary
import rtmom
import rtmom_fs
import rtmom_net
from gui.aboutdialog import AboutDialog
from gui.detaildialog import DetailDialog

class RTMOMPage(object):
    """
    App page
    """

    def _initDropdownBar(self, mainbox):
        """
        Set up a drop down list for available categories (task lists)
        """
        frame_cats = elementary.Frame(self.main.win)
        frame_cats.label_set("Choose Category")
        frame_cats.size_hint_align_set(-1, -1)
        mainbox.pack_end(frame_cats)
        frame_cats.show()

        box_cats = elementary.Box(self.main.win)
        frame_cats.content_set(box_cats)
        box_cats.show()

        self.hs_cat = elementary.Hoversel(self.main.win)
        self.hs_cat.hover_parent_set(mainbox)
        self.hs_cat.scale_set(1)
        self.hs_cat.size_hint_align_set(-1.0, 0.0)
        box_cats.pack_end(self.hs_cat)
        self.hs_cat.show()

        for i in self._myrtmom.getCategories():
            self.hs_cat.item_add(i, '',  elementary.ELM_ICON_NONE, self._toolbarCallback, i)
        

    def _initContent(self, mainbox):
        """
        Create content area of base window
        """
        scroller = elementary.Scroller(self.main.win)
        scroller.bounce_set(False, True)
        scroller.size_hint_weight_set(1.0, 1.0)
        scroller.size_hint_align_set(-1.0, -1.0)
        mainbox.pack_end(scroller)
        scroller.show()        

        contentBox = elementary.Box(self.main.win)
        contentBox.size_hint_weight_set(1.0, -1.0)
        scroller.content_set(contentBox)
        contentBox.show()
        
        self.list = elementary.List(self.main.win)
        self.list.size_hint_weight_set(1.0, 1.0)
        self.list.size_hint_align_set(-1.0, -1.0)
        contentBox.pack_end(self.list)
        self.list.show()
        
    def _initActionsDropdown(self, mainbox, buttonBox):
        """
        Drop down list for actions in the bottom of main page (wouldn't fit if realized as buttons)
        """
        self.hs_actions = elementary.Hoversel(self.main.win)
        self.hs_actions.hover_parent_set(mainbox)
        self.hs_actions.scale_set(1)
        self.hs_actions.size_hint_weight_set(10, 0)
        self.hs_actions.size_hint_align_set(-1.0, 0.0)
        buttonBox.pack_end(self.hs_actions)
        self.hs_actions.show()

        for key in sorted(ACTIONS.keys()):
            label = ACTIONS[key]
            self.hs_actions.item_add(label, '',  elementary.ELM_ICON_NONE, self._actionsCallback, key)
        self.hs_actions.label_set('Actions...')

    def _initButtons(self, mainbox):
        """
        Create button wigdets in buttom of base window
        """
        box_btns = elementary.Box(self.main.win)
        box_btns.horizontal_set(True)
        box_btns.homogenous_set(False)
        box_btns.size_hint_align_set(-1.0, 0)
        mainbox.pack_end(box_btns)
        box_btns.show()

        dropDown = self._initActionsDropdown(mainbox, box_btns)

        btn_quit = elementary.Button(mainbox)
        btn_quit._callback_add('clicked', self.main.destroy)
        btn_quit.label_set(("Quit"))
        btn_quit.size_hint_weight_set(-1, 0)
        btn_quit.size_hint_align_set(-1, 0)        
        box_btns.pack_end(btn_quit)
        btn_quit.show()

    def __init__(self, main):
        """
        Initialize app page
        
        Data is attempted to load from cache (local file); if this fails, attempts it made to load from the net.
        """
        self.main = main
        self._listMapping = {}
        
        self._myrtmom = rtmom.RTMOM()
        self._fileHandler = rtmom_fs.FileHandler()
        try:
            self._myrtmom.doLoadFromFile(self._fileHandler)
        except:
            # Fine - this is our very first run; but now we direct connection to RTM
            print "Error when loading from cache ... trying direct pull from Internet"
            netConnector = rtmom_net.getInternetConnector()
            if not netConnector.isConnected():
                netConnector.connect()
            self._myrtmom.updateFromNet(netConnector)
            self._myrtmom.doSaveToFile(self._fileHandler)
        
        mainbox = elementary.Box(self.main.win)
        mainbox.size_hint_weight_set(-1.0, -1.0)
        mainbox.show()
        self._mainbox = mainbox

        self._initDropdownBar(self._mainbox)
        self._initContent(self._mainbox)
        self._initButtons(self._mainbox)

        self.main.pager.content_push(self._mainbox)
        
        self.hs_cat.label_set(self._myrtmom.getCategories()[0])
        self._updateList(self._myrtmom.getCategories()[0])

    def promote(self):
        """
        Bring myself to front
        """
        self.main.pager.content_promote(self._mainbox)


    def _updateList(self, category = None, filter = ""):
        """
        Clears the list widget and populates new entries from category in parameter
        """
        self.list.clear()
        self._listMapping  = {}

        for task in self._myrtmom.getFullTasks(category):
            c = '%s<br><b>%s</>' % (
                                                rtmom.getExtractor().replaceCharactersBefore(task.name, 40), 
                                                rtmom.getExtractor().replaceCharactersBefore(rtmom.getExtractor().extractTags(task), 30))
            label = elementary.Label(self._mainbox)
            label.scale_set(1)
            label.label_set(c)
            item = self.list.item_append('', label, None, None, None)
            self._listMapping[item] = task
            self.list.go()            

# EVENTS
    def _toolbarCallback(self, *args):
        """
        Event Handler for any selection made in the toolbar
        """
        x,  y, entry = args
        self.hs_cat.label_set(entry)
        print ("Selected category: %s" %(entry))
        self._updateList(entry)

    def _actionsCallback(self, *args):
        """
        Event handler for the drop down list for actions
        """
        x, y, action = args
        print ("Action: %s" %(action))
        if action == '8update':
            netConnector = rtmom_net.getInternetConnector()
            if not netConnector.isConnected():
                netConnector.connect()
            self._myrtmom.updateFromNet(netConnector)
            self._myrtmom.doSaveToFile(self._fileHandler)
            self._updateList(self.hs_cat.label_get())
        elif action == "0details":
            item = self.list.selected_item_get()
            fullTask = self._listMapping[item]
            a= DetailDialog(self.main, fullTask)
            a.promote()
        elif action == "9about":
            a = AboutDialog(self.main)
            a.promote()

class MainWindow:
    """
    Base Window
    """
    
    def destroy(self, obj, *args, **kargs):
        """
        Close down elementary
        """
        elementary.exit()        
        
    def __init__(self):
        """
        Set up Frame and initialize Pager with app page
        """
        self.win = elementary.Window("rtmom", elementary.ELM_WIN_BASIC)
        self.win.title_set(("rtmom"))
        self.win.callback_destroy_add(self.destroy)

        bg = elementary.Background(self.win)
        self.win.resize_object_add(bg)
        bg.size_hint_weight_set(1.0, 1.0)
        bg.size_hint_min_set(200,300)
        bg.show()

        self.pager = elementary.Pager(self.win)
        self.pager.size_hint_weight_set(1.0, 1.0)
        self.win.resize_object_add(self.pager)
        self.pager.show()

        self.rtmom_page = RTMOMPage(self)

        self.win.resize(480, 640)
        self.win.show()
        self.rtmom_page.promote()


def initAndRun():
    """
    start up gui
    """
    elementary.init()
    MainWindow()
    elementary.run()
    elementary.shutdown()
