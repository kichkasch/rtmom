DESCRIPTION = "Python interface for Remember The Milk API."
AUTHOR = "Sridhar Ratnakumar / srid"
PRIORITY = "optional"
LICENSE = "MIT"
HOMEPAGE = "http://pypi.python.org/pypi/pyrtm"
SRCNAME = "pyrtm"
DEPENDS = "python-native"


PACKAGE_ARCH = "all"

PR = "r0"

SRC_URI = "http://pypi.python.org/packages/source/p/pyrtm/pyrtm-0.2.tar.gz"

do_compile() {
	${STAGING_BINDIR_NATIVE}/python ${S}/setup.py build ${D}
}

do_install() {
	${STAGING_BINDIR_NATIVE}/python ${S}/setup.py install ${D}
}
