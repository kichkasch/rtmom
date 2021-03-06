# This Makefile is part of rtmom
#
# global parameters
TITLE=	"rtmom"
URL=		"http://freshmeat.net/projects/rtmom"
VERSION=	"0.1.4"

API_DOC_DIR=	apidoc/

# this generates API documentation in HTML format
# epydoc needs to be installed prior to usage - the epydoc program must be in your path environement.
api-docs:
	rm -rf $(API_DOC_DIR)	
	epydoc --inheritance listed -o $(API_DOC_DIR) -n $(TITLE)_$(VERSION) -u $(URL) *.py gui/*.py
	tar czf apidoc.tar.gz apidoc/

clean:
	rm -f *.pyc gui/*.pyc
	rm -rf build/template
	rm -f apidoc.tar.gz

# this whole thing is based on ipkg-build by Carl Worth
# http://cc.oulu.fi/~rantalai/freerunner/packaging/    
#
# make sure, you have provided all required up-to-date information in build/control before building a package
dist:	clean
	mkdir -p build/template/CONTROL
	cp build/control build/template/CONTROL
	mkdir -p build/template/opt/rtmom
	cp *.py COPYING README build/template/opt/rtmom
	mkdir -p build/template/opt/rtmom/gui
	cp gui/*.py build/template/opt/rtmom/gui
	mkdir build/template/bin
	ln -s /opt/rtmom/rtmom.py build/template/bin/rtmom
	mkdir -p build/template/usr/share/doc/rtmom
	cp rtmom.conf.example build/template/usr/share/doc/rtmom/
	mkdir -p build/template/usr/share/applications
	cp build/rtmom.desktop build/template/usr/share/applications
	mkdir -p build/template/usr/share/pixmaps
	cp build/rtmom.png build/template/usr/share/pixmaps
	cd build && fakeroot ./ipkg-build template
	rm -rf build/template

sdist: clean
	tar cf build/tmp.tar *.py gui/*.py rtmom.conf.example COPYING README build/rtmom.desktop build/rtmom.png
	mkdir rtmom-$(VERSION)
	(cd rtmom-$(VERSION) && tar -xf ../build/tmp.tar)
	rm build/tmp.tar
	tar czf build/rtmom-src-$(VERSION).tar.gz rtmom-$(VERSION)
	rm -rf rtmom-$(VERSION)

# you need e17 libs and python bindings, which have not yet made it into Ubuntu repos
# check this URL for manual installation:
# http://qa.debian.org/developer.php?login=lutin%40debian.org&set=yes&bugs=0&version=1&ubuntu=0&excuses=0&bin=1&buildd=0&problems=0&popc=0&watch=0&section=0&ordering=0&uploads=1&packages=&uploader=&mirror=http%3A%2F%2Fftp.debian.org%2Fdebian
sdist_ubuntu: sdist
	clear
