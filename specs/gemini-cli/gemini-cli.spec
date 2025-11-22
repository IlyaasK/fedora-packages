Name:           gemini-cli
Version:        0.17.1
Release:        1%{?dist}
Summary:        Google Gemini CLI tool

License:        Apache-2.0
URL:            https://github.com/google-gemini/gemini-cli
Source0:        https://github.com/google-gemini/gemini-cli/releases/download/v%{version}/gemini.js

BuildArch:      noarch
Requires:       nodejs >= 18

%description
CLI tool for interacting with Google's Gemini AI models from the command line.

%prep
# no prep needed

%build
# no build needed

%install
install -Dm755 %{SOURCE0} %{buildroot}%{_bindir}/gemini

%files
%{_bindir}/gemini

%changelog
* Fri Nov 22 2024 Your Name <your@email.com> - 0.17.1-1
- Initial package
