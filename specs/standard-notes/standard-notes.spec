Name:           standard-notes
Version:        3.201.3
Release:        1%{?dist}
Summary:        Standard Notes end-to-end encrypted note-taking app
License:        AGPLv3
URL:            https://standardnotes.com
Source0:        https://github.com/standardnotes/app/releases/download/@standardnotes/desktop@%{version}/standard-notes-%{version}-linux-x86_64.AppImage
Source1:        https://github.com/standardnotes/app/releases/download/@standardnotes/desktop@%{version}/standard-notes-%{version}-linux-arm64.AppImage
Source2:        https://raw.githubusercontent.com/IlyaasK/fedora-packages/main/specs/standard-notes/standard-notes.desktop
Source3:        https://raw.githubusercontent.com/IlyaasK/fedora-packages/main/specs/standard-notes/standard-notes.png
Requires:       fuse
BuildRequires:  desktop-file-utils

%description
Standard Notes is an end-to-end encrypted note-taking application.

%prep
# no prep

%build
# no build

%install
export QA_RPATHS=$[ 0x0002 ]
%ifarch x86_64
install -Dm755 %{SOURCE0} %{buildroot}%{_bindir}/standard-notes
%endif
%ifarch aarch64
install -Dm755 %{SOURCE1} %{buildroot}%{_bindir}/standard-notes
%endif
install -Dm644 %{SOURCE2} %{buildroot}%{_datadir}/applications/standard-notes.desktop
install -Dm644 %{SOURCE3} %{buildroot}%{_datadir}/pixmaps/standard-notes.png

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/standard-notes.desktop

%files
%{_bindir}/standard-notes
%{_datadir}/applications/standard-notes.desktop
%{_datadir}/pixmaps/standard-notes.png

%changelog
* Fri Nov 21 2025 Ilyaas Kapadia <ilyaaskapadia@tutanota.com> - 3.201.3-1
- initial package
