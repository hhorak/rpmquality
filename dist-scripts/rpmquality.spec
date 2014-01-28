%if 0%{?fedora}
%bcond_without	python3
%else
%bcond_with	python3
%endif

Name:		rpmquality
Version:	0.1
Release:	0.2%{?dist}
Summary:	Tool for assessing RPM quality

Group:		Development/Tools
License:	MIT
URL:		https://github.com/hhorak/rpmquality
Source0:	rpmquality-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python-devel, python-setuptools
Requires:	python, python-setuptools
%if %{with python3}
BuildRequires:	python3-devel, python3-setuptools
Requires:	python3, python3-setuptools
%endif
Requires:	rpmlint

%description
RPM Quality Assessor uses tools like rpmlint and similar and tries to parse
and assess their output to compute some weight quality in percents.
The final number says how good the RPM is.

%if %{with python3}
%package python3
Summary:	Python 3 module of RPM quality
Group:		Development/Tools

%description python3
Module for Python 3 that serves as RPM quality tool without launcher in PATH.
%endif

%prep
%setup -q

%build
%{?with_python3: %{__python3} setup.py build}
%{__python} setup.py build

%install
# install python3 part
%if %{with python3}
%{__python3} setup.py install --skip-build --root %{buildroot}
sed -ie 's|^#!%{__python}$|#!%{__python3}|' %{buildroot}%{python3_sitelib}/%{name}/bin.py
rm -f %{buildroot}%{python3_sitelib}/%{name}/bin.pye
rm -f %{buildroot}%{_bindir}/%{name}
%endif

# install python2 part
%{__python} setup.py install --skip-build --root %{buildroot}

%files
%doc README.rst LICENSE
%{_bindir}/%{name}
%{python_sitelib}/%{name}/*.py*
%{python_sitelib}/%{name}/modules/*.py*
%{python_sitelib}/%{name}-%{version}-py?.?.egg-info

%if %{with python3}
%files python3
%doc README.rst LICENSE
%{python3_sitelib}/%{name}/*.py
%{python3_sitelib}/%{name}/__pycache__/*.cpython-33.py?
%{python3_sitelib}/%{name}/modules/*.py
%{python3_sitelib}/%{name}/modules/__pycache__/*.cpython-33.py?
%{python3_sitelib}/%{name}-%{version}-py?.?.egg-info
%endif

%changelog
* Mon Jan 27 2014 Honza Horak <hhorak@redhat.com> - 0.1-0.2
- Build for Python 3

* Wed Dec 18 2013 Honza Horak <hhorak@redhat.com> - 0-0.1
- Initial packaging

