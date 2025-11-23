Name:           qmk
Version:        1.1.8
Release:        1%{?dist}
Summary:        A program to help users work with QMK Firmware

License:        MIT
URL:            https://github.com/qmk/qmk_cli
# CHANGED: Use direct URL instead of macro to avoid SRPM build errors
Source0:        https://files.pythonhosted.org/packages/source/q/qmk/qmk-%{version}.tar.gz
Source1:        https://raw.githubusercontent.com/qmk/qmk_firmware/master/util/udev/50-qmk.rules

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
BuildRequires:  pyproject-rpm-macros
BuildRequires:  git-core
BuildRequires:  systemd-rpm-macros

Requires:       git-core
Requires:       systemd-udev

Recommends:     arm-none-eabi-gcc-cs
Recommends:     arm-none-eabi-newlib
Recommends:     avr-gcc
Recommends:     avr-libc
Recommends:     avrdude
Recommends:     dfu-programmer
Recommends:     dfu-util

%description
The QMK CLI (command line interface) makes building and working with QMK
keyboards easier. It simplifies tasks such as obtaining and compiling the
QMK firmware, creating keymaps, and flashing devices.

%prep
%autosetup -n %{name}-%{version}

%generate_buildrequires
%pyproject_buildrequires -r

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files qmk
install -D -p -m 0644 %{SOURCE1} %{buildroot}%{_udevrulesdir}/50-qmk.rules

%files -f %{pyproject_files}
%{_bindir}/qmk
%{_udevrulesdir}/50-qmk.rules
%doc README.md
%license LICENSE

%changelog
* Sun Nov 23 2025 User <user@example.com> - 1.1.8-1
- Initial package
