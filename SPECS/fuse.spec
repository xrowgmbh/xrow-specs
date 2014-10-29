Name:           fuse
Version:        2.9.3
Release:        4%{?dist}
Summary:        File System in Userspace (FUSE) utilities

Group:          System Environment/Base
License:        GPL+
URL:            http://fuse.sf.net
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       kernel >= 2.6.14
Requires:       which
BuildRequires:  libselinux-devel

Requires(pre): shadow-utils
Requires(preun): chkconfig
Requires(preun): initscripts

%description
With FUSE it is possible to implement a fully functional filesystem in a
userspace program. This package contains the FUSE userspace tools to
mount a FUSE filesystem.

%package libs
Summary:        File System in Userspace (FUSE) libraries
Group:          System Environment/Libraries
License:        LGPLv2+

%description libs
Devel With FUSE it is possible to implement a fully functional filesystem in a
userspace program. This package contains the FUSE libraries.


%package devel
Summary:        File System in Userspace (FUSE) devel files
Group:          Development/Libraries
Requires:       %{name}-libs = %{version}-%{release}
Requires:       pkgconfig
License:        LGPLv2+

%description devel
With FUSE it is possible to implement a fully functional filesystem in a
userspace program. This package contains development files (headers,
pgk-config) to develop FUSE based applications/filesystems.


%prep
%setup -q
#disable device creation during build/install
sed -i 's|mknod|echo Disabled: mknod |g' util/Makefile.in


%build
# Can't pass --disable-static here, or else the utils don't build
%configure \
 --libdir=/%{_lib} \
 --bindir=/bin \
 --exec-prefix=/
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
# change from 4755 to 0755 to allow stripping -- fixed later in files
chmod 0750 $RPM_BUILD_ROOT/bin/fusermount
# Put pc file in correct place
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mv $RPM_BUILD_ROOT/%{_lib}/pkgconfig $RPM_BUILD_ROOT%{_libdir}

# Get rid of static libs
rm -f $RPM_BUILD_ROOT/%{_lib}/*.a
# No need to create init-script
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/init.d/fuse

# Compatibility symlinks
mkdir -p $RPM_BUILD_ROOT%{_bindir}
cd $RPM_BUILD_ROOT%{_bindir}
ln -s /bin/fusermount fusermount
ln -s /bin/ulockmgr_server ulockmgr_server

%clean
rm -rf $RPM_BUILD_ROOT

%pre
getent group fuse >/dev/null || groupadd -r fuse
exit 0

%preun
if [ -f /etc/init.d/fuse ] ; then
    /sbin/service fuse stop >/dev/null 2>&1
    /sbin/chkconfig --del fuse
fi


%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING FAQ Filesystems NEWS README README.NFS
/sbin/mount.fuse
%attr(4750,root,fuse) /bin/fusermount
/bin/ulockmgr_server
# Compat symlinks
%{_bindir}/fusermount
%{_bindir}/ulockmgr_server
/usr/share/man/*
%config %{_sysconfdir}/udev/rules.d/99-fuse.rules

%files libs
%defattr(-,root,root,-)
%doc COPYING.LIB
/%{_lib}/libfuse.so.*
/%{_lib}/libulockmgr.so.*

%files devel
%defattr(-,root,root,-)
/%{_lib}/libfuse.so
/%{_lib}/libulockmgr.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/fuse.h
%{_includedir}/ulockmgr.h
%{_includedir}/fuse