%define major 3
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

%define pppd_ver %(/usr/sbin/pppd --version 2>&1 | sed -n '/pppd version \\([0-9][.0-9]*\\)/s//\\1/p')
%define pppd_ver_num %(echo %{pppd_ver} | perl -pe '/(\\d+)\\.(\\d)\\.?(\\d)?\\.?(\\d)?/; $_=($1)*1000000+($2)*10000+($3)*100+($4||0)')

Summary:	Bundled Utilities for configuring ISDN4Linux
Name:		isdn4k-utils
Version:	3.12
Release:	%mkrel 0.1
License:	GPLv2
Epoch:		1
Group:		System/Configuration/Networking
URL:		http://www.isdn4linux.de/
Source0:	%{name}.tar.gz
Source1:	%{name}-config
Source2:	capi4linux
Source3:	isdn4k-utils-ppp-2.4.4.tar.bz2
Patch1:		%{name}.ipppd.patch
Patch3:		%{name}-no-root.patch
Patch7:		%{name}-nomknod.patch
Patch9:		%{name}-glibc222.patch
Patch10:	%{name}-isdnlog.patch
Patch11:	%{name}-define.patch
Patch15:	%{name}-eurofile-init-fix.patch
Patch16:	%{name}-3.2p3-skip-capi-header-check.patch
Patch18:	isdn4k-utils-lib64.patch
Patch20:	isdn4k-utils-64bit-fixes.patch
Patch21:	isdn4k-utils-ppp244.patch
Patch23:	isdn4k-utils-target.patch
# capi20.h must #include sys/types.h - AdamW 2008/02
Patch24:	isdn4k-utils-3.2p3-types.patch
Patch25:	isdn4k-utils-autoconf25x.diff
Patch26:	isdn4k-utils-cleanup.diff
Patch27:	isdn4k-utils-openssl_des.h_fix.diff
Requires(post): rpm-helper
Requires(preun): rpm-helper
BuildRequires:	autoconf2.5
BuildRequires:	automake
BuildRequires:	gdbm-devel
BuildRequires:	imake
BuildRequires:	kernel-source
BuildRequires:	libtcl-devel
BuildRequires:	libtool
BuildRequires:	libxext-devel
BuildRequires:	libxmu-devel
BuildRequires:	libxp-devel
BuildRequires:	libxt-devel
BuildRequires:	linuxdoc-tools
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel
BuildRequires:	pcap-devel
BuildRequires:	ppp
BuildRequires:	ppp-devel
BuildRequires:	X11-devel
BuildRequires:	xaw-devel
BuildRequires:	xpm-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
isdn4k-utils is a collection of various ISDN related utilities. This
package contains configuration tools for all ISDN adapters, supported
by Linux. Furthermore, several status-monitors are provided as well as
some ISDN-based applications. Namely ipppd, a PPP daemon for synchronous
PPP over ISDN; vbox, an answering-machine and (for use with AVM-B1 only)
capifax, a faxmachine.

%package	xtools
Summary:	ISDN utilities that use X
Group:		Networking/Other
Requires:	%{name} >= %{epoch}:%{version}

%description	xtools
These are the graphical utilities for ISDN, xmonisdn and xisdnload.
They provide, each in their own way, a visual indication of the status
of the ISDN lines, so that it is directly obvious when there is a
connection, for example. 

%package	vbox
Summary:	ISDN answering machine
Group:		Communications
Requires:	%{name} >= %{epoch}:%{version}

%description	vbox
ISDN Answering Machine

%package	eurofile
Summary:	ISDN eurofile transfer tool
Group:		Networking/File transfer
License:	LGPL
Requires:	%{name} >= %{epoch}:%{version}
Requires(post): rpm-helper
Requires(preun): rpm-helper

%description	eurofile
If you want to send / receive files over an ISDN line with the eurofile system,
you need this package.

%package	isdnlog
Summary:	ISDN connection logger
Group:		Communications
Requires:	%{name} >= %{epoch}:%{version}

%description	isdnlog
isdnlog logs all ISDN connections, and can calculate the cost of calls.
If sufficient data is available, it can even recommend which alternate
carrier would have been cheaper for a given call. For countries where calls
are charged per discrete unit, it can disconnect the line just before the
next unit starts. 

%package -n	%{libname}
Summary:	Main library for %{name}
Group:		System/Libraries
Requires:	%{name} >= %{epoch}:%{version}

%description -n	%{libname}
isdn4k-utils is a collection of various ISDN related utilities. This
package contains configuration tools for all ISDN adapters, supported
by Linux. Furthermore, several status-monitors are provided as well as
some ISDN-based applications. Namely ipppd, a PPP daemon for synchronous
PPP over ISDN; vbox, an answering-machine and (for use with AVM-B1 only)
capifax, a faxmachine.
This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n	%{develname}
Summary:	Includes and other files to develop %{name} applications
Group:		Development/C
Requires:	%{libname} >= %{epoch}:%{version}
Provides:	lib%{name}-devel %{name}-devel
Obsoletes:	%{mklibname %{name} -d 2}

%description -n	%{develname}
Libraries, include files and other resources you can use to develop
%{name} applications.

%package	doc
Summary:	Complete HTML documentation for isdn4k-utils
Group:		System/Configuration/Networking
Conflicts:	isdn4k-utils < 3.2p3-28mdv2007.1

%description	doc
This is the original, complete, documentation for isdn4k-utils, in
HTML format.

isdn4k-utils is a collection of various ISDN related utilities. This
package contains configuration tools for all ISDN adapters, supported
by Linux. Furthermore, several status-monitors are provided as well as
some ISDN-based applications. Namely ipppd, a PPP daemon for synchronous
PPP over ISDN; vbox, an answering-machine and (for use with AVM-B1 only)
capifax, a faxmachine.

%prep

%setup -q -n %{name} -a3

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0554 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;

for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

%patch1 -p1 -b .old
%patch3 -p1 -b .old
%patch7 -p1 -b .old
%patch9 -p1 -b .old
%patch10 -p0 -b .old
%patch11 -p1 -b .old
%patch15 -p0 -b .old
%patch16 -p1 -b .nocheck
%patch18 -p1 -b .lib64
%patch20 -p1 -b .64bit-fixes

# (simpler) lib64 fix
perl -pi -e "s|/usr/lib/|%{_libdir}/|" pppdcapiplugin/ppp-2.*/Makefile pppdcapiplugin/Makefile.template

%patch23 -p1 -b .target
%patch24 -p1 -b .types
%patch25 -p1 -b .autoconf25x
%patch26 -p1 -b .cleanup
%patch27 -p0 -b .openssl_des.h_fix

#(peroyvind) provide our own config file with correct options and paths
install %{SOURCE1} .config
echo "LIBDIR='%{_libdir}'" >> .config

# AMD K6 is not an i686
%ifarch
perl -pi -e "s/k6 \| //" vbox3/config.sub
perl -pi -e "s/k6-\* \| //" vbox3/config.sub
perl -pi -e "s/\| k5 \|/\| k5 \| k6 \|/" vbox3/config.sub
perl -pi -e "s/\| k5-\* \|/\| k5-\* \| k6-* \|/" vbox3/config.sub
%endif

# tcl hack
. %{_libdir}/tclConfig.sh
find -type f | xargs perl -pi -e "s|tcl8\.4|tcl${TCL_VERSION}|g"

# nuke this for now
rm -rf ant-phone

# antiborker
#perl -pi -e "s|\'||g" .config <- this won't work!
find vbox -type f | xargs perl -pi -e "s|\@VBOX_DOCDIR\@|/usr/share/doc/vbox|g"
find vbox -type f | xargs perl -pi -e "s|\@VBOX_LOCKDIR\@|/var/lock|g"

%build
export FORCE_AUTOCONF_2_5=1

for i in */configure; do
    cd `dirname $i`
	autoreconf -fis
    cd ..
done

(cd linux && ln -s /usr/include .)

# workaround for automake/autoconf
if [ -x /usr/share/automake/depcomp ] ; then
  for i in capiinfo capiinit rcapid capifax; do
    cp -f /usr/share/automake/depcomp $i
    ( cd $i ; aclocal && autoconf )
  done
fi

# we need it on ia64 machine
( cd capi20; [ -f configure.in ] && libtoolize --copy --force )
( cd vbox; [ -f configure.in ] && libtoolize --copy --force )

#(peroyvind) added more flags for pppdcapiplugin since we're overriding it's CFLAGS which cointains flags needed
RPM_OPT_FLAGS="$RPM_OPT_FLAGS -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -DISDN_MAX_DRIVERS=32 -DISDN_MAX_CHANNELS=64 -fPIC -DPPPVER=%{pppd_ver_num} -I. -I`pwd`/capi20 -Ipppd -L`pwd`/capi20 -I./include"

#(peroyvind) workaround for wrong aclocal
make CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" CCFLAGS="$RPM_OPT_FLAGS" subconfig
perl -pi -e "s|CDEBUGFLAGS = .*|CDEBUGFLAGS = $RPM_OPT_FLAGS|" xisdnload/Makefile xmonisdn/Makefile
perl -pi -e "s|CXXDEBUGFLAGS = \-0.*|CXXDEBUGFLAGS = $RPM_OPT_FLAGS|" xisdnload/Makefile xmonisdn/Makefile
cp isdnlog/isdnlog/isdnlog.5.in isdnlog/isdnlog/isdnlog.5

#(peroyvind) workaround for non-existing rcapid/acinclude.m4
touch rcapid/acinclude.m4

# (blino) compile pppdcapiplugin for current pppd only to avoid errors and unnecessary time spent on compiling
perl -pi -e "s|^(PPPVERSIONS\s*)=\s*.+$|\1= %{pppd_ver}|" pppdcapiplugin/Makefile

#(peroyvind) added CCFLAGS since it's a variable used a few places in stead of CFLAGS (*sigh*)
make CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" CCFLAGS="$RPM_OPT_FLAGS" || make CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" CCFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf %{buildroot}

RPM_OPT_FLAGS="$RPM_OPT_FLAGS -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -DISDN_MAX_DRIVERS=32 -DISDN_MAX_CHANNELS=64 -fPIC -DPPPVER=%{pppd_ver_num} -I. -I`pwd`/capi20 -Ipppd -L`pwd`/capi20 -I./include"

mkdir -p %{buildroot}{%{_sbindir},%{_bindir},%{_includedir},%{_mandir},%{_docdir},/sbin,%{_initrddir},%{_libdir}/isdn}

#(peroyvind) yet another workaround.. this time for providing compile flags for stuff that was'nt compiled last time..
%makeinstall_std CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" CCFLAGS="$RPM_OPT_FLAGS" MANPATH=%{_mandir}
rm -f %{buildroot}%{_bindir}/vboxbeep # security hole if used. (dam's)
rm -f %{buildroot}%{_mandir}/man*/vboxbeep*

#(peroyvind) fix incorrect filename for man page
mv %{buildroot}%{_mandir}/man8/.isdnctrl_conf.8 %{buildroot}%{_mandir}/man8/isdnctrl_conf.8

#(peroyvind) move this one out of buildroot, we want to have it somewhere else..
rm -rf vbox/docs; mv %{buildroot}%{_docdir}/vbox vbox/docs

#(peroyvind) fix name for init script
mv %{buildroot}%{_initrddir}/eftd.sh %{buildroot}%{_initrddir}/eftd

#(peroyvind) install man pages for eurofile
install -m644 eurofile/doc/*.5 %{buildroot}%{_mandir}/man5/

#(peroyvind) remove uninstalled symlink
rm -rf %{buildroot}/usr/lib/X11/app-defaults
rm -f  %{buildroot}%{_sysconfdir}/isdn/eftusers

install -m755 %{SOURCE2} %{buildroot}%{_initrddir}/capi4linux

#(peroyvind) get rid of drdsl files which are provided by other package according to Steffen Barszus
rm -rf %{buildroot}%{_sysconfdir}/drdsl

# bork
perl -pi -e "s|^dependency_libs=.*|dependency_libs=\' -L%{_libdir}\'|g" %{buildroot}%{_libdir}/libcapi*.la

# cleanup
rm -f %{buildroot}/usr/share/doc/i4lfaq*

# hmm...
mv %{buildroot}/sbin/* %{buildroot}%{_sbindir}/

%post
%_post_service capi4linux

%preun
%_preun_service capi4linux

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%post eurofile
%_post_service eftd

%preun eurofile
%_preun_service eftd

%clean
rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc README NEWS
%dir %{_libdir}/isdn
%dir %{_datadir}/isdn
%{_datadir}/isdn/*
%dir %{_sysconfdir}/isdn
#%dir %{_sysconfdir}/drdsl
#%config(noreplace) %{_sysconfdir}/drdsl/adsl.conf
%config(noreplace) %{_sysconfdir}/ppp/peers/isdn/arcor
%config(noreplace) %{_sysconfdir}/ppp/peers/isdn/avm
%config(noreplace) %{_sysconfdir}/ppp/peers/isdn/avm-ml
%config(noreplace) %{_sysconfdir}/ppp/peers/isdn/leased
%config(noreplace) %{_sysconfdir}/ppp/peers/isdn/otelo
%config(noreplace) %{_sysconfdir}/ppp/peers/isdn/talkline
%config(noreplace) %{_sysconfdir}/isdn/isdn.conf
%config(noreplace) %{_sysconfdir}/isdn/callerid.conf
%config(noreplace) %{_sysconfdir}/isdn/rate.conf
#%config(noreplace) %{_sysconfdir}/ppp/ioptions
%{_mandir}/man4/*
%{_mandir}/man7/isdn_cause.7*
%{_mandir}/man8/avmcapictrl.8*
%{_mandir}/man*/capi*
%{_mandir}/man8/icnctrl.8*
%{_mandir}/man8/imon.8*
%{_mandir}/man8/imontty.8*
%{_mandir}/man8/ipppd.8*
%{_mandir}/man8/ipppstats.8*
%{_mandir}/man8/iprofd.8*
%{_mandir}/man8/isdnctrl.8*
%{_mandir}/man8/isdnctrl_conf.8*
%{_mandir}/man8/loopctrl.8*
%{_mandir}/man8/pcbitctl.8*
%{_mandir}/man8/eiconctrl.8*
%{_mandir}/man8/hisaxctrl.8*
%{_mandir}/man8/divertctrl.8*
%{_mandir}/man8/actctrl.8*
%defattr(755,root,root,755)
%{_initrddir}/capi4linux
%{_sbindir}/avmcapictrl
%{_sbindir}/capiinit
%{_sbindir}/hisaxctrl
%{_sbindir}/icnctrl
%{_sbindir}/imon
%{_sbindir}/imontty
%{_sbindir}/ipppd
%{_sbindir}/ipppstats
%{_sbindir}/iprofd
%{_sbindir}/isdnctrl
%{_sbindir}/loopctrl
%{_sbindir}/pcbitctl
%{_sbindir}/rcapid
%{_sbindir}/actctrl
%{_sbindir}/diva*
%{_sbindir}/eiconctrl
%{_sbindir}/divertctrl
%{_bindir}/capi*

%files xtools
%defattr(644,root,root,755)
%doc xmonisdn/README
%{_mandir}/man*/*
%{_includedir}/X11/bitmaps/net*
#%{_prefix}/X11R6/lib/X11/doc/html/*.html
%config(noreplace) %{_sysconfdir}/X11/app-defaults/XISDNLoad
%defattr(755,root,root,755)
%{_bindir}/x*

%files vbox
%defattr(644,root,root,755)
%lang(de) %doc vbox/docs/*
%doc vbox/examples vbox/README vbox/CHANGES
%{_mandir}/*/*vbox*
%dir /var/spool/vbox
%dir /var/log/vbox
%config(noreplace) %{_sysconfdir}/isdn/vboxgetty.conf
%config(noreplace) %{_sysconfdir}/isdn/vboxd.conf
%defattr(755,root,root,755)
%{_bindir}/*vbox*
%{_sbindir}/vbox*

%files eurofile
%defattr(644,root,root,755)
%doc eurofile/doc/[!R]*[!5] eurofile/COPYING* eurofile/CHANGES eurofile/README* eurofile/TODO
%{_mandir}/man5/eft*.5*
%config(noreplace) %{_sysconfdir}/isdn/eft.conf
%defattr(755,root,root,755)
%config(noreplace) %{_initrddir}/eftd
%{_sbindir}/eftd
%{_bindir}/eftp

%files isdnlog
%defattr(644,root,root,755)
%doc isdnlog/BUGS isdnlog/README.* isdnlog/CREDITS isdnlog/FAQ isdnlog/NEWS isdnlog/TODO
%config(noreplace) %{_sysconfdir}/isdn/isdnlog.*
%{_mandir}/man1/isdn*
%{_mandir}/man5/isdnlog*.5*
%{_mandir}/man5/isdn.conf.5*
%{_mandir}/man5/callerid.conf.5*
%{_mandir}/man5/isdnformat.5*
%{_mandir}/man5/rate-files.5*
%{_mandir}/man8/isdnlog.8*
%defattr(755,root,root,755)
%{_sbindir}/isdnlog
%{_sbindir}/mkzonedb
%{_bindir}/isdn*
%config(noreplace) %{_sysconfdir}/isdn/stop

%files -n %{libname}
%defattr(644,root,root,755)
%doc COPYING README NEWS
%defattr(755,root,root,755)
%{_libdir}/libcapi*.la
%{_libdir}/libcapi*.so.%{major}*
# (blino) libcapi20.so filename is hardcoded in capidyn.c, used by capiplugin.so
%attr(755,root,root) %{_libdir}/libcapi*.so
%{_libdir}/pppd/%{pppd_ver}/*

%files -n %{develname}
%defattr(644,root,root,755)
%{_libdir}/libcapi*.a
%{_includedir}/capi*.h

%files doc
%lang(de) %doc FAQ/i4lfaq-de*
%doc FAQ/i4lfaq-[123456789]*.html FAQ/i4lfaq.*
