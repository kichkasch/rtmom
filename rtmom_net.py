"""
RTM Service access (updates from / to Internet)

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

import config
import rtm
import datetime
import rtmom
import os
import os.path

internetConnector = None
"""Singleton"""
def getInternetConnector():
    """
    Singleton
    """
    global internetConnector
    if not internetConnector:
        internetConnector = InternetConnector()
    return internetConnector


class InternetConnector():
    """
    Implementation for RTM Internet Connector
    """
    
    def __init__(self):
        """
        Initialize 'empty' connection; YOU have to connect manually!
        """
        self._connection = None
        
    def isConnected(self):
        """
        Check, whether connection has been established
        """
        return self._connection != None
        
    def loadCategories(self):
        """
        Loads categories (task lists) from the net
        
        Returns a dictionary containing the names (key) and IDs (value) for the categories.
        """
        if not self.isConnected():
            raise ValueError('Not connected with RTM Net Service; cannot proceed. Please connect first.')
        categories = {}
        rspLists = self._connection.lists.getList()
        for cat in rspLists.lists.list:
            try:
                config.hidden_goups.index(cat.name)
            except:
                categories[cat.name] = cat.id
        return categories

    def _assembleFilter(self, filter):
        """
        Add components to an existing filter for additionally filtering completed tasks
        
        Depends on setting in config file.
        """
        if not config.show_completed:
            if filter:
                filter = "(" + filter + ") AND " + "status:incomplete"
            else:
                filter = "status:incomplete"
        return filter


    def loadFullTasks(self, catid = None, filter = ""):
        """
        Loads all tasks for the given category from the net
        
        The entire task instance will be returned. Extract the required information yourself!
        """
        if not self.isConnected():
            raise ValueError('Not connected with RTM Net Service; cannot proceed. Please connect first.')
        filter = self._assembleFilter(filter)
        if catid:
            rspTasks = self._connection.tasks.getList(list_id = catid,  filter = filter)
        else:
            rspTasks = self._connection.tasks.getList(filter = filter)
        return rtmom.getExtractor().extractTasksFromDottedDict(rspTasks.tasks)

    def markTaskCompleted(self, catId, task):
        """
        Mark a single task completed
        """
        if not self.isConnected():
            raise ValueError('Not connected with RTM Net Service; cannot proceed. Please connect first.')
        
        tl = self._connection.timelines.create().timeline
        rspTasks = self._connection.tasks.complete(list_id =catId, task_id = task.task.id, timeline = tl, taskseries_id = task.id)
        

    def connect(self, tokenPath = None):
        """
        Estabilshes connection with Remember The Milk backend
        
        Checks, whether token is known already; otherwise user interaction; finally connection
        """
        if not tokenPath:
            tokenPath = config.TOKEN_PATH
        token = None
        try:
            f = open(tokenPath, 'r')
            token = f.read().strip()
            f.close()
        except:
            token = None
        conn = rtm.RTM(config.api_key, config.shared_secret, token)
        if not token:
            print 'No token found'
            print 'Give me access here:', conn.getAuthURL()
            raw_input('Press enter once you gave access')
            folder, fileName = os.path.split(tokenPath)
            if not os.path.isdir(folder):
                os.makedirs(folder)
            f = open(tokenPath, "w")
            f.write(conn.getToken())
            f.close()
        self._connection = conn
