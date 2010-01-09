#!/usr/bin/env python

"""
Main module for rtmom

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
categoryMapping = None
"""Maps names of Categories (lists) for tasks to their corresponding IDs"""

def getCategories(rtm):
    global categoryMapping
    categoryMapping = {}
    rspLists = rtm.lists.getList()
    for cat in rspLists.lists.list:
        categoryMapping[cat.name] = cat.id
    return categoryMapping.keys()

def _assembleFilter(filter):
    if not config.show_completed:
        if filter:
            filter = "(" + filter + ") AND " + "status:incomplete"
        else:
            filter = "status:incomplete"
    return filter

def _extractTasksFromDottedDict(taskList):
    tasks = []
    if not isinstance(taskList, (list, tuple)):
        for t in taskList.taskseries:
            tasks.append(t)
    else:
        for l in taskList:      
            # XXX: taskseries *may* be a list 
            if isinstance(l.taskseries, (list, tuple)):
                for t in l.taskseries:
                    tasks.append(t)
            else:
                tasks.append(l.taskseries)
    return tasks
            
def getFullTasks(rtm, cat = None, filter = ""):
    global categoryMapping
    filter = _assembleFilter(filter)
    if cat and categoryMapping:
        rspTasks = rtm.tasks.getList(list_id = categoryMapping[cat],  filter = filter)
    else:
        rspTasks = rtm.tasks.getList(filter = filter)
    return _extractTasksFromDottedDict(rspTasks.tasks.list)
    
def getTasks(rtm, cat = None, filter = ""):
    """
    Returns names of tasks
    """
    taskNames = []
    for task in getFullTasks(rtm, cat, filter):
        taskNames.append(task.name)
    return taskNames


def getConnection():
    """
    Estabilshes connection with Remember The Milk backend
    
    Checks, whether token is known already; otherwise user interaction; finally connection
    """
    token = None
    try:
        f = open(config.TOKEN_PATH, 'r')
        token = f.read().strip()
        f.close()
    except:
        token = None
    conn = rtm.RTM(config.api_key, config.shared_secret, token)
    if not token :
        print 'No token found'
        print 'Give me access here:', conn.getAuthURL()
        raw_input('Press enter once you gave access')
        f = open(config.TOKEN_PATH, "w")
        f.write(conn.getToken())
        f.close()

    return conn


def printTasks(rtm):
    """
    Command line output of all tasksk for testing purposes
    """
#    for task in getTasks(rtm):
    for task in getTasks(rtm, "Privat"):
        print task

def printCategories(rtm):
    for cat in getCategories(rtm):
        print cat

"""
This starts rtmom
"""
if __name__ == '__main__':
#    c = getConnection()
#    printCategories(c)
#    print "\n\n"
#    printTasks(c)
    import gui.rtmom_gui
    gui.rtmom_gui.initAndRun()
