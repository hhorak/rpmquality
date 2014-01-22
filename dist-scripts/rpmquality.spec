Name:		rpmquality
Version:	0.1
Release:	0.1%{?dist}
Summary:	Tool for assessing RPM quality

Group:		Development/Tools
License:	MIT
URL:		/dev/null
Source0:	rpmquality-%{version}.tar.gz

BuildRequires:	python-devel
Requires:	python

%description
RPM Quality Assessor uses tools like rpmlint and similar and tries to parse
and assess their output to compute some weight quality in percents.
The final number says how good the RPM is.

%prep
%setup -q


%build
%{__python} setup.py build

%install
%{__python} setup.py install --skip-build --root %{buildroot}

#install -dp -m 0644 %{buildroot}%{_bindir}
#mkdir -p %{buildroot}%{python_sitelib}/%{name}
#pushd src
#cp -r --parents -p * %{buildroot}%{python_sitelib}/%{name}
#popd

%files
%doc README.rst LICENSE
%{_bindir}/%{name}
%{python_sitelib}/%{name}/*.py*
%{python_sitelib}/%{name}/modules/*.py*
#%{python_sitelib}/%{name}/softwarecollectios_modules/*.py*
%{python_sitelib}/%{name}-%{version}-py?.?.egg-info


%changelog
* Wed Dec 18 2013 Honza Horak <hhorak@redhat.com> - 0-0.1
- Initial packaging

