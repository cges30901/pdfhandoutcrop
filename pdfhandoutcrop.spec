#
# spec file for package python-pdfhandoutcrop
#
# Copyright (c) 2019 Hsiu-Ming Chang <cges30901@gmail.com>
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

Name:           pdfhandoutcrop
Version:        0.99.2
Release:        0
License:        GPL-3.0+
Summary:        A tool to crop pdf handout with multiple pages per sheet
Url:            https://cges30901.github.io/pdfhandoutcrop/
Group:          Productivity/Other
Source:         https://files.pythonhosted.org/packages/source/p/pdfhandoutcrop/pdfhandoutcrop-%{version}.tar.gz
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires:       python3-PyPDF2
Requires:       python3-qt5
Requires:       python3-PyMuPDF
%if 0%{?suse_version}
BuildRequires:  update-desktop-files
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch

%description
PdfHandoutCrop is a tool to crop pdf handout with multiple pages per sheet. Sometimes the teacher give us handout in pdf format with multiple pages per sheet. If I print it directly, the font size and pictures are too small to read. So I created PdfHandoutCrop to help me crop the handout.

%prep
%setup -q -n pdfhandoutcrop-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
install -D -m0644 pdfhandoutcrop.desktop %{buildroot}%{_datadir}/applications/pdfhandoutcrop.desktop
install -D -m0644 icons/128/pdfhandoutcrop.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/pdfhandoutcrop.png
install -D -m0644 icons/48/pdfhandoutcrop.png %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/pdfhandoutcrop.png
%if 0%{?suse_version}
%suse_update_desktop_file -r pdfhandoutcrop Utility DesktopUtility
%endif

%files
%defattr(-,root,root,-)
%doc README.md LICENSE.txt
%{_bindir}/pdfhandoutcrop
%{python3_sitelib}/*
%{_datadir}/applications/pdfhandoutcrop.desktop
%{_datadir}/icons/hicolor/

%changelog
