%global php_extdir  %(php-config --extension-dir 2>/dev/null || echo "undefined")
%global php_inidir  %(php-config --configure-options | sed "s/.*with-config-file-scan-dir=//" | sed "s/[[:space:]]--.*//" 2>/dev/null || echo "undefined")

Name:           php-zend-debugger
Version:        6.0
Release:        1
Summary:        Extension to debug PHP

Group:          Development/Languages
License:        GPLv2
URL:            http://www.zend.com/
Source0:        debugger.ini
Source1:        ZendDebugger.so
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Conflicts:      php-pecl-xdebug

%description
Extension to debug PHP

%install

# install config file
install -d $RPM_BUILD_ROOT%{php_inidir}
install -d $RPM_BUILD_ROOT%{php_extdir}
cp %{SOURCE0} $RPM_BUILD_ROOT%{php_inidir}
cp %{SOURCE1} $RPM_BUILD_ROOT%{php_extdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%config(noreplace) %{php_inidir}/debugger.ini
%defattr(755,root,root,-)
%{php_extdir}/ZendDebugger.so
