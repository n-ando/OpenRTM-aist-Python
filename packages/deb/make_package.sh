#!/bin/sh 

openrtm_deb_makefile () {
cat <<'EOF'
# -*- Makefile -*-

all: install
install:
	python setup.py install
EOF
}

openrtm_example_deb_makefile () {
cat <<'EOF'
# -*- Makefile -*-

all: install
install:
	python setup.py install
EOF
}

openrtm_deb_makefile_py26 () {
cat <<'EOF'
# -*- Makefile -*-

all: install
install:
	python setup.py install --install-layout=deb
EOF
}

openrtm_deb_readme () {
cat <<'EOF'
openrtm-aist for Debian
-----------------------
Debian package of OpenRTM-aist

 -- Noriaki Ando <n-ando@aist.go.jp>  Mon, 23 Jun 2008 16:18:55 +0900
EOF
} 

openrtm_example_deb_readme () {
cat <<'EOF'
openrtm-aist for Debian
-----------------------
Debian package of OpenRTM-aist example

 -- Noriaki Ando <n-ando@aist.go.jp>  Mon, 23 Jun 2008 16:18:55 +0900
EOF
} 

openrtm_deb_changelog () {
cat <<'EOF'
openrtm-aist-python (1.1.0-rc1) unstable; urgency=low

  * Initial release.
 -- Noriaki Ando <n-ando@aist.go.jp>  Mon, 23 Jun 2008 16:18:55 +0900
EOF
}

openrtm_example_deb_changelog () {
cat <<'EOF'
openrtm-aist-python-example (1.1.0-rc1) unstable; urgency=low

  * Initial release.
 -- Noriaki Ando <n-ando@aist.go.jp>  Mon, 23 Jun 2008 16:18:55 +0900
EOF
}

openrtm_deb_compat () {
cat <<EOF
4
EOF
}

openrtm_deb_control () {
cat<<'EOF'
Source: openrtm-aist-python
Section: main
Priority: extra
Maintainer: Noriaki Ando <n-ando@aist.go.jp>
Build-Depends: debhelper, python, python-omniorb
Standards-Version: 3.7.2

Package: openrtm-aist-python
Architecture: any
Depends: ${shlibs:Depends}, ${misc:Depends}, python, python-omniorb
Description: OpenRTM-aist, RT-Middleware distributed by AIST
 OpenRTM-aist is a reference implementation of RTC (Robotic Technology 
 Component) specification which is OMG standard. OpenRTM-aist includes
 RT-Middleware runtime environment and RTC framework. The OMG standard
 defines a component model and certain important infrastructure services
 applicable to the domain of robotics software development.
 OpenRTM-aist is being developed and distributed by 
 Task Intelligence Research Group, Intelligent Systems Research Institute, 
 National Institute of Advanced Industrial Science and Technology (AIST), Japan. 
 Please see http://www.openrtm.org/openrtm/ for more detail. 

EOF
}

openrtm_example_deb_control () {
cat<<'EOF'
Source: openrtm-aist-python-example
Section: main
Priority: extra
Maintainer: Noriaki Ando <n-ando@aist.go.jp>
Build-Depends: debhelper, python
Standards-Version: 3.7.2

Package: openrtm-aist-python-example
Architecture: any
Depends: ${shlibs:Depends}, ${misc:Depends}
Description: OpenRTM-aist, RT-Middleware distributed by AIST
 OpenRTM-aist is a reference implementation of RTC (Robotic Technology 
 Component) specification which is OMG standard. OpenRTM-aist includes
 RT-Middleware runtime environment and RTC framework. The OMG standard
 defines a component model and certain important infrastructure services
 applicable to the domain of robotics software development.
 OpenRTM-aist is being developed and distributed by 
 Task Intelligence Research Group, Intelligent Systems Research Institute, 
 National Institute of Advanced Industrial Science and Technology (AIST), Japan. 
 Please see http://www.openrtm.org/openrtm/ for more detail. 

EOF
}

openrtm_deb_copyright () {
cat <<'EOF'
This package was debianized by Noriaki Ando <n-ando@aist.go.jp> on
Mon, 23 Jun 2008 16:18:55 +0900.

It was downloaded from <http://www.openrtm.org>

Upstream Author(s): 

    Noriaki Ando <n-ando@aist.go.jp>

Copyright: 

    Copyright (C) 2003-2008
    Noriaki Ando and the OpenRTM-aist Project team
    Intelligent Systems Research Institute,
    National Institute of Advanced Industrial Science and Technology (AIST),
    Tsukuba, Japan, All rights reserved.

License:

    The OpenRTM-aist-0.4 (AIST Software Distribution Number: H19PRO-693) is the
    dual-licensed open source software. You can use, copy, distribute and/or
    modify this library under the terms and conditions of either of the
    licenses below.
    
    1) LGPL (GNU LESSER GENERAL PUBLIC LICENSE)
    See COPYING.LIB.
    
    2) Individual Licnese
    You can purchase license from AIST and/or AIST's TLO to copy, distribute,
    modify and/or sublicense the library without any limitation in the terms of
    LGPL. The individual license should be concluded with a negotiated agreement
    between you and AIST and/or AIST TLO. To conclude individual license,
    contact the person responsible of AIST.

The Debian packaging is (C) 2008, Noriaki Ando <n-ando@aist.go.jp> and
is licensed under the LGPL, see `/usr/share/common-licenses/LGPL'.

# Please also look if there are files or directories which have a
# different copyright/license attached and list them here.
EOF
}

openrtm_deb_dirs () {
cat <<EOF
usr/bin
usr/sbin
EOF
}

openrtm_deb_docs () {
cat <<EOF
README
EOF
}

openrtm_deb_files () {
cat <<EOF
openrtm-aist-python_1.1.0-rc1_i386.deb main extra
EOF
}

openrtm_example_deb_files () {
cat <<EOF
openrtm-aist-python-example_1.1.0-rc1_i386.deb main extra
EOF
}

openrtm_deb_rules () {
cat <<'EOF'
#!/usr/bin/make -f
# -*- makefile -*-
# Sample debian/rules that uses debhelper.
# This file was originally written by Joey Hess and Craig Small.
# As a special exception, when this file is copied by dh-make into a
# dh-make output file, you may use that output file without restriction.
# This special exception was added by Craig Small in version 0.37 of dh-make.

# Uncomment this to turn on verbose mode.
#export DH_VERBOSE=1





configure: configure-stamp
configure-stamp:
	dh_testdir
	# Add here commands to configure the package.

	touch configure-stamp


build: build-stamp

build-stamp: configure-stamp  
	dh_testdir

	# Add here commands to compile the package.
	#$(MAKE)
	#docbook-to-man debian/openrtm-aist-python.sgml > openrtm-aist-python.1

	touch $@

clean: 
	dh_testdir
	dh_testroot
	rm -f build-stamp configure-stamp

	# Add here commands to clean up after the build process.
	#$(MAKE) clean

	dh_clean 

install: build
	dh_testdir
	dh_testroot
	dh_clean -k 
	dh_installdirs

	# Add here commands to install the package into debian/openrtm-aist-python.
	# $(MAKE) DESTDIR=$(CURDIR)/debian/openrtm-aist-python install
	python setup.py install --prefix=$(CURDIR)/debian/openrtm-aist-python/usr

# Build architecture-independent files here.
binary-indep: build install
# We have nothing to do by default.

# Build architecture-dependent files here.
binary-arch: build install
	dh_testdir
	dh_testroot
#	dh_installchangelogs 
#	dh_installdocs
	dh_installexamples
#	dh_install
#	dh_installmenu
#	dh_installdebconf	
#	dh_installlogrotate
#	dh_installemacsen
#	dh_installpam
#	dh_installmime
#	dh_python
#	dh_installinit
#	dh_installcron
#	dh_installinfo
	dh_installman
	dh_link
	dh_strip
	dh_compress
	dh_fixperms
#	dh_perl
#	dh_makeshlibs
	dh_installdeb
	dh_shlibdeps
	dh_gencontrol
	dh_md5sums
	dh_builddeb

binary: binary-indep binary-arch
.PHONY: build clean binary-indep binary-arch binary install

EOF
}

openrtm_deb_rules_py26 () {
cat <<'EOF'
#!/usr/bin/make -f
# -*- makefile -*-
# Sample debian/rules that uses debhelper.
# This file was originally written by Joey Hess and Craig Small.
# As a special exception, when this file is copied by dh-make into a
# dh-make output file, you may use that output file without restriction.
# This special exception was added by Craig Small in version 0.37 of dh-make.

# Uncomment this to turn on verbose mode.
#export DH_VERBOSE=1





configure: configure-stamp
configure-stamp:
	dh_testdir
	# Add here commands to configure the package.

	touch configure-stamp


build: build-stamp

build-stamp: configure-stamp  
	dh_testdir

	# Add here commands to compile the package.
	#$(MAKE)
	#docbook-to-man debian/openrtm-aist-python.sgml > openrtm-aist-python.1

	touch $@

clean: 
	dh_testdir
	dh_testroot
	rm -f build-stamp configure-stamp

	# Add here commands to clean up after the build process.
	#$(MAKE) clean

	dh_clean 

install: build
	dh_testdir
	dh_testroot
	dh_clean -k 
	dh_installdirs

	# Add here commands to install the package into debian/openrtm-aist-python.
	# $(MAKE) DESTDIR=$(CURDIR)/debian/openrtm-aist-python install
	python setup.py install --prefix=$(CURDIR)/debian/openrtm-aist-python/usr --install-layout=deb

# Build architecture-independent files here.
binary-indep: build install
# We have nothing to do by default.

# Build architecture-dependent files here.
binary-arch: build install
	dh_testdir
	dh_testroot
#	dh_installchangelogs 
#	dh_installdocs
	dh_installexamples
#	dh_install
#	dh_installmenu
#	dh_installdebconf	
#	dh_installlogrotate
#	dh_installemacsen
#	dh_installpam
#	dh_installmime
#	dh_python
#	dh_installinit
#	dh_installcron
#	dh_installinfo
	dh_installman
	dh_link
	dh_strip
	dh_compress
	dh_fixperms
#	dh_perl
#	dh_makeshlibs
	dh_installdeb
	dh_shlibdeps
	dh_gencontrol
	dh_md5sums
	dh_builddeb

binary: binary-indep binary-arch
.PHONY: build clean binary-indep binary-arch binary install

EOF
}

openrtm_deb_example_rules () {
cat <<'EOF'
#!/usr/bin/make -f
# -*- makefile -*-
# Sample debian/rules that uses debhelper.
# This file was originally written by Joey Hess and Craig Small.
# As a special exception, when this file is copied by dh-make into a
# dh-make output file, you may use that output file without restriction.
# This special exception was added by Craig Small in version 0.37 of dh-make.

# Uncomment this to turn on verbose mode.
#export DH_VERBOSE=1





configure: configure-stamp
configure-stamp:
	dh_testdir
	# Add here commands to configure the package.

	touch configure-stamp


build: build-stamp

build-stamp: configure-stamp  
	dh_testdir

	# Add here commands to compile the package.
	#$(MAKE)
	#docbook-to-man debian/openrtm-aist-python.sgml > openrtm-aist-python.1

	touch $@

clean: 
	dh_testdir
	dh_testroot
	rm -f build-stamp configure-stamp

	# Add here commands to clean up after the build process.
	#$(MAKE) clean

	dh_clean 

install: build
	dh_testdir
	dh_testroot
	dh_clean -k 
	dh_installdirs

	# Add here commands to install the package into debian/openrtm-aist-python.
	# $(MAKE) DESTDIR=$(CURDIR)/debian/openrtm-aist-python install
	python setup.py install --prefix=$(CURDIR)/debian/openrtm-aist-python-example/usr

# Build architecture-independent files here.
binary-indep: build install
# We have nothing to do by default.

# Build architecture-dependent files here.
binary-arch: build install
	dh_testdir
	dh_testroot
#	dh_installchangelogs 
#	dh_installdocs
	dh_installexamples
#	dh_install
#	dh_installmenu
#	dh_installdebconf	
#	dh_installlogrotate
#	dh_installemacsen
#	dh_installpam
#	dh_installmime
#	dh_python
#	dh_installinit
#	dh_installcron
#	dh_installinfo
	dh_installman
	dh_link
	dh_strip
	dh_compress
	dh_fixperms
#	dh_perl
#	dh_makeshlibs
	dh_installdeb
	dh_shlibdeps
	dh_gencontrol
	dh_md5sums
	dh_builddeb

binary: binary-indep binary-arch
.PHONY: build clean binary-indep binary-arch binary install

EOF
}

export PATH=/usr/local/bin:/usr/bin:/bin:/usr/X11R6/bin:/usr/local/X11R6/bin:/usr/local/sbin:/usr/sbin:/sbin
export LANG=C
export LC_ALL=C

# date
date=`date "+%y%m%d%H%M"`
time=/usr/bin/time
# package location and build directory
# package=/usr/users/builder/PackageBuild/src/OpenRTM-aist-1.1.0.tar.gz
package=/usr/users/builder/PyPackageBuild/src/OpenRTM-aist-Python-1.1.0.tar.gz
package_example=/usr/users/builder/PyPackageBuild/src/OpenRTM-aist-Python-example-1.1.0.tar.gz
packagedir=openrtm-aist-python-1.1.0
packagedir_example=openrtm-aist-python-example-1.1.0
decomp_packagedir=OpenRTM-aist-Python-1.1.0
decomp_example_packagedir=OpenRTM-aist-Python-example-1.1.0
package_date=`ls -al $package | awk '{printf("%s/%s %s\n",$6,$7,$8);}'`
package_date=`diff -ac $package /dev/null | head -1 |awk '{print $3,$4,$5,$6,$7,$8;}'`
package_name=`basename $package`
python_ver=`python -V 3>&1 > /dev/null 2>&3| sed -e's/Python //'`
echo "python version" $python_ver
py_major=`echo $python_ver | cut -f1 -d'.'`
py_minor=`echo $python_ver | cut -f2 -d'.'`
py_release=`echo $python_ver | cut -f3 -d'.'`
echo "py_major" $py_major
echo "py_minor" $py_minor
echo "py_release" $py_release

python_version=""

if test $py_major -ge 2; then
    if test $py_minor -ge 6; then
	python_version="python26"
    fi
fi

# buildroot=/usr/users/builder/PackageBuild
buildroot=/usr/users/builder/PyPackageBuild

logheader="<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 3.2 Final//EN\"><html><body><pre>"
logfooter="</pre></body></html>"

# system information
hostname=`hostname`
os=`uname -s`
release=`uname -r`-`uname -p`

dist_name=""
dist_key=""
# Check the lsb distribution name
if test -f /etc/lsb-release ; then
    . /etc/lsb-release
    if test "x$DISTRIB_DESCRIPTION" != "x" ; then
	dist_name=$DISTRIB_DESCRIPTION-`uname -m`
	dist_key=$DISTRIB_ID
    fi
fi
# Check the Fedora version
if test "x$dist_name" = "x" && test -f /etc/fedora-release ; then
    dist_name=`cat /etc/fedora-release`-`uname -m`
    dist_key=`sed -e 's/.[^0-9]*\([0-9]\).*/fc\1/' /etc/fedora-release`
fi
#Check the Debian version
if test "x$dist_name" = "x" && test -f /etc/debian_version ; then
    dist_name="Debian"`cat /etc/debian_version`-`uname -m`
    dist_key="Debian"
fi
# Check the Vine version
if test "x$dist_name" = "x" && test -f /etc/vine-release ; then
    dist_name=`cat /etc/vine-release`-`uname -m`
    dist_key=`sed -e 's/.*\([0-9]\)\.\([0-9]\).*/vl\1\2/' /etc/vine-release`
fi
# Check the TuboLinux version
if test "x$dist_name" = "x" && test -f /etc/turbolinux-release ; then
    dist_name=`cat /etc/tubolinux-release`-`uname -m`
    dist_key=""
fi

if test "x$dist_name" = "x" ; then
    dist_name=$os$release
fi
# Check the RedHat/Fedora version
if test "x$dist_name" = "x" && test -f /etc/redhat-release ; then
    dist_name=`cat /etc/redhat-release`-`uname -m`
fi

# only fedora and vine
if test ! "x$dist_key" = "xDebian" -a ! "x$dist_key" = "xUbuntu" ; then
    echo $dist_key
    echo "This is not debian/ubuntu"
    exit 0
fi

echo $dist_key

distname=`echo $dist_name | sed 's/[ |\(|\)]//g'`
# system dependent build directory and log file name
builddir=$buildroot/$distname
timestamp=$buildroot/.$distname
logfile=$distname-Python$date.log

build=""
echo $dist_key
# check package
if test -f $package ; then
    echo "Package found: " $package
else
    echo "Package not found: " $pacakge
    exit 1
fi
cd $buildroot

# check if package is new
if test -f $timestamp ; then
    if test $package -nt $timestamp ; then
	build=yes
	echo "New source file was found."
        touch $timestamp
    fi
else
    echo "Timestamp not found."
    touch $timestamp
    build=yes
fi

if test "x$build" = "x" ; then
    echo "No new package."
    exit 1
fi

# cleanup 
echo "cleanup " $builddir/$packagedir
rm -rf $builddir

mkdir -p $builddir
cd $builddir

echo "distribution: " $dist_name >> $buildroot/$logfile
echo "package: $package_date " >> $buildroot/$logfile


#------------------------------------------------------------
# package build process
#------------------------------------------------------------
echo $logheader > $buildroot/make-$logfile

tar xvzf $package
mv $decomp_packagedir $packagedir
mkdir $packagedir/debian
echo "packagedir " $packagedir
tar xvzf $package_example
mv $decomp_example_packagedir $packagedir_example
mkdir $packagedir_example/debian
echo "packagedir_example " $packagedir_example

if test "x$python_version"  = "x" ; then
    openrtm_deb_makefile  > $packagedir/Makefile
else
    openrtm_deb_makefile_py26  > $packagedir/Makefile
fi
#openrtm_deb_readme    > $packagedir/debian/README.Debian
openrtm_deb_changelog > $packagedir/debian/changelog
openrtm_deb_compat    > $packagedir/debian/compat
openrtm_deb_control   > $packagedir/debian/control
openrtm_deb_copyright > $packagedir/debian/copyright
openrtm_deb_dirs      > $packagedir/debian/dirs
openrtm_deb_docs      > $packagedir/debian/docs
openrtm_deb_files     > $packagedir/debian/files
chmod 444 $packagedir/debian/files
if test "x$python_version"  = "x" ; then
    openrtm_deb_rules     > $packagedir/debian/rules
else
    openrtm_deb_rules_py26     > $packagedir/debian/rules
fi
chmod 755 $packagedir/debian/rules

#for example
openrtm_example_deb_makefile  > $packagedir_example/Makefile
openrtm_example_deb_changelog > $packagedir_example/debian/changelog
openrtm_deb_compat    > $packagedir_example/debian/compat
openrtm_example_deb_control   > $packagedir_example/debian/control
openrtm_deb_copyright > $packagedir_example/debian/copyright
openrtm_deb_dirs      > $packagedir_example/debian/dirs
openrtm_deb_docs      > $packagedir_example/debian/docs
openrtm_example_deb_files     > $packagedir_example/debian/files
chmod 444 $packagedir_example/debian/files
openrtm_deb_example_rules     > $packagedir_example/debian/rules
chmod 755 $packagedir_example/debian/rules

cd $packagedir

if $time -p -o make_time-$logfile dpkg-buildpackage -us -uc -rfakeroot >> $buildroot/make-$logfile 2>&1 ; then
    cd ../
    cd $packagedir_example
    if $time -p -o make_time-$logfile dpkg-buildpackage -us -uc -rfakeroot >> $buildroot/make-$logfile 2>&1 ; then
	echo $logfooter >> $buildroot/make-$logfile
	make_time=`awk '/real/{printf("%s[s] ", $0);}' make_time-$logfile`
	echo "make: OK" >> $buildroot/$logfile
	echo "make_time: $make_time" >> $buildroot/$logfile
	rm -f make_time-$logfile
	
    else
	echo "make: NG" >> $buildroot/$logfile
	rm -f make_time-$logfile
	exit 1
    fi
else
    echo "make: NG" >> $buildroot/$logfile
    rm -f make_time-$logfile
    exit 1
fi

