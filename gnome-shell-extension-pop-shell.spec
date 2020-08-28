%global uuid        pop-shell@system76.com
%global forgeurl    https://github.com/pop-os/shell
%global commit      841632872d77abc3c45cd13540ffae755839655a
%global date        20200821

%forgemeta

Name:           gnome-shell-extension-pop-shell
Version:        0.1.0
Release:        0.2%{?dist}
Summary:        GNOME Shell extension for advanced tiling window management
# The entire source code is GPLv3 except math.js which is ASL 2.0
License:        GPLv3 and ASL 2.0
URL:            %{forgeurl}
Source0:        %{forgesource}
Source1:        50_pop-shell.gschema.override
BuildArch:      noarch
BuildRequires:  npm(typescript) >= 3.8
Requires:       gnome-shell-extension-common
Recommends:     gnome-extensions-app
Recommends:     gnome-shell-extension-native-window-placement


%description
Pop Shell is a keyboard-driven layer for GNOME Shell which allows for quick and
sensible navigation and management of windows.  The core feature of Pop Shell
is the addition of advanced tiling window management - a feature that has been
highly-sought within our community.  For many - ourselves included - i3wm has
become the leading competitor to the GNOME desktop.


%prep
%forgesetup


%build
# The convert target compiles the typescript to javascript and does some sed
# manipulation of the resulting files.
%make_build convert

# The compile target has a prerequisite of the schemas target, which we don't
# want, because our schemas will be compiled by glib2's file triggers.  Perform
# the steps we do want from that target manually.
mkdir -p _build
cp -r --preserve=mode,timestamps metadata.json icons target/*.js imports/*.js *.css _build


%install
%make_install

# install the schema file
install -D -p -m 0644 \
    schemas/org.gnome.shell.extensions.pop-shell.gschema.xml \
    %{buildroot}%{_datadir}/glib-2.0/schemas/%{uuid}.gschema.xml

# install the schema override file
install -D -p -m 0644 %{S:1} %{buildroot}%{_datadir}/glib-2.0/schemas/50_pop-shell.gschema.override


%files
%license LICENSE
%doc README.md
%{_datadir}/gnome-shell/extensions/%{uuid}
%{_datadir}/glib-2.0/schemas/%{uuid}.gschema.xml
%{_datadir}/glib-2.0/schemas/50_pop-shell.gschema.override


%changelog
* Fri Aug 28 2020 Carl George <carl@george.computer> - 0.1.0-0.2.20200821git8416328
- Add keyboard shortcut overrides

* Thu Aug 27 2020 Carl George <carl@george.computer> - 0.1.0-0.1.20200821git8416328
- Initial package
