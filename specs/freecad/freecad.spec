Name:           freecad
Version:        1.0.2
Release:        1%{?dist}
Summary:        Feature-rich, open-source parametric 3D modeler

License:        LGPLv2+
URL:            https://www.freecad.org
# Note: The python version in the filename (py311) might change in future releases.
# The auto-update workflow should handle updating this URL.
Source0:        https://github.com/FreeCAD/FreeCAD/releases/download/%{version}/FreeCAD_%{version}-conda-Linux-aarch64-py311.AppImage

ExclusiveArch:  aarch64

BuildRequires:  desktop-file-utils
# fuse is often needed to run AppImage to extract contents, but we can also use
# other tools if needed. Assuming we can run it on the build host (aarch64).
BuildRequires:  fuse

Requires:       fuse-libs

%description
FreeCAD is a general-purpose parametric 3D CAD modeler and a building
information modeling (BIM) software with Finite Element Method (FEM) support.

This package wraps the official AppImage for aarch64.

%prep
# No setup needed for AppImage, just copy it.

%build
# Nothing to build

%install
mkdir -p %{buildroot}%{_bindir}
install -m 755 %{SOURCE0} %{buildroot}%{_bindir}/freecad

# Extract AppImage contents to get icon and desktop file
# We need to make the source executable first to run it
chmod +x %{SOURCE0}
# Run with --appimage-extract
# Note: This requires the build environment to support FUSE or we need to use --appimage-extract-and-run if FUSE is not available but we have a way to mount?
# Actually, --appimage-extract usually works without FUSE if it just extracts squashfs.
# But sometimes it fails in chroot.
# Alternative: manually mount or use unsquashfs if available.
# Let's try running it. If it fails, we might need 'squashfs-tools'.
%{SOURCE0} --appimage-extract || true

mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps

# The extracted content is in squashfs-root/
if [ -d squashfs-root ]; then
    # Install desktop file
    # We might need to edit the desktop file to point to the correct binary
    install -m 644 squashfs-root/org.freecad.FreeCAD.desktop %{buildroot}%{_datadir}/applications/freecad.desktop
    desktop-file-install --dir=%{buildroot}%{_datadir}/applications \
        --set-key=Exec --set-value=freecad \
        --set-icon=freecad \
        %{buildroot}%{_datadir}/applications/freecad.desktop

    # Install icon
    install -m 644 squashfs-root/org.freecad.FreeCAD.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/freecad.svg
fi

%files
%{_bindir}/freecad
%{_datadir}/applications/freecad.desktop
%{_datadir}/icons/hicolor/scalable/apps/freecad.svg

%changelog
* Sun Nov 30 2024 Ilyaas Kalim <ilyaas@ilyaas.ca> - 1.0.2-1
- Initial package for FreeCAD AppImage aarch64
