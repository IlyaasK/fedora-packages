Name:           qmk
Version:        1.1.8
Release:        1%{?dist}
Summary:        A program to help users work with QMK Firmware

License:        MIT
URL:            https://github.com/qmk/qmk_cli
# Source code from PyPI
Source0:        %{pypi_source}
# Udev rules fetched directly from the main firmware repo
Source1:        https://raw.githubusercontent.com/qmk/qmk_firmware/master/util/udev/50-qmk.rules

BuildArch:      noarch

# Build dependencies for Python generation
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
BuildRequires:  pyproject-rpm-macros
BuildRequires:  git-core
BuildRequires:  systemd-rpm-macros

# Runtime dependencies
Requires:       git-core
Requires:       systemd-udev

# Recommended toolchain dependencies.
# QMK can manage these via 'qmk setup', but installing system packages is cleaner.
# These package names are standard in Fedora for both x86 and aarch64.
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

It includes the 'qmk' command and installs necessary udev rules for
non-root device flashing.

%prep
%autosetup -n %{name}-%{version}

%generate_buildrequires
# This macro automatically generates BuildRequires from requirements.txt
%pyproject_buildrequires -r

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files qmk

# Install udev rules to /usr/lib/udev/rules.d/
install -D -p -m 0644 %{SOURCE1} %{buildroot}%{_udevrulesdir}/50-qmk.rules

%files -f %{pyproject_files}
%{_bindir}/qmk
%{_udevrulesdir}/50-qmk.rules
%doc README.md
%license LICENSE

%changelog
* Sun Nov 23 2025 User <user@example.com> - 1.1.8-1
- Initial package for Fedora Copr
- Includes 50-qmk.rules for udev
