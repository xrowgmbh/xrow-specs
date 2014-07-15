%define extname ezpublish-ezodf

Name:           ezpublish-ezodf
Version:        2.4
Release:        6
Summary:        Import and Export Libreoffice, Word and PDF
Group:          Applications/Productivity
License:        GPLv2+
URL:            https://github.com/ezsystems/ezodf
Source0:        eZconversion.zip
Source1:        converttooo.php
Source2:        ezpublish-odf
Source3:        DisableFirstStartWzd.oxt
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
Requires: xinetd
Requires: libreoffice-core
Requires: libreoffice-writer
Requires: libreoffice-headless
#Requires: xorg-x11-server-Xvfb

%description
Import and Export Libreoffice, Word and PDF

%prep
rm -Rf %{name}-%{version}
mkdir %{name}-%{version}
#%setup -q -n ezpublish-ezodf
unzip -d %{name}-%{version} %{SOURCE0}

%install
#rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_datadir}/openoffice.org/extensions/%{extname}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/ezodf
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/xinetd.d/
mkdir -p $RPM_BUILD_ROOT%{_bindir}
\cp -a %{name}-%{version}/* $RPM_BUILD_ROOT%{_datadir}/openoffice.org/extensions/%{extname}
\cp %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/ezp-converttooo
\cp %{SOURCE0} $RPM_BUILD_ROOT%{_datadir}/ezodf/eZconversion.zip
\cp %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/ezodf/DisableFirstStartWzd.oxt
install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/xinetd.d/%{name}

# Cleanup patch backups
find $RPM_BUILD_ROOT%{_datadir}/openoffice.org/extensions/%{extname} -name \*.orig -exec rm '{}' \;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%attr(644,root,root) %{_sysconfdir}/xinetd.d/*
%{_datadir}/*
%{_bindir}/*

%post
unopkg add --shared /usr/share/ezodf/eZconversion.zip
unopkg add --shared /usr/share/ezodf/DisableFirstStartWzd.oxt
/etc/init.d/xinetd restart

%postun
unopkg remove --shared org.openoffice.legacy.eZconversion.zip
unopkg remove --shared org.openoffice.legacy.DisableFirstStartWzd.oxt
/etc/init.d/xinetd restart
