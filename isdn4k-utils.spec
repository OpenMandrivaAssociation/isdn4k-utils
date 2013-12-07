%define api	20
%define major	3
%define oldlib	%mklibname %{name} %{major}
%define olddev	%mklibname %{name} -d

%define	libname	%mklibname capi %{api} %{major}
%define	devname	%mklibname capi %{api} -d

%define pppd_ver %(/usr/sbin/pppd --version 2>&1 | sed -n '/pppd version \\([0-9][.0-9]*\\)/s//\\1/p')
%define pppd_ver_num %(echo %{pppd_ver} | perl -pe '/(\\d+)\\.(\\d)\\.?(\\d)?\\.?(\\d)?/; $_=($1)*1000000+($2)*10000+($3)*100+($4||0)')

Summary:	Bundled Utilities for configuring ISDN4Linux
Name:		isdn4k-utils
Epoch:		1
Version:	3.12
Release:	16
License:	GPLv2
Group:		System/Configuration/Networking
Url:		http://www.isdn4linux.de/
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
#Patch21:	isdn4k-utils-ppp244.patch
Patch23:	isdn4k-utils-target.patch
# capi20.h must #include sys/types.h - AdamW 2008/02
Patch24:	isdn4k-utils-3.2p3-types.patch
Patch25:	isdn4k-utils-autoconf25x.diff
Patch26:	isdn4k-utils-cleanup.diff
Patch27:	isdn4k-utils-openssl_des.h_fix.diff
Patch28:	isdn4k-utils-fix-str-fmt.patch
Patch29:	isdn4k-utils-tcl86.patch
Patch30:	isdn4k-utils-autoconf-2.6.4-quoting.patch
Patch31:	isdn4k-utils-CVS-2010-05-01-capi.patch
Patch32:	isdn4k-utils-automake-1.13-fixes.patch

BuildRequires:	imake
BuildRequires:	kernel-source
BuildRequires:	libtool
BuildRequires:	linuxdoc-tools
BuildRequires:	ppp
BuildRequires:	gdbm-devel
BuildRequires:	pcap-devel
BuildRequires:	ppp-devel
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(tcl)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xaw7)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xmu)
BuildRequires:	pkgconfig(xpm)
BuildRequires:	pkgconfig(xt)
Requires(post,preun):	rpm-helper
Conflicts:	%{oldlib} < 1:3.12-11

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
Requires:	%{name} >= %{EVRD}

%description	xtools
These are the graphical utilities for ISDN, xmonisdn and xisdnload.
They provide, each in their own way, a visual indication of the status
of the ISDN lines, so that it is directly obvious when there is a
connection, for example. 

%package	vbox
Summary:	ISDN answering machine
Group:		Communications
Requires:	%{name} >= %{EVRD}

%description	vbox
ISDN Answering Machine

%package	eurofile
Summary:	ISDN eurofile transfer tool
Group:		Networking/File transfer
License:	LGPLv2
Requires:	%{name} >= %{EVRD}
Requires(post,preun): rpm-helper

%description	eurofile
If you want to send / receive files over an ISDN line with the eurofile system,
you need this package.

%package	isdnlog
Summary:	ISDN connection logger
Group:		Communications
Requires:	%{name} >= %{EVRD}

%description	isdnlog
isdnlog logs all ISDN connections, and can calculate the cost of calls.
If sufficient data is available, it can even recommend which alternate
carrier would have been cheaper for a given call. For countries where calls
are charged per discrete unit, it can disconnect the line just before the
next unit starts. 

%package -n	%{libname}
Summary:	Main library for %{name}
Group:		System/Libraries
%rename		%{oldlib}
Conflicts:	%{name} < 1:3.12-11

%description -n	%{libname}
isdn4k-utils is a collection of various ISDN related utilities. This
package contains configuration tools for all ISDN adapters, supported
by Linux. Furthermore, several status-monitors are provided as well as
some ISDN-based applications. Namely ipppd, a PPP daemon for synchronous
PPP over ISDN; vbox, an answering-machine and (for use with AVM-B1 only)
capifax, a faxmachine.
This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n	%{devname}
Summary:	Includes and other files to develop %{name} applications
Group:		Development/C
Requires:	%{libname} >= %{EVRD}
Provides:	%{name}-devel %{EVRD}
Conflicts:	%{_lib}isdn4k-utils3 < 1:3.12-7mdv
%rename		%{olddev}

%description -n	%{devname}
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
%setup -qn %{name} -a3
%apply_patches

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0554 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;

for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

# (simpler) lib64 fix
sed -i -e "s|/usr/lib/|%{_libdir}/|" pppdcapiplugin/ppp-2.*/Makefile pppdcapiplugin/Makefile.template

#(peroyvind) provide our own config file with correct options and paths
install %{SOURCE1} .config
echo "LIBDIR='%{_libdir}'" >> .config

# AMD K6 is not an i686
%ifarch
sed -i -e "s/k6 \| //" vbox3/config.sub
sed -i -e "s/k6-\* \| //" vbox3/config.sub
sed -i -e "s/\| k5 \|/\| k5 \| k6 \|/" vbox3/config.sub
sed -i -e "s/\| k5-\* \|/\| k5-\* \| k6-* \|/" vbox3/config.sub
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
	autoreconf -fi
    cd ..
done

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
sed -i -e "s|CDEBUGFLAGS = .*|CDEBUGFLAGS = $RPM_OPT_FLAGS|" xisdnload/Makefile xmonisdn/Makefile
sed -i -e "s|CXXDEBUGFLAGS = \-0.*|CXXDEBUGFLAGS = $RPM_OPT_FLAGS|" xisdnload/Makefile xmonisdn/Makefile
cp isdnlog/isdnlog/isdnlog.5.in isdnlog/isdnlog/isdnlog.5

#(peroyvind) workaround for non-existing rcapid/acinclude.m4
touch rcapid/acinclude.m4

# (blino) compile pppdcapiplugin for current pppd only to avoid errors and unnecessary time spent on compiling
sed -i -e "s|^(PPPVERSIONS\s*)=\s*.+$|\1= %{pppd_ver}|" pppdcapiplugin/Makefile

#(peroyvind) added CCFLAGS since it's a variable used a few places in stead of CFLAGS (*sigh*)
make CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" CCFLAGS="$RPM_OPT_FLAGS" || make CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" CCFLAGS="$RPM_OPT_FLAGS"

%install
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

# cleanup
rm -f %{buildroot}/usr/share/doc/i4lfaq*
rm -f %{buildroot}%{_libdir}/*.*a

# hmm...
mv %{buildroot}/sbin/* %{buildroot}%{_sbindir}/

%post
%_post_service capi4linux

%preun
%_preun_service capi4linux

%post eurofile
%_post_service eftd

%preun eurofile
%_preun_service eftd

%files
%doc README NEWS
%{_libdir}/pppd/%{pppd_ver}/*
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
%{_mandir}/man4/isdn_audio.4*
%{_mandir}/man4/isdnctrl.4*
%{_mandir}/man4/isdninfo.4*
%{_mandir}/man4/ttyI.4*
%{_mandir}/man5/rate.conf.5*
%{_mandir}/man7/isdn_cause.7*
%{_mandir}/man8/actctrl.8*
%{_mandir}/man8/avmcapictrl.8*
%{_mandir}/man8/capiinfo.8*
%{_mandir}/man8/capiplugin.8*
%{_mandir}/man8/divertctrl.8*
%{_mandir}/man8/eiconctrl.8*
%{_mandir}/man8/hisaxctrl.8*
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

%files xtools
%doc xmonisdn/README
%{_includedir}/X11/bitmaps/net*
#%{_prefix}/X11R6/lib/X11/doc/html/*.html
%config(noreplace) %{_sysconfdir}/X11/app-defaults/XISDNLoad
%{_bindir}/x*
%{_mandir}/man1/xisdnload.1x.*
%{_mandir}/man1/xmonisdn.1x.*

%files vbox
%lang(de) %doc vbox/docs/*
%doc vbox/examples vbox/README vbox/CHANGES
%dir /var/spool/vbox
%dir /var/log/vbox
%config(noreplace) %{_sysconfdir}/isdn/vboxgetty.conf
%config(noreplace) %{_sysconfdir}/isdn/vboxd.conf
%{_bindir}/*vbox*
%{_sbindir}/vbox*
%{_mandir}/man1/vbox.1*
%{_mandir}/man1/vboxconvert.1*
%{_mandir}/man1/vboxctrl.1*
%{_mandir}/man1/vboxmode.1*
%{_mandir}/man1/vboxplay.1*
%{_mandir}/man1/vboxtoau.1*
%{_mandir}/man5/vbox.conf.5*
%{_mandir}/man5/vboxd.conf.5*
%{_mandir}/man5/vbox_file.5*
%{_mandir}/man5/vboxgetty.conf.5*
%{_mandir}/man5/vboxrc.5*
%{_mandir}/man5/vboxtcl.5*
%{_mandir}/man8/vboxd.8*
%{_mandir}/man8/vboxgetty.8*
%{_mandir}/man8/vboxmail.8*
%{_mandir}/man8/vboxputty.8*

%files eurofile
%doc eurofile/doc/[!R]*[!5] eurofile/COPYING* eurofile/CHANGES eurofile/README* eurofile/TODO
%config(noreplace) %{_sysconfdir}/isdn/eft.conf
%defattr(755,root,root,755)
%config(noreplace) %{_initrddir}/eftd
%{_sbindir}/eftd
%{_bindir}/eftp
%{_mandir}/man5/eftaccess.5*
%{_mandir}/man5/efthosts.5*
%{_mandir}/man5/eft_wuauth.5*
%{_mandir}/man5/eft_xferlog.5*

%files isdnlog
%doc isdnlog/BUGS isdnlog/README.* isdnlog/CREDITS isdnlog/FAQ isdnlog/NEWS isdnlog/TODO
%config(noreplace) %{_sysconfdir}/isdn/isdnlog.*
%defattr(755,root,root,755)
%{_sbindir}/isdnlog
%{_sbindir}/mkzonedb
%{_bindir}/isdn*
%config(noreplace) %{_sysconfdir}/isdn/stop
%{_mandir}/man1/autovbox.1*
%{_mandir}/man1/isdnbill.1*
%{_mandir}/man1/isdnconf.1*
%{_mandir}/man1/isdnrate.1*
%{_mandir}/man1/isdnrep.1*
%{_mandir}/man1/rmdtovbox.1*
%{_mandir}/man5/callerid.conf.5*
%{_mandir}/man5/isdn.conf.5*
%{_mandir}/man5/isdnformat.5*
%{_mandir}/man5/isdnlog.5*
%{_mandir}/man5/isdnlog.users.5*
%{_mandir}/man5/rate-files.5*
%{_mandir}/man8/isdnlog.8*
%{_mandir}/man8/mkzonedb.8*

%files -n %{libname}
%{_libdir}/libcapi%{api}.so.%{major}*

%files -n %{devname}
%doc COPYING README NEWS
%attr(755,root,root) %{_libdir}/libcapi*.so
%{_includedir}/capi*.h

%files doc
%lang(de) %doc FAQ/i4lfaq-de*
%doc FAQ/i4lfaq-[123456789]*.html FAQ/i4lfaq.*

