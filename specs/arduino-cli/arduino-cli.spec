Name:           arduino-cli
Version:        1.3.1
Release:        1%{?dist}
Summary:        Arduino command line tool
License:        GPLv3
URL:            https://github.com/arduino/arduino-cli
Source0:        https://github.com/arduino/arduino-cli/releases/download/v%{version}/arduino-cli_%{version}_Linux_64bit.tar.gz
Source1:        https://github.com/arduino/arduino-cli/releases/download/v%{version}/arduino-cli_%{version}_Linux_ARM64.tar.gz

%global debug_package %{nil}

%description
Arduino CLI is a command line tool for programming Arduino boards.

%prep
%ifarch x86_64
%setup -q -c -T -a 0
%endif
%ifarch aarch64
%setup -q -c -T -a 1
%endif

%build
# prebuilt binary

%install
install -Dm755 arduino-cli %{buildroot}%{_bindir}/arduino-cli

# generate completions
%{buildroot}%{_bindir}/arduino-cli completion bash > arduino-cli.bash
%{buildroot}%{_bindir}/arduino-cli completion zsh > arduino-cli.zsh
%{buildroot}%{_bindir}/arduino-cli completion fish > arduino-cli.fish

install -Dm644 arduino-cli.bash %{buildroot}%{_datadir}/bash-completion/completions/arduino-cli
install -Dm644 arduino-cli.zsh %{buildroot}%{_datadir}/zsh/site-functions/_arduino-cli
install -Dm644 arduino-cli.fish %{buildroot}%{_datadir}/fish/vendor_completions.d/arduino-cli.fish

%files
%{_bindir}/arduino-cli
%{_datadir}/bash-completion/completions/arduino-cli
%{_datadir}/zsh/site-functions/_arduino-cli
%{_datadir}/fish/vendor_completions.d/arduino-cli.fish

%changelog
* Sat Nov 22 2025 Ilyaas Kapadia <ilyaaskapadia@tutanota.com> - 1.3.1-1
- initial package
