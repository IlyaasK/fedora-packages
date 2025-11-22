Name:           standard-notes
Version:        3.201.3
Release:        5%{?dist}
Summary:        Standard Notes end-to-end encrypted note-taking app
License:        AGPLv3
URL:            https://standardnotes.com

Source0:        https://github.com/standardnotes/app/releases/download/@standardnotes/desktop@%{version}/standard-notes-%{version}-linux-x86_64.AppImage
Source1:        https://github.com/standardnotes/app/releases/download/@standardnotes/desktop@%{version}/standard-notes-%{version}-linux-arm64.AppImage
Source2:        https://raw.githubusercontent.com/IlyaasK/fedora-packages/main/specs/standard-notes/standard-notes.desktop
Source3:        https://raw.githubusercontent.com/IlyaasK/fedora-packages/main/specs/standard-notes/standard-notes.png

# ---------------------------------------------------------------------
# APPIMAGE SAFEGUARDS
# ---------------------------------------------------------------------
# 1. Disable debuginfo generation (prevent "No build ID" errors)
%global debug_package %{nil}
# 2. Disable stripping (prevent corrupting the AppImage binary)
%global __strip /bin/true
# 3. Disable post-install checks (prevent repackaging errors)
%global __os_install_post %{nil}
# 4. Disable automatic dependency scanning (prevent finding internal AppImage libs)
AutoReq:        no
# ---------------------------------------------------------------------

Requires:       fuse
Requires:       zlib
BuildRequires:  desktop-file-utils

%description
Standard Notes is an end-to-end encrypted note-taking application.

%prep
# No preparation needed for pre-built binaries

%build
# No compilation needed

%install
# 1. Create directory structure
#    We use /opt/standard-notes for the main binary and libs
mkdir -p %{buildroot}/opt/standard-notes
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/pixmaps

# 2. Install the AppImage binary to /opt
%ifarch x86_64
install -Dm755 %{SOURCE0} %{buildroot}/opt/standard-notes/standard-notes.AppImage
%endif
%ifarch aarch64
install -Dm755 %{SOURCE1} %{buildroot}/opt/standard-notes/standard-notes.AppImage
%endif

# 3. FIX MISSING libz.so
#    Fedora only provides libz.so.1 by default. AppImages often look for "libz.so".
#    We create a symlink inside our private /opt folder pointing to the system lib.
ln -s %{_libdir}/libz.so.1 %{buildroot}/opt/standard-notes/libz.so

# 4. Create the Wrapper Script
#    This script sets LD_LIBRARY_PATH so the app sees our private libz.so link
#    before launching the actual binary.
cat <<EOF > %{buildroot}%{_bindir}/standard-notes
#!/bin/sh
export LD_LIBRARY_PATH=/opt/standard-notes:\$LD_LIBRARY_PATH
exec /opt/standard-notes/standard-notes.AppImage "\$@"
EOF

# Make the wrapper executable
chmod 755 %{buildroot}%{_bindir}/standard-notes

# 5. Install Desktop File and Icon
install -Dm644 %{SOURCE2} %{buildroot}%{_datadir}/applications/standard-notes.desktop
install -Dm644 %{SOURCE3} %{buildroot}%{_datadir}/pixmaps/standard-notes.png

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/standard-notes.desktop

%files
# Own the specific directory in /opt
/opt/standard-notes/
%{_bindir}/standard-notes
%{_datadir}/applications/standard-notes.desktop
%{_datadir}/pixmaps/standard-notes.png

%changelog
* Sat Nov 22 2025 Ilyaas Kapadia <ilyaaskapadia@tutanota.com> - 3.201.3-5
- Implement best-practice packaging:
- Install to /opt with private libs
- Add wrapper script to handle LD_LIBRARY_PATH
- Fix libz.so missing error without requiring zlib-devel
- Prevent binary stripping
