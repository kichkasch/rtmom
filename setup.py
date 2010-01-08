"""
Manual setup file for rtmom
 
Elementary based client for "Remember the Milk" (http://www.rememberthemilk.com/) 
written in Python.
 
rtmom is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
 
rtmom is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
 
You should have received a copy of the GNU General Public License
along with rtmom. If not, see <http://www.gnu.org/licenses/>.


Run with 
    python setup.py build /         - or
    python setup.py install /
    
Puts all rtmom stuff under /opt/rtmom (assuming you provide / as destination)
Some links and additional stuff is put in corresponding places.
"""

import sys
import os
import os.path
import shutil

filesToMove = [
               ['conf', 'home/root/.rtmom', 'conf'], 
               ['build/rtmom.desktop', 'usr/share/applications', 'rtmom.desktop'], 
               ['build/rtmom.png', 'usr/share/pixmaps', 'rtmom.png']
               ]
filesToLink = [
               ['../opt/rtmom/rtmom.py', 'bin','rtmom']
               ]


def doBuild(path):
    pass

def doInstall(path):
    print "installing rtmom"
    basedir = os.path.join(path, 'opt/rtmom)
    if not os.path.exists(os.path.join(path, 'opt/')):
        os.mkdir(os.path.join(path, 'opt/'))
    shutil.copytree(os.getcwdu(), basedir)
    for entry in filesToMove:
        dir = os.path.join(path, entry[1])
        if not os.path.exists(dir):
            os.makedirs(dir)
        shutil.move(os.path.join(basedir, entry[0]), os.path.join(path, entry[1], entry[2]))
    for entry in filesToLink:
        destDir = os.path.join(path, entry[1])
        if not os.path.exists(destDir):
            os.makedirs(destDir)
        os.symlink(entry[0], os.path.join(destDir, entry[2]))            

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Wrong number of arguments"
        sys.exit(1)
    if sys.argv[1] == 'build':
        doBuild(sys.argv[2])
    elif sys.argv[1] == 'install':
        doInstall(sys.argv[2])
    
    else:
        print "Unknown command"
        sys.exit(1)

