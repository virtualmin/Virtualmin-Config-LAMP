Name:           virtualmin-config
Version:        6.0.24
Release:        1
Summary:        Collection of plugins to initialize the configuration of services that Virtualmin manages, and a command line tool called config-system to run them
License:        GPL+
Group:          Development/Libraries
URL:            https://github.com/virtualmin/Virtualmin-Config/
Source0:        Virtualmin-Config-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl >= 0:5.010
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Log::Log4perl)
BuildRequires:  perl(Test::More)
BuildRequires:	perl(Module::Load)
Requires:	webmin
Requires:       perl(Log::Log4perl)
Requires:       perl(Term::ANSIColor)
Requires:       perl(Term::Spinner::Color)
Requires:	perl(Module::Load)

%description
This is a mini-framework for configuring elements of a Virtualmin system.
It uses Webmin as a library to abstract common configuration tasks,
provides a friendly status indicator, and makes it easy to pick and choose
the kind of configuration you want (should you choose to go that route).
The Virtualmin install script chooses either the LAMP (with Apache) or LEMP
(with nginx) bundle, and performs the configuration for the whole stack.

%prep
%setup -q -n Virtualmin-Config-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/libexec/webmin/virtual-server
# link virtualmin-config-system into Virtualmin dir
ln -s /usr/bin/virtualmin-config-system \
  $RPM_BUILD_ROOT/usr/libexec/webmin/virtual-server/config-system.pl

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

#%check
#make test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc dist.ini LICENSE META.json README
%{perl_vendorlib}/*
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_bindir}/*
/usr/libexec/webmin/virtual-server/config-system.pl

%changelog
* Sun Nov 04 2018 Joe Cooper <joe@virtualmin.com> 6.0.24-1
- A bunch of changes for Ubuntu/Debian that don't impact RHEL
* Fri Oct 13 2017 Joe Cooper <joe@virtualmin.com> 6.0.21-1
- Update SASL flags
* Thu Sep 28 2017 Joe Cooper <joe@virtualmin.com> 6.0.20-1
- Minimal configs adds Dovecot, SASL, removes Fail2ban
- Fix Apache default file handling on Ubuntu 16.04
- ProFTPd shouldn't require TlS
* Mon Sep 04 2017 Joe Cooper <joe@virtualmin.com> 6.0.16-1
- Fix ProFTPd failure to write config changes
* Fri Sep 01 2017 Joe Cooper <joe@virtualmin.com> 6.0.15-1
- Remove MiniVirtualmin plugin, Virtualmin plugin handles it when bundle is Mini*
- Handle some DHCP configured systems by adding localhost to name servers
- Fix SSL default site on CentOS (disabling it).
* Wed Aug 23 2017 Joe Cooper <joe@virtualmin.com> 6.0.14-1
- Fix non-fatal warn on Quotas
- Fix some SASL problems
- Fix Quotas convertquota error by using checkquota instead
- Make Virtualmin use nginx correctly
* Tue Aug 22 2017 Joe Cooper <joe@virtualmin.com> 6.0.13-1
- Fixes for Apache init/systemd detection
- Non-fatal error on Quotas
- New non-fatal error result type
* Fri Jun 23 2017 Joe Cooper <joe@virtualmin.com> 6.0.5-1
- Fail2ban and Firewalld modules added
- Handle systemd or not
* Mon May 08 2017 Joe Cooper <joe@virtualmin.com>
- Rename to config-system
* Mon May 08 2017 Joe Cooper <joe@virtualmin.com>
- Tweak deps
* Sat May 06 2017 Joe Cooper <joe@virtualmin.com> 6.0.0-1
- Specfile autogenerated by cpanspec 1.78.
