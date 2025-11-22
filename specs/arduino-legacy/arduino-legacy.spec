Name:           arduino-legacy
Version:        1.8.19
Release:        1%{?dist}
Summary:        Open-source electronics prototyping platform (Legacy 1.x)
License:        GPLv2+
URL:            https://www.arduino.cc
ExclusiveArch:  aarch64


# ---------------------------------------------------------------------
# THE FIX: Stop RPM from messing with the binaries
# ---------------------------------------------------------------------
# 1. Disable debug info (we already did this)
%global debug_package %{nil}

# 2. Disable the "strip" step. This stops the "Unable to recognise format" errors
#    by telling RPM that the 'strip' command is just 'true' (do nothing).
%global __strip /bin/true

# 3. Disable all post-install checks (repacking jars, checking rpaths, etc).
#    Since this is a pre-built binary blob in /opt, we want to keep it exact.
%global __os_install_post %{nil}
# ---------------------------------------------------------------------

Source0:        https://downloads.arduino.cc/arduino-%{version}-linuxaarch64.tar.xz
Source1:        https://raw.githubusercontent.com/IlyaasK/fedora-packages/refs/heads/main/specs/arduino-legacy/arduino-legacy.desktop

# Disable auto-dependency generation because this packages a bundled JDK
AutoReq:        no

BuildRequires:  desktop-file-utils

%description
Arduino is an open-source electronics prototyping platform based on 
flexible, easy-to-use hardware and software. 
This is the legacy 1.x version of the IDE.

%prep
%setup -q -n arduino-%{version}

# Fix permissions
find . -type f -name "*" -exec chmod -x {} \;
chmod +x arduino
chmod +x arduino-builder
chmod +x hardware/tools/avr/bin/*
chmod +x java/bin/*
chmod +x lib/libastylej.so

%build
# Binary repack, no build needed

%install
# 1. Create directories
mkdir -p %{buildroot}/opt/arduino-%{version}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/128x128/apps

# 2. Copy files to /opt
cp -a * %{buildroot}/opt/arduino-%{version}/

# 3. Create executable symlink
ln -s /opt/arduino-%{version}/arduino %{buildroot}%{_bindir}/arduino

# 4. Install the Desktop File (Source1)
install -Dm644 %{SOURCE1} %{buildroot}%{_datadir}/applications/arduino-legacy.desktop

# 5. Install the Icon
if [ -f lib/arduino.png ]; then
    install -Dm644 lib/arduino.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/arduino-legacy.png
else
    find %{buildroot}/opt/arduino-%{version} -name "*.png" -exec cp {} %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/arduino-legacy.png \; -quit
fi

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/arduino-legacy.desktop

%files
/opt/arduino-%{version}
%{_bindir}/arduino
%{_datadir}/applications/arduino-legacy.desktop
%{_datadir}/icons/hicolor/128x128/apps/arduino-legacy.png

%changelog
* Sat Nov 22 2025 Ilyaas Kapadia <ilyaaskapadia@tutanota.com> - 1.8.19-1
- Initial package for Arduino 1.8.19 (Legacy)
