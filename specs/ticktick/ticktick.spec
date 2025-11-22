Name:           ticktick
Version:        6.0.40
Release:        1%{?dist}
Summary:        TickTick task management app
License:        Proprietary
URL:            https://ticktick.com
%ifarch x86_64
Source0:        https://download.ticktick.app/download/linux/linux_rpm_x64/ticktick-%{version}-x86_64.rpm
%endif
%ifarch aarch64
Source0:        https://download.ticktick.app/download/linux/linux_rpm_arm64/ticktick-%{version}-aarch64.rpm
%endif

# copy deps from their rpm
AutoReqProv: no

%description
TickTick task and project management application.

%prep
rpm2cpio %{SOURCE0} | cpio -idmv

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
