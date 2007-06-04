%define major 0
%define libname %mklibname %name %major
%define build_plf 0
%{?_with_plf: %{expand: %%global build_plf 1}}
%if %build_plf
%define distsuffix plf
%endif
%define pre pre2
%if %pre
%define rel 0.%pre.1
%define fname %name-%version%pre
%else
%define rel 1
%define fname %name-%version
%endif

Summary:	Next generation Beep Media Player
Name:		bmpx
Version:	0.40.0
Release:	%mkrel %rel
License:	GPL
Group:		Sound
URL:		http://beep-media-player.org/
Source0:	http://files.beep-media-player.org/releases/0.36/%{fname}.tar.bz2
Requires:	gstreamer0.10-plugins-base
Requires:	gstreamer0.10-plugins-good
Requires:	gstreamer0.10-plugins-ugly
Requires:	gstreamer0.10-gnomevfs
Requires:	pygtk2.0
Requires:	dbus-python
Requires:	dbus-x11
BuildRequires:	glib2-devel >= 2.10.0
BuildRequires:	hal-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	libgstreamer-plugins-base-devel
BuildRequires:	pygtk2.0-devel
BuildRequires:	gtkmm2.4-devel
BuildRequires:	librsvg-devel
BuildRequires:	libglademm2.4-devel
BuildRequires:	libboost-devel
BuildRequires:	libsm-devel
BuildRequires:	startup-notification-devel
BuildRequires:	libcdda-devel
BuildRequires:	taglib-devel
BuildRequires:	gamin-devel
BuildRequires:	ImageMagick
BuildRequires:	curl-devel
BuildRequires:	neon0.26-devel
BuildRequires:	libmusicbrainz-devel
BuildRequires:	libalsa-devel
BuildRequires:	sqlite3-devel
BuildRequires:	sidplay-devel
BuildRequires:  libofa-devel
#BuildRequires:  gaim-devel
BuildRequires:	flex bison
BuildRequires:	zip
BuildRequires:	desktop-file-utils
%if %build_plf
BuildRequires:	libmpeg4ip-devel
BuildRequires:	libmoodriver-devel >= 0.20
%endif
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
BMPx is the codename for the next-generation BMP. In general, users of
BMP should be familiar with BMPx right from the beginning, but there
will be new features and usage semantics changes as well. The code has
been rewritten ~95% from scratch, including the skinning engine and
the playback backend. A few utility functions and miscellaneous stuff
has been taken from the old codebase.

%if %build_plf
This package is in PLF as it violates some patents.
%endif


%package -n	%libname
Summary:	Library for BMPX
Group:		System/Libraries

%description -n	%libname
Library for BMPX.

%package -n	%libname-devel
Summary:	Devel library for BMPX
Group:		Development/C
Provides:	lib%name-devel = %version-%release
Requires:	%libname = %version

%description -n	%libname-devel
Devel library for BMPX.

%prep

%setup -q -n %fname

%build
%configure2_5x --enable-hal --enable-ofa --enable-sid \
%if %build_plf
 --enable-mp4v2 --enable-moodriver
%endif
#--enable-gaim

%make

%install
rm -rf $RPM_BUILD_ROOT %name.lang
%makeinstall_std
mv %buildroot%_datadir/locale/th_TH %buildroot%_datadir/locale/th
%find_lang %name
mkdir -p %{buildroot}/%{_menudir}
cat << EOF > %{buildroot}/%{_menudir}/%{name}
?package(%name):command=" %{_bindir}/beep-media-player-2"\
 icon="%name.png" needs="X11" section="Multimedia/Sound"\
 mimetypes="audio/x-mp3;audio/x-ogg;application/x-ogg;audio/x-mpegurl;audio/x-wav"\
 title="BMPx" longtitle="Play music" xdg="true"
EOF
desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-Multimedia-Sound" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/bmp-2.0.desktop


mkdir -p %{buildroot}/{%{_liconsdir}/,%_iconsdir,%_miconsdir}
ln -s %_datadir/icons/hicolor/48x48/apps/%name.png %{buildroot}/%{_liconsdir}/
convert -scale 32 data/icons/%name.png %buildroot%_iconsdir/%name.png
convert -scale 16 data/icons/%name.png %buildroot%_miconsdir/%name.png

#gw useless:
rm -f %buildroot%_libdir/%name/plugins/*/*.la \
      %buildroot%_libdir/%name/plugins/*/*/*.la

# why does this happen on seggie?
rm -f %{buildroot}%{_datadir}/locale/locale.alias

# broken symlink
ln -sf beep-media-player-2 %buildroot%_bindir/bmp2

# gw install firefox extension manually
install -m 644 xpi/bmp.xpi %buildroot%_datadir/%name/
cat > README.urpmi << EOF
Run 'firefox %_datadir/%name/bmp.xpi' to install the BMP-LastFM extension to
associate BMP with lastfm:// URIs
EOF


%post -n %libname -p /sbin/ldconfig

%postun -n %libname -p /sbin/ldconfig

%post
%update_menus
%update_desktop_database
%update_icon_cache hicolor

%postun
%clean_menus
%clean_desktop_database
%clean_icon_cache hicolor

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %name.lang
%defattr(-,root,root)
%doc README* ChangeLog AUTHORS
%_bindir/bmp2
%_bindir/beep-media-player-2
%_bindir/bmp-enqueue-files-2.0
%_bindir/bmp-enqueue-uris-2.0
%_bindir/bmp-play-files-2.0
%_bindir/bmp-play-lastfm-2.0
%_datadir/dbus-1/services/*
%_datadir/%name
%_datadir/applications/bmp-2.0.desktop
%_datadir/applications/bmp-enqueue-2.0.desktop
%_datadir/applications/bmp-play-2.0.desktop
%_datadir/applications/bmp-2.0-offline.desktop
%_datadir/icons/hicolor/48x48/apps/%name.png
%_mandir/man1/beep-media-player-2.1*
%{_menudir}/%{name}
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%_libdir/bmpx/
%_libexecdir/beep-media-player-2-bin
%_libexecdir/beep-media-player-2-sentinel
%_includedir/bmp-2.0/
%_libdir/pkgconfig/*.pc


