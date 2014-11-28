Name: ezcluster
Summary: The eZ Cluster of the xrow GmbH
Version: 2.0
Release: 1
License: GPL
Group: Applications/Webservice
URL: http://packages.xrow.com/redhat
Distribution: Linux
Vendor: xrow GmbH
Packager: Bjoern Dieding / xrow GmbH <bjoern@xrow.de>
BuildRequires: libxslt subversion
Requires: yum
Requires: mariadb-server mariadb
# mlocate will crawl /mnt/nas
Conflicts: mlocate
Conflicts: xrow-psa
Conflicts: mod_ssl
#When bulding a new image
#Requires: libuuid-devel qemu-img
Requires: httpd haproxy mod-pagespeed ntp aws-cli nfs-utils nfs4-acl-tools sudo varnish autofs dkms
Requires: selinux-policy yum-cron
Requires: php
# for veewee
Requires: libxslt-devel
Requires: varnish >= 4.0
Requires(pre): /usr/sbin/useradd
Requires(postun): /usr/sbin/userdel
BuildRequires: /usr/bin/composer

BuildRoot: %{_tmppath}/%{name}-root
BuildArch: noarch
%description

%install
rm -rf $RPM_BUILD_ROOT

git clone https://github.com/xrowgmbh/ezcluster $RPM_BUILD_ROOT%{_datadir}/ezcluster
mv $RPM_BUILD_ROOT%{_datadir}/ezcluster/etc $RPM_BUILD_ROOT%{_sysconfdir}

/usr/bin/composer update -d $RPM_BUILD_ROOT%{_datadir}/ezcluster
#for f in $RPM_BUILD_ROOT%{_datadir}/ezcluster/schema/*.xsd
#do
#	xsltproc --stringparam title "eZ Cluster XML Schema" \
#                 --output $f.html $RPM_BUILD_ROOT%{_datadir}/ezcluster/build/xs3p/xs3p.xsl $f
#done

#del unneeded
rm -Rf $RPM_BUILD_ROOT%{_datadir}/ezcluster/drafts
rm -Rf $RPM_BUILD_ROOT%{_datadir}/ezcluster/build

mkdir -p $RPM_BUILD_ROOT/var/www/sites


mkdir $RPM_BUILD_ROOT%{_bindir}
cp $RPM_BUILD_ROOT%{_datadir}/ezcluster/ezcluster $RPM_BUILD_ROOT%{_bindir}/ezcluster

chmod +x $RPM_BUILD_ROOT%{_datadir}/ezcluster/ezcluster
chmod +x $RPM_BUILD_ROOT%{_bindir}/ezcluster

%files
%defattr(-,root,root,-)
%{_sysconfdir}/*   
%{_datadir}/ezcluster/*         
%{_datadir}/ezcluster/.git*
%{_bindir}/*
%attr(777, root, root) /var/www/sites
%attr(755, root, root) %{_sysconfdir}/rc.d/init.d/ezcluster
%attr(440, root, root) %{_sysconfdir}/sudoers.d/ezcluster

%pre

grep "^ec2-user:" /etc/group &> /dev/null
if [ $? -ne "0" ]; then
    groupadd -g 222 ec2-user
fi
grep "^ec2-user:" /etc/passwd &> /dev/null
if [ $? -ne "0" ]; then
    useradd -m -u 222 -g ec2-user -G wheel,ec2-user -c "Cloud Default User" ec2-user
fi

%post

if [ "$1" -eq "1" ]; then

mkdir -p /mnt/nas
mkdir -p /mnt/storage
chmod 777 /mnt/nas
chmod 777 /mnt/storage

# drbd needs this for gfs
sed -i "s/locking_type = 1/locking_type = 3/g" /etc/lvm/lvm.conf

#logrotate
sed -i "s/weekly/daily/g" /etc/logrotate.conf
sed -i "s/#compress/compress/g" /etc/logrotate.conf

# all SSH need revisit
#sed -i "s/PasswordAuthentication yes/PasswordAuthentication no/g" /etc/ssh/sshd_config
#sed -i "s/UseDNS yes/UseDNS no/g" /etc/ssh/sshd_config
#very wrong
#sed -i "s/UsePAM yes/UsePAM no/g" /etc/ssh/sshd_config
sed -i "s/127.0.0.1/0.0.0.0/g" /usr/share/ezfind/etc/jetty.xml
sed -i "s/VARNISH_LISTEN_PORT[[:blank:]]*=.*$/VARNISH_LISTEN_PORT=80/g" /etc/sysconfig/varnish
sed -i "s/VARNISH_VCL_CONF[[:blank:]]*=.*$/VARNISH_VCL_CONF=\/etc\/varnish\/ezcluster.vcl/g" /etc/sysconfig/varnish
sed -i "s/VARNISH_STORAGE[[:blank:]]*=.*$/VARNISH_STORAGE=\"malloc,\$\{VARNISH_STORAGE_SIZE\}\"/g" /etc/sysconfig/varnish

#sed -i "s/PACKAGE_SETUP=yes/PACKAGE_SETUP=no/g" /etc/sysconfig/cloud-init

# All Apache settings
sed -i "s/^Listen 80$/#Listen 80/g" /etc/httpd/conf/httpd.conf
sed -i "s/^LogFormat \"%h/LogFormat \"%{X-Forwarded-For}i/g" /etc/httpd/conf/httpd.conf
sed -i "s/ModPagespeed on/ModPagespeed off/g" /etc/httpd/conf.d/pagespeed.conf

sed -i "s/^Defaults    requiretty/#Defaults    requiretty/g" /etc/sudoers

sed -i '
/^#Listen 80/ a\
Listen 8080\
' /etc/httpd/conf/httpd.conf

/sbin/chkconfig --add ezcluster

chkconfig postfix off
chkconfig httpd off 
chkconfig varnish off 
chkconfig nfs off
chkconfig nfslock off
chkconfig drbd off
chkconfig ezfind-solr off
chkconfig mysql off
chkconfig sendmail off
chkconfig xfs off
chkconfig varnish off
chkconfig haproxy off

fi

chkconfig autofs on


rm -Rf /tmp/.compilation/

%preun

if [ "$1" -eq "0" ]; then
   sed -i "s/locking_type = 3/locking_type = 1/g" /etc/lvm/lvm.conf
   sed -i "s/daily/weekly/g" /etc/logrotate.conf
   sed -i "s/compress/#compress/g" /etc/logrotate.conf 
#   sed -i "s/PasswordAuthentication no/PasswordAuthentication yes/g" /etc/ssh/sshd_config
#   sed -i "s/UseDNS no/UseDNS yes/g" /etc/ssh/sshd_config
#   sed -i "s/UsePAM no/UsePAM yes/g" /etc/ssh/sshd_config   
   sed -i "s/0.0.0.0/127.0.0.1/g" /usr/share/ezfind/etc/jetty.xml
   sed -i "s/^Listen 8080//g" /etc/httpd/conf/httpd.conf
   sed -i "s/^#Listen 80/Listen 80/g" /etc/httpd/conf/httpd.conf
   sed -i "s/^LogFormat \"%{X-Forwarded-For}i/LogFormat \"%h/g" /etc/httpd/conf/httpd.conf
   sed -i "s/^#Defaults    requiretty/Defaults    requiretty/g" /etc/sudoers
   /sbin/service ezcluster stop > /dev/null 2>&1
   /sbin/chkconfig --del ezcluster
fi


%postun
 
if [ "$1" -eq "0" ]; then
   chkconfig httpd on
   /sbin/service httpd stop > /dev/null 2>&1
   /usr/sbin/userdel ec2-user
fi
rm -Rf /tmp/.compilation/

%clean
rm -rf $RPM_BUILD_ROOT
