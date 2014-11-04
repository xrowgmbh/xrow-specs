#
# spec file for package libvo-aacenc
#

%define soname 0
%define bname vo-aacenc
Name:           lib%{bname}
Version:        0.1.2
Release:        6
License:        Apache License 2.0
Summary:        VisualOn AAC encoder library
Url:            http://www.webmproject.org/
Group:          Productivity/Multimedia/Other
Source:         %{bname}-%{version}.tar.gz
BuildRequires:  yasm gcc
BuildRequires:  make >= 3.81
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
This library contains an encoder implementation of the Advanced Audio
Coding (AAC) audio codec. The library is based on a codec implementation
by VisualOn as part of the Stagefright framework from the Google
Android project.

%package devel
License:        Apache License 2.0
Summary:        VisualOn AAC encoder library - Development headers
Group:          Development/Languages/C and C++
Requires:       %{name} = %{version}

%description devel
Development headers and library

This library contains an encoder implementation of the Advanced Audio
Coding (AAC) audio codec. The library is based on a codec implementation
by VisualOn as part of the Stagefright framework from the Google
Android project.

%prep
%setup -q -n %{bname}-%{version}

%build
export CFLAGS="%{optflags}"
# It is only an emulation of autotools configure; the macro does not work
autoreconf --force
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --enable-shared 
make %{?_smp_mflags}

%install
%makeinstall

%clean
rm -rf %{buildroot}

%post -n %{name} -p /sbin/ldconfig

%postun -n %{name} -p /sbin/ldconfig

%files -n %{name}
%defattr(-, root, root)
%doc COPYING README ChangeLog NOTICE
%{_libdir}/libvo-aacenc.so.0*

%files devel
%defattr(-,root,root)
%{_includedir}/vo-aacenc/
%{_libdir}/libvo-aacenc.so
%{_libdir}/pkgconfig/vo-aacenc.pc
%{_libdir}/libvo-aacenc.a
%{_libdir}/libvo-aacenc.la

%changelog
* Fri Sep 02 2011 - Michele Catalano <michele.catalano@mayflower.de>
- initial with version 0.1.1
