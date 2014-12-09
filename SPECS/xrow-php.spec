%define _PHPDIR /
%define _PHPNAME php54
Name: xrow-php
Summary: Tweaks for PHP 5.4
Version: 5.4
Release: 2
License: GPL
Group: Applications/Webservice
URL: http://packages.xrow.com/redhat
Distribution: Linux
Vendor: xrow GmbH
Packager: Bjoern Dieding / xrow GmbH <bjoern@xrow.de>
Requires(pre): policycoreutils-python
Requires(pre): php
Requires: httpd autoconf
Requires: php
Requires: php-devel php-bcmath php-devel php-enchant php-fpm php-gd php-imap php-intl php-ldap php-mbstring php-mysqlnd php-pdo php-pear php-process php-pspell php-soap php-tidy php-xml php-xmlrpc
Requires: php-pecl-ssh2 php-pecl-memcached php-pecl-http php-pecl-xdebug php-pecl-zendopcache
Source0: xrow-php.cron

BuildRoot: %{_tmppath}/%{name}-root
BuildArch: noarch

%description

Tweaks for PHP

%install

mkdir -p $RPM_BUILD_ROOT%{_bindir}

curl -s https://getcomposer.org/installer | /usr/bin/php -- --install-dir=$RPM_BUILD_ROOT%{_bindir} --filename=composer
curl -s http://pear2.php.net/pyrus.phar -o $RPM_BUILD_ROOT%{_bindir}/pyrus.phar

mkdir -p $RPM_BUILD_ROOT/usr/share/magallanes
wget https://github.com/andres-montanez/Magallanes/archive/master.zip -O magallanes.zip
unzip magallanes.zip
mv Magallanes-master/* $RPM_BUILD_ROOT/usr/share/magallanes
ln -sf /usr/share/magallanes/bin/mage ${RPM_BUILD_ROOT}/%{_bindir}
rm -Rf magallanes.zip Magallanes-master

cat <<EOL > $RPM_BUILD_ROOT%{_bindir}/pyrus
#!/bin/bash
/usr/bin/php -dphar.readonly=0 /usr/bin/pyrus.phar
EOL
chmod +x $RPM_BUILD_ROOT%{_bindir}/pyrus

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/cron.daily
cp %{SOURCE0} $RPM_BUILD_ROOT%{_sysconfdir}/cron.daily/xrow-php

%files
%defattr(-,root,root,-)
%{_bindir}/*
%attr(755,root,root) %{_sysconfdir}/cron.daily/*
%{_datadir}/*

%post

sed -i "s/display_errors[[:blank:]]*=.*$/display_errors = On/g" %{_PHPDIR}etc/php.ini
sed -i "s/short_open_tag[[:blank:]]*=.*$/short_open_tag = Off/g" %{_PHPDIR}etc/php.ini
sed -i "s/upload_max_filesize[[:blank:]]*=.*$/upload_max_filesize = 50M/g" %{_PHPDIR}etc/php.ini
sed -i "s/post_max_size[[:blank:]]*=.*$/post_max_size = 50M/g" %{_PHPDIR}etc/php.ini
sed -i "s/memory_limit[[:blank:]]*=.*$/memory_limit = 1024M/g" %{_PHPDIR}etc/php.ini
sed -i "s/;date.timezone[[:blank:]]*=.*$/date.timezone =Europe\/Berlin/g" %{_PHPDIR}etc/php.ini
sed -i "s/max_execution_time[[:blank:]]*=.*$/max_execution_time = 60/g" %{_PHPDIR}etc/php.ini
sed -i "s/zend_debugger.expose_remotely=2/zend_debugger.expose_remotely=0/g" %{_PHPDIR}etc/php.d/debugger.ini
sed -i "s/\/usr\/lib\/sendmail/\/usr\/sbin\/sendmail/g" %{_PHPDIR}etc/php.ini
sed -i "s/:\/usr\/local\/zend\/share\/ZendFramework\/library//g" %{_PHPDIR}etc/php.ini
sed -i "s/;extension=memcached.so/extension=memcached.so/g" %{_PHPDIR}etc/php.d/memcached.ini
sed -i "s/extension=memcache.so/;extension=memcache.so/g" %{_PHPDIR}etc/php.d/memcache.ini
sed -i "s/;extension=ssh2.so/extension=ssh2.so/g" %{_PHPDIR}etc/php.d/ssh2.ini

if [ -f /etc/httpd/conf.d/php.conf ]
then
 sed -i "s/LoadModule/#LoadModule/g" /etc/httpd/conf.d/php.conf
 sed -i "s/AddHandler/#AddHandler/g" /etc/httpd/conf.d/php.conf
 sed -i "s/AddType/#AddType/g" /etc/httpd/conf.d/php.conf
 sed -i "s/DirectoryIndex/#DirectoryIndex/g" /etc/httpd/conf.d/php.conf
fi

#sed -i "s/SELINUX=enforcing/SELINUX=disabled/g" /etc/selinux/config

%preun          

if [ $1 -eq 0 ]; then
 if [ -f /usr/local/zend/etc/conf.d/debugger.ini.disabled ] 
 then
  mv /usr/local/zend/etc/conf.d/debugger.ini.disabled /usr/local/zend/etc/conf.d/debugger.ini
 fi
 RETVAL='rpm -qa php'  
 if [ "$RETVAL" != "" ] && [ -f /etc/httpd/conf.d/php.conf ]
 then
  sed -i "s/#LoadModule/LoadModule/g" /etc/httpd/conf.d/php.conf
  sed -i "s/#AddHandler/AddHandler/g" /etc/httpd/conf.d/php.conf
  sed -i "s/#AddType/AddType/g" /etc/httpd/conf.d/php.conf
  sed -i "s/#DirectoryIndex/DirectoryIndex/g" /etc/httpd/conf.d/php.conf
 fi

 sed -i "s/display_errors = On/display_errors = Off/g" %{_PHPDIR}etc/php.ini
 sed -i "s/short_open_tag = Off/short_open_tag = On/g" %{_PHPDIR}etc/php.ini 
 sed -i "s/upload_max_filesize = 50M/upload_max_filesize = 2M/g" %{_PHPDIR}etc/php.ini
 sed -i "s/post_max_size = 50M/post_max_size = 8M/g" %{_PHPDIR}etc/php.ini
 sed -i "s/memory_limit = 512M/memory_limit = 128M/g" %{_PHPDIR}etc/php.ini
 sed -i "s/;date.timezone =/date.timezone =Europe\/Berlin/g" %{_PHPDIR}etc/php.ini
 sed -i "s/max_execution_time = 60/max_execution_time = 30/g" %{_PHPDIR}etc/php.ini
 sed -i "s/zend_debugger.expose_remotely=0/zend_debugger.expose_remotely=2/g" %{_PHPDIR}etc/php.d/debugger.ini
fi

%clean
rm -rf $RPM_BUILD_ROOT
