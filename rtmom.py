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

class RTMOM():
    """
    Local data management for rtmom
    
    @ivar _categories: Maps names of Categories (lists) for tasks to their corresponding IDs
    @ivar _tasks: Holds information about all tasks in memory
    """
    def __init__(self):
        """
        Constructor - empy initialize categories and tasks
        """
        self._categories = None
        self._tasks = None

    def getCategories(self):
        """
        Return categories in memory
        """
        return sorted(self._categories.keys())
        
    def getFullTasks(self, category):
        """
        Return tasks in memory
        """        
        return self._tasks[category]
    
    def getFullTaskFromName(self, taskName):
        """
        Searches for the full task using the task name
        """
        for cat in self.getCategories():
            for fullTask in self.getFullTasks(cat):
                if fullTask.name == taskName:
                    return fullTask
        raise ValueError('Task with given name could not be found.')
    
    def getTasks(self, cat):
        """
        Returns names of tasks in memory
        """
        taskNames = []
        for task in self.getFullTasks(cat):
            taskNames.append(task.name)
        return taskNames

    def doLoadFromFile(self, fileHandler):
        """
        Populate local lists with content from local file
        """
        print "--- Loading from local cache"
        self._tasks, self._categories = fileHandler.loadFromFile()
        print "\t Sucess"
        
    def doSaveToFile(self, fileHandler):
        """
        Write all information from local lists (memory) to local file
        """
        print "--- Saving to local cache"
        fileHandler.saveToFile(self._tasks, self._categories)
        print "\t Sucess"

    def updateFromNet(self, netHandler):
        """
        Populate local lists (memory) with content from RTM service in the Internet
        """
        print "--- Updating from Net"
        self._categories = netHandler.loadCategories()
        self._tasks = {}
        for name, id in self._categories.items():
            self._tasks[name] = netHandler.loadFullTasks(id)
        print "\t Sucess"
       
extractor = None
def getExtractor():
    """
    Singleton
    """
    global extractor
    if not extractor:
        extractor = InformationExtractor()
    return extractor
      
class InformationExtractor():
    """
    Extract (and format) information coming from RTM
    """
    def __init__(self):
        pass
        
    def extractTags(self, task, delimiter = ", "):
        ret = ""
        if not isinstance(task.tags, list): # no tag at all
            if  isinstance(task.tags.tag, list):
                ret += task.tags.tag[0]
                for tagEntry in task.tags.tag[1:]:
                    ret += delimiter + tagEntry
            else:
               ret += task.tags.tag 
        return ret
        
    def replaceCharactersBefore(self, string, maxLen = 0):
        ret = str(string)
        ret = ret.replace('<', '(')
        ret = ret.replace('>', ')')     
        ret = ret.replace('\/', '/')
        if maxLen:
            if len(ret) > maxLen:
                ret = ret[:maxLen-3]+"..."
        return ret
        
    def replaceCharactersAfter(self, string):
        ret = str(string)
        ret = ret.replace('\n', '<br>')
        return ret
        
    def formatNote(self, note):
        ret = """<b>""" + self.replaceCharactersBefore(note.title)+ """</>\n""" + self.replaceCharactersBefore(getattr(note,'$t'))   # the note content is hidden in the XML content (here $t)
        return self.replaceCharactersAfter(ret)
        
        
"""
This starts rtmom
"""
if __name__ == '__main__':
    import gui.rtmom_gui
    gui.rtmom_gui.initAndRun()
