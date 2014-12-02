Summary: eZ Find Solr Service
Name: ezfind-solr
Epoch: 54
Version: 5.4
Release: 41
License: GPL
Group: Applications/Webservice
Source1: ezfind.initd
Source2: stopwords.txt
Source3: mysql-connector-java-5.1.15-bin.jar
Source4: SOLRCLEAN
Source5: ezfind.logrotate
URL: http://ez.no/ezfind
Distribution: Linux
Vendor: eZ Systems
Packager: Bjoern Dieding / xrow GmbH <bjoern@xrow.de>
Requires: java-1.7.0-openjdk
Conflicts: ezfind-solr23 ezfind-solr25 ezfind-solr27 ezfind-solr50  ezfind-solr51 ezfind-solr52 
Conflicts: ezfind-solr < 54:5.4

BuildRoot: %{_tmppath}/%{name}-root
BuildArch: noarch
%description
eZ Find Solr Service

%prep
rm -Rf ezfind-%{version}
env GIT_SSL_NO_VERIFY=true git clone https://github.com/ezsystems/ezfind.git ezfind-%{version}
cd ezfind-%{version}
git checkout 38304f26c07cb9f342dae60b58a9a21040c79a32
cd ..
rm -Rf ezfind-%{version}/.git
rm -Rf ezfind-%{version}/.gitignore
cp -pf %{SOURCE1} . 

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_datadir}
mkdir -p $RPM_BUILD_ROOT%{_var}/ezfind
mkdir -p $RPM_BUILD_ROOT%{_var}/log/ezfind
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
mkdir -p $RPM_BUILD_ROOT%{_datadir}/ezfind/solr-webapp

cp -R ezfind-%{version}/java/* $RPM_BUILD_ROOT%{_datadir}/ezfind
cp %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/ezfind/solr/ezp-default/conf/stopwords.txt
cp %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/ezfind/solr/lib/mysql-connector-java-5.1.15-bin.jar
cp %{SOURCE4} $RPM_BUILD_ROOT%{_datadir}/ezfind/solr/bin/SOLRCLEAN
cp %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/ezfind
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/ezfind-solr

cp $RPM_BUILD_ROOT%{_datadir}/ezfind/etc/jetty.xml $RPM_BUILD_ROOT%{_datadir}/ezfind/etc/jetty.xml.dist

sed -i 's/<SystemProperty name="jetty.logs" default=".\/logs"\/>/<SystemProperty name="jetty.logs" default="\/var\/log\/ezfind"\/>/g' $RPM_BUILD_ROOT%{_datadir}/ezfind/etc/jetty.xml 

cp $RPM_BUILD_ROOT%{_datadir}/ezfind/solr/ezp-default/conf/solrconfig.xml $RPM_BUILD_ROOT%{_datadir}/ezfind/solr/ezp-default/conf/solrconfig.xml.dist

cp $RPM_BUILD_ROOT%{_datadir}/ezfind/solr/ezp-default/conf/schema.xml $RPM_BUILD_ROOT%{_datadir}/ezfind/solr/ezp-default/conf/schema.xml.dist

sed -i '/type="text_icu"/d' $RPM_BUILD_ROOT%{_datadir}/ezfind/solr/ezp-default/conf/schema.xml
sed -i '/<fieldType name="text_icu" class="solr.TextField" positionIncrementGap="100" autoGeneratePhraseQueries="false">/,/<\/fieldType>/d' $RPM_BUILD_ROOT%{_datadir}/ezfind/solr/ezp-default/conf/schema.xml

sed -i 's@<str name=\"confFiles\">.*@<str name=\"confFiles\">schema.xml,elevate.xml,stopwords.txt</str>@g' $RPM_BUILD_ROOT%{_datadir}/ezfind/solr/ezp-default/conf/solrconfig.xml

sed -i '
/<\/fields>/ i\
<dynamicField name="*____loc" type="location" indexed="true" stored="true"\/>\
<dynamicField name="*____loc_0_coordinate" type="double" indexed="true" stored="true"\/>\
<dynamicField name="*____loc_1_coordinate" type="double" indexed="true" stored="true"\/>\
' $RPM_BUILD_ROOT%{_datadir}/ezfind/solr/ezp-default/conf/schema.xml

sed -i '
/<\/schema>/ i\
     <copyField source="*_lk" dest="ezf_df_tags"\/>\
     <copyField source="*_k" dest="ezf_df_tags"\/>\
' $RPM_BUILD_ROOT%{_datadir}/ezfind/solr/ezp-default/conf/schema.xml

sed -i '
/<\/fields>/ i\
     <field name="ezf_df_tags" type="text" indexed="true" stored="true" multiValued="true" termVectors="true"\/>\
' $RPM_BUILD_ROOT%{_datadir}/ezfind/solr/ezp-default/conf/schema.xml

%files
%defattr(-,root,root)
%{_sysconfdir}/*
%{_datadir}/*
%attr(755, ezfind, ezfind) %{_datadir}/ezfind/solr-webapp
%attr(755, ezfind, ezfind) %{_var}/ezfind
%attr(755, ezfind, ezfind) %{_var}/log/ezfind

%pre
if [ $1 -eq 1 ]; then
    echo "Initial setup of SOLR"
    /usr/sbin/groupadd -g 271 ezfind 2> /dev/null || :
    /usr/sbin/useradd -c ezfind -g ezfind -u 271 -s /sbin/nologin -d / -r ezfind 2> /dev/null || :
fi

%post
if [ $1 -eq 1 ]; then
    /sbin/chkconfig --add ezfind-solr
fi

%preun
if [ $1 -eq 0 ]; then
   echo "Final removal of SOLR"
   /sbin/service ezfind-solr stop > /dev/null 2>&1
   /sbin/chkconfig --del ezfind-solr
fi 

%postun
if [ $1 -eq 0 ]; then
   /usr/sbin/userdel -f ezfind 2> /dev/null || : 
   /usr/sbin/groupdel -f ezfind 2> /dev/null || :
fi


%changelog

%clean
rm -rf $RPM_BUILD_ROOT
