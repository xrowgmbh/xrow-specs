Name:           aws-cli
Version:        1.6.5
Release:        2
Summary:        Amazon Web Services Command Line Interface
License:        Apache-2.0
Group:          System/Management
Url:            https://github.com/aws/aws-cli
Source0:        https://github.com/aws/%{name}/archive/%{version}.tar.gz
Requires:       python
Requires:       python-bcdoc
Requires:       python-botocore
#Requires:       python-colorama
Requires:       python-docutils
Requires:       python-rsa
Requires:       python-six
BuildRequires:  python
BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch

%description
The AWS Command Line Interface (CLI) is a unified tool to manage your AWS services. With just one tool to download and configure, you can control multiple AWS services from the command line and automate them through scripts.

%prep
%setup -q

%build
python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot} --install-scripts=%{_bindir}
# No DOS crap
rm %{buildroot}/%{_bindir}/aws.cmd

%files
%defattr(-,root,root,-)
%doc CHANGELOG.rst LICENSE.txt README.rst
%dir %{python_sitelib}/awscli
%dir %{python_sitelib}/awscli-%{version}-py%{py_ver}.egg-info
%{_bindir}/*
%{python_sitelib}/awscli/*
%{python_sitelib}/*egg-info/*

%changelog
