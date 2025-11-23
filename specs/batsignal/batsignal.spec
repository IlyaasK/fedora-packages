Name:           batsignal
Version:        1.8.0
Release:        1%{?dist}
Summary:        Lightweight battery monitor daemon

License:        ISC
URL:            https://github.com/electrickite/batsignal
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  libnotify-devel
BuildRequires:  git-core

Requires:       libnotify

%description
A lightweight battery daemon written in C that notifies the user about
various battery states. It is intended for minimal window managers, but
can be used in any environment that supports desktop notifications via
libnotify.

%prep
%autosetup

%build
# pass CFLAGS to ensure Fedora security hardening options are used
make %{?_smp_mflags} CFLAGS="%{optflags}"

%install
# The Makefile usually expects PREFIX to install to /usr/bin/
%make_install PREFIX=%{_prefix}

%files
%license LICENSE
%doc README.md
%{_bindir}/batsignal
%{_mandir}/man1/batsignal.1*

%changelog
* Sun Nov 23 2025 User <user@example.com> - 1.8.0-1
- Initial package
