%define _PHPDIR /
Name: php-composer
Summary: Composer for PHP
Version: 1.0.1
Release: 1
License: GPL
Group: Applications/Webservice
URL: http://packages.xrow.com/redhat
Distribution: Linux
Vendor: xrow GmbH
Packager: Bjoern Dieding / xrow GmbH <bjoern@xrow.de>
Requires(pre): policycoreutils-python
Requires(pre): php
BuildRoot: %{_tmppath}/%{name}-root
BuildArch: noarch

%description

Composer for PHP

%install

mkdir -p $RPM_BUILD_ROOT%{_bindir}

curl -s https://getcomposer.org/installer | %{_PHPDIR}usr/bin/php -- --install-dir=$RPM_BUILD_ROOT%{_bindir} --filename=composer

mkdir -p $RPM_BUILD_ROOT/usr/share/magallanes
wget https://github.com/xrowgmbh/Magallanes/archive/master.zip -O magallanes.zip
unzip magallanes.zip
mv Magallanes-master/* $RPM_BUILD_ROOT/usr/share/magallanes
ln -sf /usr/share/magallanes/bin/mage ${RPM_BUILD_ROOT}%{_bindir}
rm -Rf magallanes.zip Magallanes-master

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_datadir}/*

%post

# Update composer after install
/usr/bin/composer self-update

%clean
rm -rf $RPM_BUILD_ROOT
