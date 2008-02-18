%define name fricorder
%define version 0.6
%define release %mkrel 6
%define title Fricorder

Summary: Video recorder for Freebox from a french isp adsl 
Name:    %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{version}.tar.bz2
Patch0: %{name}-fixed-exe.patch.bz2
Source10:  %{name}-16.png
Source11:  %{name}-32.png
Source12:  %{name}-48.png
License: GPL
Group: 	 Video
Url: 	 http://manatlan.online.fr/fricorder.php
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch: noarch

Requires: vlc
Requires: python => 2.4 
Requires: pygtk2.0 pygtk2.0-libglade python-pyxml
Requires: zenity
Requires: at

%description
Fricorder is a video recorder for Freebox from a french isp adsl.

Fricorder permet de programmer des enregistrements
vidéo des flux émis par la freebox dans le cadre de
la fonctionnalité "multiposte", en utilisant vlc.

Ses principales features :
 - interfaces Web (pilotable à distance) et GTK
 - utilisation d'un guide tv pour faciliter la saisie (xmltv)
 - utilise les capacités de linux ;-) (commande "at")
   (fricorder n'a pas besoin d'être lancé, c'est l'OS qui se
   charge de l'enregistrement, seul ce dernier doit tourner ;-)
 - recherche des flux directement sur la freebox (playlist.m3u)

%prep
%setup -q -n %{name}
%patch -p1 
chmod 444 README

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/%{name}-%{version}
install -m755 frecord.sh $RPM_BUILD_ROOT/%{_datadir}/%{name}-%{version}
install -m755 fricorder.py $RPM_BUILD_ROOT/%{_datadir}/%{name}-%{version}
install -m644 SimpleGladeApp.py $RPM_BUILD_ROOT/%{_datadir}/%{name}-%{version}
install -m644 fricorder.glade $RPM_BUILD_ROOT/%{_datadir}/%{name}-%{version}
install -m755 fricorder-web.py $RPM_BUILD_ROOT/%{_datadir}/%{name}-%{version}
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/%{name}-%{version}/libs
for i in libs/*; do
  install -m644 $i $RPM_BUILD_ROOT/%{_datadir}/%{name}-%{version}/libs
done
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/%{name}-%{version}/templates
for i in templates/*; do
  install -m644 $i $RPM_BUILD_ROOT/%{_datadir}/%{name}-%{version}/templates
done
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/%{name}-%{version}/tmp

mkdir -p $RPM_BUILD_ROOT/%{_bindir}/
cat <<EOF >$RPM_BUILD_ROOT/%{_bindir}/%{name}
#!/bin/sh
PYTHONPATH=${PYTHONPATH=.}

PYTHONPATH=${PYTHONPATH}:%{_datadir}/%{name}-%{version}

exec python -u -O %{_datadir}/%{name}-%{version}/fricorder.py $*
EOF
chmod 755 $RPM_BUILD_ROOT/%{_bindir}/%{name}

#menus

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=%{title}
Comment=%{summary}
Exec=%{_bindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=QT;Video;Player;X-MandrivaLinux-Multimedia-Video;
EOF

install -m644 %{SOURCE10} -D %buildroot/%{_miconsdir}/%{name}.png
install -m644 %{SOURCE11} -D %buildroot/%{_iconsdir}/%{name}.png
install -m644 %{SOURCE12} -D %buildroot/%{_liconsdir}/%{name}.png

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc COPYING README
%{_bindir}/%{name}
%{_datadir}/%{name}-%{version}
%_iconsdir/%{name}.png
%_liconsdir/%{name}.png
%_miconsdir/%{name}.png
%_datadir/applications/mandriva-%{name}.desktop

%post
%{update_menus}

%postun
%{clean_menus}
