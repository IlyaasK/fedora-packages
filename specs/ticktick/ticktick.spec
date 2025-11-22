Name:           ticktick
Version:        6.0.40
Release:        1%{?dist}
Summary:        TickTick task management app
License:        Proprietary
URL:            https://ticktick.com
Source0:        https://download.ticktick.app/download/linux/linux_rpm_x64/ticktick-%{version}-x86_64.rpm
Source1:        https://download.ticktick.app/download/linux/linux_rpm_arm64/ticktick-%{version}-aarch64.rpm

AutoReqProv: no

%description
TickTick task and project management application.

%prep
%ifarch x86_64
rpm2cpio %{SOURCE0} | cpio -idmv
%endif
%ifarch aarch64
rpm2cpio %{SOURCE1} | cpio -idmv
%endif

%install
mkdir -p %{buildroot}
cp -a opt %{buildroot}/
cp -a usr %{buildroot}/

%files
/opt/TickTick/
%{_datadir}/applications/ticktick.desktop
%{_datadir}/icons/hicolor/*/apps/ticktick.png
/usr/lib/.build-id/

%changelog
* Fri Nov 21 2025 Ilyaas Kapadia <ilyaaskapadia@tutanota.com> - 6.0.40-1
- repackaged from official rpm
