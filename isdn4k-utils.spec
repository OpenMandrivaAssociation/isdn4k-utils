%define	name		isdn4k-utils
%define	version		3.2p3
%define release		%mkrel 28
%define	lib_major	2
%define	lib_name	%mklibname %{name} %{lib_major}
%define	lib_name_dev	%{lib_name}-devel

%define pppd_ver	%(/usr/sbin/pppd --version 2>&1 | sed -n '/pppd version \\([0-9][.0-9]*\\)/s//\\1/p')
%define pppd_ver_num	%(echo %{pppd_ver} | perl -pe '/(\\d+)\\.(\\d)\\.?(\\d)?\\.?(\\d)?/; $_=($1)*1000000+($2)*10000+($3)*100+($4||0)')

Summary:	Bundled Utilities for configuring ISDN4Linux
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Epoch:		1
Group:		System/Configuration/Networking
Source0:	%{name}.v%{version}.tar.bz2
Source1:	%{name}-config
Source2:	capi4linux
Patch1:		%{name}.ipppd.patch
Patch2:		%{name}-capi4kutils-14062004.diff
Patch3:		%{name}-no-root.patch
Patch7:		%{name}-nomknod.patch
Patch9:		%{name}-glibc222.patch
Patch10:	%{name}-isdnlog.patch
Patch11:	%{name}-define.patch
Patch15:	%{name}-eurofile-init-fix.patch
Patch16:	%{name}-3.2p3-skip-capi-header-check.patch
Patch17:	isdn4k-utils-libtool.c-gcc-3.4.patch
Patch18:	isdn4k-utils-lib64.patch
Patch19:	isdn4k-utils-capifax-ALERT-fix.diff
Patch20:	isdn4k-utils-64bit-fixes.patch
Patch21:	isdn4k-utils-ppp244.patch
Patch22:	isdn4k-utils-gcc4.patch
URL:		http://www.isdn4linux.de/
Requires(post):		rpm-helper
Requires(preun):		rpm-helper
Requires:	kernel >= 2.2.0
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	ppp
BuildRequires:	gdbm-devel xpm-devel ncurses-devel kernel-source XFree86-devel imake
BuildRequires:	automake1.4 autoconf2.5 linuxdoc-tools libtcl-devel

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
Requires:	%{name} = %{epoch}:%{version}

%description	xtools
These are the graphical utilities for ISDN, xmonisdn and xisdnload.
They provide, each in their own way, a visual indication of the status
of the ISDN lines, so that it is directly obvious when there is a
connection, for example. 

%package	vbox
Summary:	ISDN answering machine
Group:		Communications
Requires:	%{name} = %{epoch}:%{version}

%description	vbox
ISDN Answering Machine

%package	eurofile
Summary:	ISDN eurofile transfer tool
Group:		Networking/File transfer
License:	LGPL
Requires:	%{name} = %{epoch}:%{version}
Requires(post):		rpm-helper
Requires(preun):		rpm-helper

%description	eurofile
If you want to send / receive files over an ISDN line with the eurofile system,
you need this package.

%package	isdnlog
Summary:	ISDN connection logger
Group:		Communications
Requires:	%{name} = %{epoch}:%{version}

%description	isdnlog
isdnlog logs all ISDN connections, and can calculate the cost of calls.
If sufficient data is available, it can even recommend which alternate
carrier would have been cheaper for a given call. For countries where calls
are charged per discrete unit, it can disconnect the line just before the
next unit starts. 

%package -n	%{lib_name}
Summary:	Main library for %{name}
Group:		System/Libraries
Requires:	%{name} = %{epoch}:%{version}

%description -n	%{lib_name}
isdn4k-utils is a collection of various ISDN related utilities. This
package contains configuration tools for all ISDN adapters, supported
by Linux. Furthermore, several status-monitors are provided as well as
some ISDN-based applications. Namely ipppd, a PPP daemon for synchronous
PPP over ISDN; vbox, an answering-machine and (for use with AVM-B1 only)
capifax, a faxmachine.
This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n	%{lib_name_dev}
Summary:	Includes and other files to develop %{name} applications
Group:		Development/C
Requires:	%{lib_name} = %{epoch}:%{version}
Provides:	lib%{name}-devel %{name}-devel

%description -n	%{lib_name_dev}
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
%setup -q -n %{name}
%patch1 -p1 -b .old
%patch2 -p1 -b .old
%patch3 -p1 -b .old
%patch7 -p1 -b .old
%patch9 -p1 -b .old
%patch10 -p0 -b .old
%patch11 -p1 -b .old
%patch15 -p0 -b .old
%patch16 -p1 -b .nocheck
%patch17 -p1 -b .gcc34
%patch18 -p1 -b .lib64
%patch19 -p0 -b .old
%patch20 -p1 -b .64bit-fixes
# (blino) copy the whole directory and replace 2.4.2 with current version
cp -a pppdcapiplugin/ppp-2.4.2 pppdcapiplugin/ppp-%{pppd_ver}
%patch21 -p1 -b .ppp244
perl -pi -e 's|(PLUGINDIR=\${DESTDIR})/usr/lib/(pppd/)|\1/\$(LIBDIR)/\2|' pppdcapiplugin/ppp-2.*/Makefile
%patch22 -p0 -b .gcc4

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

#(peroyvind) fix automake in capifax
cp %{_datadir}/automake-1.4/config.* capifax
cp %{_datadir}/automake-1.4/config.* rcapid
cp %{_datadir}/automake-1.4/config.* capiinit
cp %{_datadir}/automake-1.4/config.* capiinfo

# tcl hack
. %{_libdir}/tclConfig.sh
find -type f | xargs perl -pi -e "s|tcl8\.4|tcl${TCL_VERSION}|g"

%build
export FORCE_AUTOCONF_2_5=1
cd capi20; libtoolize --copy --force; aclocal-1.4; automake-1.4; cd -
cd capiinit; aclocal-1.4; automake-1.4; autoconf; cd - 
cd capifax; aclocal-1.4; automake-1.4; autoconf; cd -
cd capiinfo; aclocal-1.4; automake-1.4; autoconf; cd -


perl -pi -e "s|CONFIG_FAQDIR=.*|CONFIG_FAQDIR=\'%{_docdir}/%{name}-%{version}\'|" .config
#(peroyvind) added more flags for pppdcapiplugin since we're overriding it's CFLAGS which cointains flags needed
RPM_OPT_FLAGS="$RPM_OPT_FLAGS -DISDN_MAX_DRIVERS=32 -DISDN_MAX_CHANNELS=64 -fPIC -DPPPVER=%{pppd_ver_num} -I. -I`pwd`/capi20 -Ipppd -L`pwd`/capi20 -I./include"

#(peroyvind) workaround for wrong aclocal
make CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" CCFLAGS="$RPM_OPT_FLAGS" subconfig ACLOCAL=aclocal-1.4 AUTOMAKE=automake-1.4
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
rm -rf $RPM_BUILD_ROOT
RPM_OPT_FLAGS="$RPM_OPT_FLAGS -DISDN_MAX_DRIVERS=32 -DISDN_MAX_CHANNELS=64 -fPIC -DPPPVER=%{pppd_ver_num} -I. -I`pwd`/capi20 -Ipppd -L`pwd`/capi20 -I./include"
mkdir -p $RPM_BUILD_ROOT{%{_sbindir},%{_bindir},%{_includedir},%{_mandir},%{_docdir},/sbin,%{_initrddir},%{_libdir}/isdn}
#(peroyvind) yet another workaround.. this time for providing compile flags for stuff that was'nt compiled last time..
%{makeinstall_std} CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" CCFLAGS="$RPM_OPT_FLAGS" MANPATH=%{_mandir}
rm -f $RPM_BUILD_ROOT%{_bindir}/vboxbeep # security hole if used. (dam's)
rm -f $RPM_BUILD_ROOT%{_mandir}/man*/vboxbeep*
#(peroyvind) fix incorrect filename for man page
mv $RPM_BUILD_ROOT%{_mandir}/man8/.isdnctrl_conf.8 $RPM_BUILD_ROOT%{_mandir}/man8/isdnctrl_conf.8
#(peroyvind) move this one out of buildroot, we want to have it somewhere else..
rm -rf vbox/docs; mv $RPM_BUILD_ROOT%{_docdir}/vbox vbox/docs
#(peroyvind) fix name for init script
mv $RPM_BUILD_ROOT%{_initrddir}/eftd.sh $RPM_BUILD_ROOT%{_initrddir}/eftd
#(peroyvind) install man pages for eurofile
install -m644 eurofile/doc/*.5 $RPM_BUILD_ROOT%{_mandir}/man5/

#(peroyvind) remove uninstalled symlink
rm -rf $RPM_BUILD_ROOT/usr/lib/X11/app-defaults
rm -f  $RPM_BUILD_ROOT%{_sysconfdir}/isdn/eftusers

install -m755 %{SOURCE2} $RPM_BUILD_ROOT%{_initrddir}/capi4linux

#(peroyvind) get rid of drdsl files which are provided by other package according to Steffen Barszus
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/drdsl

# cleanup
rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%_post_service capi4linux

%preun
%_preun_service capi4linux

%post -n %{lib_name} -p /sbin/ldconfig
%postun -n %{lib_name} -p /sbin/ldconfig

%post eurofile
%_post_service eftd

%preun eurofile
%_preun_service eftd

%files
%defattr(644,root,root,755)
%doc README NEWS
%dir %{_libdir}/isdn
%dir %{_datadir}/isdn
%{_datadir}/isdn/*
%dir %{_sysconfdir}/isdn
%{_initrddir}/capi4linux
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

%files -n %{lib_name}
%defattr(644,root,root,755)
%doc COPYING README NEWS
%defattr(755,root,root,755)
%{_libdir}/libcapi*.la
%{_libdir}/libcapi*.so.*
# (blino) libcapi20.so filename is hardcoded in capidyn.c, used by capiplugin.so
%attr(755,root,root) %{_libdir}/libcapi*.so
%{_libdir}/pppd/%{pppd_ver}/*

%files -n %{lib_name_dev}
%defattr(644,root,root,755)
%{_libdir}/libcapi*.a
%{_includedir}/capi*.h

%files doc
%lang(de) %doc FAQ/i4lfaq-de*
%doc FAQ/i4lfaq-[123456789]*.html FAQ/i4lfaq.*
