"""
Configuration for rtmom

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
import os.path
import os
import ConfigParser

#
# Part 1: Application specific configurations
#
APP_NAME = "rtmom"
APP_VERSION = "0.1.4 (2010-02-16)"

api_key = "afa4ce19b3ec31058c593fbca19ab636"
"""Key from RTM to use with this app (not the user)"""
shared_secret = "d6302c3f33fcd4cf"
"""Key from RTM to use with this app (not the user)"""

homedir = os.environ.get('HOME')

TOKEN_PATH = os.path.join(homedir, ".rtmom", "token")
"""The path where rtmom will store the user token when running for the first time; the token will then be loaded with every later use"""

CACHE_PATH =os.path.join(homedir, ".rtmom", "cache")
"""Allow for offline mode - all data is cached in this file until user manually asks for an update"""

CONFIG_PATH = os.path.join(homedir, ".rtmom", "conf")
"""Path of configuration file"""

#
# Part 2: User specific configurations
#

settings = None
def getSettings():
    """
    'Singleton'
    """
    global settings
    if not settings:
        settings = Settings()
    return settings
 
class Settings:
    """
    Handles user settings using configuration file in users home
    """
    
    def __init__(self):
        """
        Initialise and load
        
        If not config file yet available, create one with default settings.
        """
        if not os.path.isfile(CONFIG_PATH):
            self._createInitialConfig()
        self._config = ConfigParser.ConfigParser()
        self._config.readfp(open(CONFIG_PATH))
        
    def getValue(self, key, type = str):
        """
        Return value from user settings
        
        Allows for conversion into certain formats (e.g. lists or bool) by using parameter 'key'.
        """
        val = self._config.get("rtmom", key)
        if type == str:
            return val
        if type == list:
            items = val.split(",")
            ret = []
            for item in items:
                ret.append(item.strip())
            return ret
        if type == bool:
            return val.strip().lower() == "true"
        raise ValueError('Requested type for config value not defined')
            
    def _createInitialConfig(self):
        f = open(CONFIG_PATH, 'w')
        f.write("""[rtmom]\nshow_completed=False\nhidden_groups=Inbox,Sent""")
        f.close()
