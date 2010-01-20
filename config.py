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

# These values will be loaded from config file later on
show_completed = False
hidden_goups = ['Inbox', 'Sent']

APP_NAME = "rtmom"
APP_VERSION = "0.1.3 (2010-01-20)"

api_key = "afa4ce19b3ec31058c593fbca19ab636"
"""Key from RTM to use with this app (not the user)"""
shared_secret = "d6302c3f33fcd4cf"
"""Key from RTM to use with this app (not the user)"""

TOKEN_PATH = "/home/root/.rtmom/token"
"""The path where rtmom will store the user token when running for the first time; the token will then be loaded with every later use"""

CACHE_PATH = "/home/root/.rtmom/cache"
"""Allow for offline mode - all data is cached in this file until user manually asks for an update"""
