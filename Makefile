# This Makefile is part of rtmom
#
# global parameters
TITLE=	"rtmom"
URL=		"http://freshmeat.net/projects/rtmom"
VERSION=	"0.1"

API_DOC_DIR=	apidoc/

# this generates API documentation in HTML format
# epydoc needs to be installed prior to usage - the epydoc program must be in your path environement.
api-docs:
	rm -rf $(API_DOC_DIR)	
	epydoc --inheritance listed -o $(API_DOC_DIR) -n $(TITLE)_$(VERSION) -u $(URL) *.py 
	tar czf apidoc.tar.gz apidoc/

clean:
	rm -f *.pyc 
	rm -rf build/template
	rm -f apidoc.tar.gz

# this whole thing is based on ipkg-build by Carl Worth
# http://cc.oulu.fi/~rantalai/freerunner/packaging/    
#
# make sure, you have provided all required up-to-date information in build/control before building a package
dist:	clean
	mkdir build/template
	mkdir build/template/CONTROL
	cp build/control build/template/CONTROL
	mkdir -p build/template/opt/rtmom
	cp *.py COPYING README build/template/opt/rtmom
	mkdir build/template/bin
	ln -s /opt/rtmom/rtmom.py build/template/bin/rtmom
	mkdir -p build/template/home/root/.rtmom
	cp conf build/template/home/root/.rtmom/conf
	mkdir -p build/template/usr/share/applications
	cp build/rtmom.desktop build/template/usr/share/applications
	mkdir -p build/template/usr/share/pixmaps
	cp build/rtmom.png build/template/usr/share/pixmaps
	cd build && fakeroot ./ipkg-build template
	rm -rf build/template

sdist: clean
	tar cf build/tmp.tar *.py conf COPYING README build/rtmom.desktop build/rtmom.png
	mkdir rtmom-$(VERSION)
	(cd rtmom-$(VERSION) && tar -xf ../build/tmp.tar)
	rm build/tmp.tar
	tar czf build/rtmom-src-$(VERSION).tar.gz rtmom-$(VERSION)
	rm -rf rtmom-$(VERSION)
