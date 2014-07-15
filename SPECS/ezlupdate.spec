Summary: ezlupdate
Name: ezlupdate
Version: 4.6.0
Release: 11
License: GPL
Group: Applications/Webservice
URL: https://github.com/ezsystems/ezpublish
Distribution: Linux
Vendor: eZ Systems
Packager: Bjoern Dieding / xrow GmbH <bjoern@xrow.de>
Requires: qt
BuildRequires: qt-devel >= 4.5, gcc-c++, git
BuildRoot: %{_tmppath}/%{name}-root
BuildArch: x86_64
%description
ezlupdate

%prep
rm -Rf ezlupdate-%{version}
env GIT_SSL_NO_VERIFY=true git clone https://github.com/ezsystems/ezpublish-legacy.git ezlupdate-%{version}
rm -Rf ezupdate-%{version}/.git
rm -Rf ezupdate-%{version}/.gitignore
cd  ezlupdate-%{version}/support/ezlupdate-qt4.5/ezlupdate
sed -i "s/..\/..\/..\/bin\/linux/.\//g" ezlupdate.pro
/usr/lib64/qt4/bin/qmake ezlupdate.pro
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
cp ezlupdate-%{version}/support/ezlupdate-qt4.5/ezlupdate/ezlupdate $RPM_BUILD_ROOT%{_bindir}

%files
%defattr(755,root,root)
%{_bindir}/ezlupdate

%changelog

%clean
rm -rf $RPM_BUILD_ROOT
