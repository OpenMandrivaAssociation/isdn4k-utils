%define major 3
%define oldlib	%mklibname %{name} %{major}
%define olddev	%mklibname %{name} -d

%define	libname	%mklibname capi20_ %{major}
%define	devname	%mklibname capi20 -d

%define pppd_ver %(/usr/sbin/pppd --version 2>&1 | sed -n '/pppd version \\([0-9][.0-9]*\\)/s//\\1/p')
%define pppd_ver_num %(echo %{pppd_ver} | perl -pe '/(\\d+)\\.(\\d)\\.?(\\d)?\\.?(\\d)?/; $_=($1)*1000000+($2)*10000+($3)*100+($4||0)')

Summary:	Bundled Utilities for configuring ISDN4Linux
Name:		isdn4k-utils
Version:	3.12
Release:	11
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
Patch28:	isdn4k-utils-fix-str-fmt.patch
Patch29:	isdn4k-utils-tcl86.patch
Patch30:	isdn4k-utils-autoconf-2.6.4-quoting.patch
Patch31:	isdn4k-utils-CVS-2010-05-01-capi.patch
Patch32:	isdn4k-utils-automake-1.13-fixes.patch
Requires(post): rpm-helper
Requires(preun):rpm-helper
Conflicts:	%{oldlib} < 1:3.12-11
BuildRequires:	autoconf automake libtool
BuildRequires:	gdbm-devel
BuildRequires:	imake
BuildRequires:	kernel-source
BuildRequires:	tcl-devel
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
BuildRequires:	libx11-devel
BuildRequires:	libxaw-devel
BuildRequires:	libxext-devel
BuildRequires:	libxmu-devel
BuildRequires:	libxpm-devel
BuildRequires:	libxp-devel
BuildRequires:	libxt-devel

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
# There's a ton of non-versioned libs, plugins and development files
# in the library package, so it needs to obsolete its old major(s)
# In fact, if this isn't going to be fixed, there's really no point
# versioning the lib package at all.
# - AdamW 2008/10
Obsoletes:	%{mklibname isdn4k-utils 2} <= 1:3.2p3-38mdv2009.0
%rename		%{oldlib}

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
Requires:	%{libname} >= %{epoch}:%{version}-%{release}
Provides:	lib%{name}-devel %{name}-devel
Obsoletes:	%{mklibname %{name} -d 2}
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

%patch28 -p0 -b .str
%patch29 -p0 -b .tcl86
%patch30 -p1 -b .autoconf
%patch31 -p1 -b .capi
%patch32 -p1 -b .am113~

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
%defattr(755,root,root,755)
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
%defattr(755,root,root,755)
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
%doc COPYING README NEWS
%defattr(755,root,root,755)
%{_libdir}/libcapi*.so.%{major}*
%{_libdir}/pppd/%{pppd_ver}/*

%files -n %{devname}
%attr(755,root,root) %{_libdir}/libcapi*.so
%{_includedir}/capi*.h

%files doc
%lang(de) %doc FAQ/i4lfaq-de*
%doc FAQ/i4lfaq-[123456789]*.html FAQ/i4lfaq.*


%changelog
* Tue Jan 17 2012 Oden Eriksson <oeriksson@mandriva.com> 1:3.12-10
+ Revision: 761942
- one more fix...
- fix file lists
- various fixes

* Mon Nov 28 2011 Oden Eriksson <oeriksson@mandriva.com> 1:3.12-9
+ Revision: 734985
- relink against new pcap

* Tue Apr 19 2011 Funda Wang <fwang@mandriva.org> 1:3.12-8
+ Revision: 655901
- tweak br

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuild

* Wed May 05 2010 Funda Wang <fwang@mandriva.org> 1:3.12-7mdv2010.1
+ Revision: 542280
- fix capidyn.c, hardcode libmajor instead of libname
- fix build with autoconf 2.6

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuilt against openssl-0.9.8m

* Sat Mar 28 2009 Funda Wang <fwang@mandriva.org> 1:3.12-5mdv2009.1
+ Revision: 361911
- fix str fmt
- rebuild for tcl 8.6
- rediff types patch
- BR tcl-devel
- rediff glibc patch
- rediff nomknod patch

* Thu Oct 30 2008 Adam Williamson <awilliamson@mandriva.org> 1:3.12-4mdv2009.1
+ Revision: 298810
- fix the obsolete to really work (38mdv2009.0 is greater than 38mdv)

* Wed Oct 29 2008 Oden Eriksson <oeriksson@mandriva.com> 1:3.12-3mdv2009.1
+ Revision: 298264
- rebuilt against libpcap-1.0.0

* Thu Oct 23 2008 Adam Williamson <awilliamson@mandriva.org> 1:3.12-2mdv2009.1
+ Revision: 296769
- lib package must obsolete old major, as it contains unversioned libs

* Thu Oct 16 2008 Oden Eriksson <oeriksson@mandriva.com> 1:3.12-1mdv2009.1
+ Revision: 294143
- bump release

* Sat Oct 11 2008 Oden Eriksson <oeriksson@mandriva.com> 1:3.12-0.1mdv2009.1
+ Revision: 291874
- 3.12 (latest, synced with fedora)
- drop obsolete patches; P2,P17,P19,P22
- fix deps

* Thu Jul 31 2008 Oden Eriksson <oeriksson@mandriva.com> 1:3.2p3-38mdv2009.0
+ Revision: 258105
- rebuild
- rebuild

* Thu Jun 19 2008 Oden Eriksson <oeriksson@mandriva.com> 1:3.2p3-36mdv2009.0
+ Revision: 226233
- bump release
- added a temporary hack to find out why the bs won't play nice...
- fix devel package naming and other stuff
- rebuild

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - remove useless kernel require

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

  + Adam Williamson <awilliamson@mandriva.org>
    - add types.patch (fixes 'size_t has not been declared' errors when building against capi20h.)

* Fri Jan 04 2008 Olivier Blin <blino@mandriva.org> 1:3.2p3-31mdv2008.1
+ Revision: 144850
- bump release
- restore BuildRoot
- fix output of "service capi4linux status"
- add LSB header in initscript
- fix permission of capi4linux service so that it can be enabled again (got broken in revision 54938)

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - buildrequires X11-devel instead of XFree86-devel

* Fri Sep 07 2007 Anssi Hannula <anssi@mandriva.org> 1:3.2p3-30mdv2008.0
+ Revision: 82017
- rebuild for new soname of tcl

* Tue Jul 24 2007 Olivier Blin <blino@mandriva.org> 1:3.2p3-29mdv2008.0
+ Revision: 54992
- add patch to fix target check in FAQ install rule and make CONFIG_FAQDIR empty

* Tue Jul 24 2007 Oden Eriksson <oeriksson@mandriva.com> 1:3.2p3-28mdv2008.0
+ Revision: 54956
- nuke installed docs
- make it find latest tcl
- resync with the src.rpm file in cooker with changes committed by blino:
  - do not mark capi4linux service as config file
  - bunzip2 sources and patches
  - drop unused patches
  - fix build with ppp 2.4.4
  - move doc in a separate isdn4k-utils-doc package


* Wed Sep 27 2006 Olivier Blin <blino@mandriva.com> 3.2p3-28mdv2007.0
- rebuild for ncurses

* Sat Aug 05 2006 Thierry Vignaud <tvignaud@mandriva.com> 3.2p3-27mdv2007.0
- fix buildrequires
- fix build on x86_64

* Sat Aug 05 2006 Olivier Blin <blino@mandriva.com> 3.2p3-26mdv2007.0
- don't require X11 (not provided anymore, and not really needed anyway)
- adapt to new X11 layout

* Fri Jan 20 2006 Olivier Blin <oblin@mandriva.com> 3.2p3-25mdk
- remove requires on release
- convert prereq to requires(X)

* Fri Jan 20 2006 Christiaan Welvaart <cjw@daneel.dyndns.org> 3.2p3-24mdk
- fix buildrequires: tcl -> libtcl-devel

* Sun Jan 01 2006 Oden Eriksson <oeriksson@mandriva.com> 3.2p3-23mdk
- rebuilt against soname aware deps

* Sat Dec 31 2005 Mandriva Linux Team <http://www.mandrivaexpert.com/> 3.2p3-22mdk
- Rebuild

* Fri Jul 22 2005 Olivier Blin <oblin@mandriva.com> 1:3.2p3-21mdk
- Patch22: gcc4 fixes
- force autoconf for capifax as well
- create /dev/capi20 in init script (Source2) if it doesn't exist

* Fri Apr 08 2005 Olivier Blin <oblin@mandrakesoft.com> 3.2p3-20mdk
- Source2 (update): trigger capi device creation by calling capiinit twice

* Wed Apr 06 2005 Olivier Blin <oblin@mandrakesoft.com> 3.2p3-19mdk
- Patch21: really build capiplugin for pppd 2.4.3

* Thu Jan 20 2005 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 3.2p3-18mdk
- rebuild for new readline
- fix build with current ppp

* Wed Dec 22 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 3.2p3-17mdk
- fix buildrequires
- prereq on rpm-helper
- mark capi4linux init file as config

* Tue Sep 21 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.2p3-16mdk
- build & 64-bit fixes
- BuildPreReq: ppp (pppd)

* Tue Sep 14 2004 Olivier Blin <blino@mandrake.org> 3.2p3-15mdk
- add capi4linux service

* Thu Sep 09 2004 Olivier Blin <blino@mandrake.org> 3.2p3-14mdk
- own %%{_libdir}/isdn

* Thu Jul 29 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 3.2p3-13mdk
- get rid of drdsl files which are provided by other package according to Steffen Barszus

* Sat Jul 24 2004 Olivier Blin <blino@mandrake.org> 3.2p3-12mdk
- move libcapi20.so in lib package (needed by capiplugin.so)

* Fri Jul 23 2004 Olivier Blin <blino@mandrake.org> 3.2p3-11mdk
- replace patch14 with a perl one-liner, easier to update
- put plugins in current pppd dir, define pppd_ver (2.4.2)

* Wed Jul 14 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 3.2p3-10mdk
- from Steffen Barszus <st_barszus@gmx.de>:
	o moved patch 2 to patch 3 for capi4k-utils update
	o added patch 2 for update of capi4k-utils to make them kernel 2.6 compatible
	o rediffed patch 14
	o added patch 19 - fix capifax compilation
	o corrected spec to use the updated P16 actually

* Fri Jul 02 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.2p3-9mdk
- fix gcc3.4 patch
- lib64 fixes unmerged from maintainer

* Wed Jun 30 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 3.2p3-8mdk
- fix gcc-3.4 build (P17 from Laurent Montel)
- skip all checks for linux/capi.h (updated P16)
- force use of autoconf2.5 and automake1.4

* Sat Jun 05 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 3.2p3-7mdk
- rebuild

* Sun Feb 29 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 3.2p3-6mdk
- fix automake
- fix requires
- fix buildrequires(lib64..)
- skip check for linux/capi.h (P16)
- added docs
- added init script to post{,un} for eurofile

