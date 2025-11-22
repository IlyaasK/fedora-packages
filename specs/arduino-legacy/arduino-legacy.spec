Name:           arduino-legacy
Version:        1.8.19
Release:        1%{?dist}
Summary:        Open-source electronics prototyping platform (Legacy 1.x)
License:        GPLv2+
URL:            https://www.arduino.cc
# The user requested aarch64 specifically
ExclusiveArch:  aarch64

Source0:        https://downloads.arduino.cc/arduino-%{version}-linuxaarch64.tar.xz

# Arduino 1.x bundles its own Java Runtime Environment (JRE) and many libs.
# We must disable automatic dependency generation to prevent conflicts 
# with system Java or library provides.
AutoReq:        no

BuildRequires:  desktop-file-utils

%description
Arduino is an open-source electronics prototyping platform based on 
flexible, easy-to-use hardware and software. 
This is the legacy 1.x version of the IDE.

%prep
%setup -q -n arduino-%{version}

# Fix permissions for the bundled java runtime and other binaries
find . -type f -name "*" -exec chmod -x {} \;
chmod +x arduino
chmod +x arduino-builder
chmod +x hardware/tools/avr/bin/*
chmod +x java/bin/*
# libastyle sometimes needs exec permissions depending on how it's called
chmod +x lib/libastylej.so

%build
# This is a binary repack, nothing to build.

%install
# 1. Create the destination directories
mkdir -p %{buildroot}/opt/arduino-%{version}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/128x128/apps

# 2. Copy the application files to /opt/
cp -a * %{buildroot}/opt/arduino-%{version}/

# 3. Create the executable symlink
ln -s /opt/arduino-%{version}/arduino %{buildroot}%{_bindir}/arduino

# 4. GENERATE THE DESKTOP FILE MANUALLY
# (This fixes the "No such file" error and sets the correct paths immediately)
cat > %{buildroot}%{_datadir}/applications/arduino-legacy.desktop <<EOF
[Desktop Entry]
Type=Application
Name=Arduino IDE (Legacy)
GenericName=Electronics Prototyping Platform
Comment=Open-source electronics prototyping platform
Exec=arduino
Icon=arduino-legacy
Terminal=false
Categories=Development;IDE;Electronics;
MimeType=text/x-arduino;
Keywords=embedded;electronics;avr;microcontroller;
StartupWMClass=processing-app-Base
EOF

# 5. Install the Icon
# We try to find the icon in the likely locations.
# If lib/arduino.png exists, we use it.
if [ -f lib/arduino.png ]; then
    install -Dm644 lib/arduino.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/arduino-legacy.png
else
    # Fallback: If the png is missing, create a dummy one or warn
    echo "Warning: lib/arduino.png not found. Icon might be missing."
    # Try looking in the copied /opt directory just in case
    find %{buildroot}/opt/arduino-%{version} -name "*.png" -exec cp {} %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/arduino-legacy.png \; -quit
fi%check
desktop-file-validate %{buildroot}%{_datadir}/applications/arduino-legacy.desktop

%files
/opt/arduino-%{version}
%{_bindir}/arduino
%{_datadir}/applications/arduino-legacy.desktop
%{_datadir}/icons/hicolor/1024x1024/apps/arduino.png

%changelog
* Sat Nov 22 2025 Ilyaas Kapadia <ilyaaskapadia@tutanota.com> - 1.8.19-1
- Initial package for Arduino 1.8.19 (Legacy)
