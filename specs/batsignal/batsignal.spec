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
BuildRequires:  pkgconfig

Requires:       libnotify

%description
A lightweight battery daemon written in C that notifies the user about
various battery states.

%prep
%autosetup

%build
# We must append $(pkg-config ...) so GCC knows where to find the headers
make %{?_smp_mflags} \
    CFLAGS="%{optflags} $(pkg-config --cflags libnotify)" \
    LDFLAGS="%{build_ldflags} $(pkg-config --libs libnotify)"

%install
%make_install PREFIX=%{_prefix}

%files
%license LICENSE
%doc README.md
%{_bindir}/batsignal
%{_mandir}/man1/batsignal.1*

%changelog
* Sun Nov 23 2025 User <user@example.com> - 1.8.0-1
- Initial package
- Fixed build flags to include libnotify headers
