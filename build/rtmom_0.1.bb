DESCRIPTION = "Elementary based client for Remember the Milk written in Python. "
AUTHOR = "Michael Pilgermann"
PRIORITY = "optional"
LICENSE = "GPL"
HOMEPAGE = "http://freshmeat.net/projects/rtmom"
SRCNAME = "rtmom"
DEPENDS = "python-core pyrtm python-elementary"

PACKAGE_ARCH = "all"

PR = "r0"

SRC_URI = "???"

FILES_${PN} += "/opt/rtmom \
                ${datadir}/pixmaps \
                ${datadir}/applications \
                /home"
CONFFILES_${PN} += "/home/root/.${PN}/conf"

do_compile() {
	${STAGING_BINDIR_NATIVE}/python ${S}/setup.py build ${D}
}

do_install() {
	${STAGING_BINDIR_NATIVE}/python ${S}/setup.py install ${D}
	rm -rf ${D}/opt/rtmom/build/
	rm -rf ${D}/opt/rtmom/patches/
}
