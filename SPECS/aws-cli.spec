Name:           aws-cli
Version:        1.5.4
Release:        0
Summary:        Amazon Web Services Command Line Interface
License:        Apache-2.0
Group:          System/Management
Url:            https://github.com/aws/aws-cli
Source0:        https://github.com/aws/%{name}/archive/%{version}.tar.gz
Requires:       python
%if 0%{?suse_version} && 0%{?suse_version} <= 1110
Requires:       python-argparse >= 1.1
%endif
Requires:       python-bcdoc    >= 0.12.0
Requires:       python-botocore >= 0.67.0
Requires:       python-colorama >= 0.2.5
Requires:       python-docutils >= 0.10
Requires:       python-rsa      >= 3.1.2
Requires:       python-six      >= 1.1.0
BuildRequires:  python
BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch

%description
The AWS Command Line Interface (CLI) is a unified tool to manage your AWS services. With just one tool to download and configure, you can control multiple AWS services from the command line and automate them through scripts.

%prep
%setup -q
%patch0 -p1

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
