#!/usr/bin/env python

"""
Main module for rtmom

Elementary based client for "Remember the Milk" (http://www.rememberthemilk.com/) written in Python. 

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

TOKEN_PATH = "./token"

import config
import rtm

def printTasks(rtm):
    """
    Command line output for the beginning
    """
    rspTasks = rtm.tasks.getList(filter = '') #filter='dueWithin:"1 week of today"')
    tasks = []
    for l in rspTasks.tasks.list:
        # XXX: taskseries *may* be a list 
        if isinstance(l.taskseries, (list, tuple)):
            for t in l.taskseries:
                tasks.append(t.name)
        else:
            tasks.append(l.taskseries.name)
    for task in tasks:
        print task

def getConnection():
    """
    Estabilshes connection with Remember The Milk backend
    
    Checks, whether token is known already; otherwise user interaction; finally connection
    """
    token = None
    try:
        f = open(TOKEN_PATH, 'r')
        token = f.read().strip()
        f.close()
    except:
        token = None
    conn = rtm.RTM(config.api_key, config.shared_secret, token)
    if not token :
        print 'No token found'
        print 'Give me access here:', conn.getAuthURL()
        raw_input('Press enter once you gave access')
        f = open(TOKEN_PATH, "w")
        f.write(conn.getToken())
        f.close()

    return conn


"""
This starts rtmom
"""
if __name__ == '__main__':
    printTasks(getConnection())
