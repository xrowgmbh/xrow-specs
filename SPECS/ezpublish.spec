Name: ezpublish
Summary: eZ Publish dependancies
Version: 4.7
Release: 5
License: GPL
Group: Applications/Webservice
URL: http://ez.no
Distribution: Linux
Vendor: eZ Systems
Packager: Bjoern Dieding / xrow GmbH <bjoern@xrow.de>
Requires: ImageMagick, xpdf
Requires: crontabs
Requires: git, telnet, lynx, nano, subversion, bind-utils, sysstat, sudo, fontforge
Requires: memcached, varnish, redis
BuildRoot: %{_tmppath}/%{name}-root
BuildArch: noarch

%description
eZ Publish dependancies

%install

%files
%defattr(-,root,root)


%post
if [ $1 -eq 1 ]; then
    /sbin/chkconfig httpd on
    /sbin/chkconfig memcached on
    /sbin/chkconfig varnishncsa off
    /sbin/chkconfig varnishlog off
    /sbin/chkconfig varnish on
fi

%preun
if [ $1 -eq 0 ]; then
   echo "You might what to disable at boot http"
   #/sbin/chkconfig httpd off
   #/sbin/chkconfig memcached off
fi 

%clean
rm -rf $RPM_BUILD_ROOT
