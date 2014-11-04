%global php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%global php_extdir  %(php-config --extension-dir 2>/dev/null || echo "undefined")

Name:           php-ffmpeg
Version:        0.6.3
Release:        2
Summary:        Extension to manipulate movie in PHP

Group:          Development/Languages
License:        GPLv2
URL:            http://ffmpeg-php.sourceforge.net/
Patch0:         php-ffmpeg.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  ffmpeg-devel
BuildRequires:  re2c
Obsoletes:      ffmpeg-php <= %{version}
Provides:       ffmpeg-php = %{version}-%{release}

%if %{?php_zend_api}0
# for fedora >= 6
Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}
%else
# for fedora <= 5
Requires:       php-api = %{php_apiver}
%endif


%description
ffmpeg-php is an extension for PHP that adds an easy to use, object-oriented
API for accessing and retrieving information from video and audio files. 
It has methods for returning frames from movie files as images that can be 
manipulated using PHP's image functions. This works well for automatically 
creating thumbnail images from movies. ffmpeg-php is also useful for reporting
the duration and bitrate of audio files (mp3, wma...). ffmpeg-php can access
many of the video formats supported by ffmpeg (mov, avi, mpg, wmv...).


%prep

svn export --force https://ffmpeg-php.svn.sourceforge.net/svnroot/ffmpeg-php/trunk/ffmpeg-php/ .

#%patch0 -p1 -b .orig

# we will use include from php-devel
#rm gd.h gd_io.h


%build
phpize
%configure \
    --with-libdir=%{_lib} \
    --with-ffmpeg=%{_includedir}/ffmpeg \
    CFLAGS=-I%{_includedir}/php/ext/gd/libgd
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install INSTALL_ROOT=$RPM_BUILD_ROOT

# install config file
install -d $RPM_BUILD_ROOT%{_sysconfdir}/php.d
install -d $RPM_BUILD_ROOT/etc/conf.d
cat > $RPM_BUILD_ROOT%{_sysconfdir}/php.d/%{name}.ini << 'EOF'
; --- Enable %{name} extension module
extension=ffmpeg.so

; --- options for %{name} 
;ffmpeg.allow_persistent = 0
;ffmpeg.show_warnings = 0
EOF
cp $RPM_BUILD_ROOT%{_sysconfdir}/php.d/%{name}.ini $RPM_BUILD_ROOT/etc/conf.d 

%check
# should be run after install
#ldd modules/ffmpeg.so
#TEST_PHP_EXECUTABLE=$(which php) NO_INTERACTION=1 php -q -n \
#   -dextension_dir=$PWD/modules -dextension=gd.so -dextension=ffmpeg.so \
#   run-tests.php
# I know some tests fails
true


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc ChangeLog CREDITS EXPERIMENTAL LICENSE TODO test_ffmpeg.php
%config(noreplace) %{_sysconfdir}/php.d/%{name}.ini
%config(noreplace) /etc/conf.d/%{name}.ini
%{php_extdir}/ffmpeg.so


%changelog
* Sun Mar 21 2010 Remi Collet <rpms@famillecollet.com> 0.6.3-1.svn676
- update to 0.6.3 svn snapshot revision 676

* Wed Apr 23 2008 Remi Collet <rpms@famillecollet.com> 0.5.2.1-1
- update to 0.5.1.1

* Thu Nov 15 2007 Remi Collet <rpms@famillecollet.com> 0.5.1-2
- F8 rebuild

* Mon Aug 27 2007 Remi Collet <rpms@famillecollet.com> 0.5.1-2
- rename from ffmpeg-php to php-ffmpeg
- fix License

* Sat Jul 07 2007 Remi Collet <rpms@famillecollet.com> 0.5.1-1
- initial SPEC

