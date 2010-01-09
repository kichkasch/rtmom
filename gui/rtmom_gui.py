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
import ecore, elementary
import rtmom
import rtmom_fs
import rtmom_net

class MainWindow:
    """
    Base Window
    """
    
    def destroy(self, obj, *args, **kargs):
        """
        Close down elementary
        """
        elementary.exit()

    def _initDropdownBar(self, mainbox):
        frame_cats = elementary.Frame(mainbox)
        frame_cats.label_set("Choose Category")
        frame_cats.size_hint_align_set(-1, -1)
        mainbox.pack_end(frame_cats)
        frame_cats.show()

        box_cats = elementary.Box(mainbox)
        frame_cats.content_set(box_cats)
        box_cats.show()

        self.hs_cat = elementary.Hoversel(mainbox)
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
        scroller = elementary.Scroller(mainbox)
        scroller.bounce_set(True, True)
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
        """
        Create button wigdets in buttom of base window
        """
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
        btn_update.callback_clicked_add(self._btnUpdateCallback)
        box_btns.pack_end(btn_update)
        btn_update.show()

        btn_quit = elementary.Button(mainbox)
        btn_quit._callback_add('clicked', self.destroy)
        btn_quit.label_set(("Quit"))
        btn_quit.size_hint_weight_set(1, 0)
        btn_quit.size_hint_align_set(-1, 0)        
        box_btns.pack_end(btn_quit)
        btn_quit.show()
        
        
    def __init__(self):
        """
        Initialize base window
        
        Data is attempted to load from cache (local file); if this fails, attempts it made to load from the net.
        """
        self._myrtmom = rtmom.RTMOM()
        self._fileHandler = rtmom_fs.FileHandler()
        try:
            self._myrtmom.doLoadFromFile(self._fileHandler)
        except:
            # Fine - this is our very first run; but now we direct connection to RTM
            print "Error when loading from cache ... trying direct pull from Internet"
            netConnector = rtmom_net.getInternetConnector()
            if not netConnector.isConnected():
                netConnector.connect(tokenCallback = None)
            self._myrtmom.updateFromNet(netConnector)
            self._myrtmom.doSaveToFile(self._fileHandler)
        
        self.win = elementary.Window("rtmom", elementary.ELM_WIN_BASIC)
        self.win.title_set(("rtmom"))
        self.win.callback_destroy_add(self.destroy)

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

        self._initDropdownBar(mainbox)
        self._initContent(mainbox)
        self._initButtons(mainbox)
        self.win.show()
        
        self.hs_cat.label_set(self._myrtmom.getCategories()[0])
        self._updateList(self._myrtmom.getCategories()[0])

    def _updateList(self, category = None, filter = ""):
        """
        Clears the list widget and populates new entries from category in parameter
        """
        self.list.clear()
        for task in self._myrtmom.getTasks(category):
            label = elementary.Label(self._mainbox)
            label.scale_set(1)
            label.label_set('%s' % task)
            self.list.item_append(task, label, None, None, None)
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

    def _btnUpdateCallback(self, *args):
        """
        Event handler for button 'update'
        
        Initiates a pull of information from the net in the backend.
        """
        netConnector = rtmom_net.getInternetConnector()
        if not netConnector.isConnected():
            netConnector.connect(tokenCallback = None)
        self._myrtmom.updateFromNet(netConnector)
        self._myrtmom.doSaveToFile(self._fileHandler)
        self._updateList(self.hs_cat.label_get())


def initAndRun():
    """
    start up gui
    """
    elementary.init()
    MainWindow()
    elementary.run()
    elementary.shutdown()
