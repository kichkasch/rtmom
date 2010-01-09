"""
File system access for rtmom (caching information for offline use)

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

import pickle
import config

class FileHandler():
    """
    Implementation for File System access (cache, offline mode)
    """
    
    def __init__(self, filename = None):
        """
        Initialize variable for filename
        
        Either from parameter given, or - if none given - from entry in config file.
        """
        if filename:
            self._filename = filename
        else:
            self._filename = config.CACHE_PATH
        
    def loadFromFile(self):
        """
        Loads chached data from a local file
        """
        f = open(self._filename, "r")
        (tasks,  categories) = pickle.load(f)
        f.close()
        return tasks, categories
        
    def saveToFile(self, tasks, categories):
        """
        Writes all cached data to a local file
        """
        f = open(self._filename, "w")
        pickle.dump((tasks, categories), f)
        f.close()
