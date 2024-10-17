%define major 0
%define libname %mklibname %name %major
%define develname %mklibname -d %name
%define pre 0
%if %pre
%define rel 0.%pre.2
%define fname %name-%{version}RC3
%else
%define rel 10
%define fname %name-%version
%endif

Summary:	Next generation Beep Media Player
Name:		bmpx
Version:	0.40.14
Release:	%mkrel %rel
License:	GPLv2+
Group:		Sound
URL:		https://bmpx.backtrace.info/site/BMPx_Homepage
Source0:	http://files.backtrace.info/releases/0.40/%{fname}.tar.bz2
Patch:		bmpx-0.40.14-format-strings.patch
Patch1:		bmpx-0.40.14-no-gsd-spawn.patch
Patch2:		bmpx-0.40.14-new-cairomm.patch
Patch3:		bmpx-0.40.14-compile.patch
Patch4:		bmpx-0.40.14-libsoup24.patch
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
BuildRequires:	libsoup-devel
BuildRequires:	libgstreamer-plugins-base-devel
BuildRequires:	pygtk2.0-devel
BuildRequires:	librsvg-devel
BuildRequires:	libglademm2.4-devel
BuildRequires:	boost-devel
BuildRequires:	libsm-devel
BuildRequires:	startup-notification-devel
BuildRequires:	libcdio-devel
BuildRequires:	taglib-devel
BuildRequires:	gamin-devel
BuildRequires:	imagemagick
BuildRequires:	curl-devel
BuildRequires:  libmusicbrainz-devel
BuildRequires:	libalsa-devel
BuildRequires:	sqlite3-devel
BuildRequires:	sidplay-devel
BuildRequires:  libofa-devel
BuildRequires:  libsexymm-devel
BuildRequires:  libgnome-vfs2-devel
BuildRequires:  libGConf2-devel
BuildRequires:	intltool
#BuildRequires:  gaim-devel
BuildRequires:	flex bison
BuildRequires:	zip
BuildRequires:	desktop-file-utils
BuildRequires:  libxslt-proc
Obsoletes:	%libname
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

%package -n	%develname
Summary:	Devel library for BMPX
Group:		Development/C
Provides:	lib%name-devel = %version-%release
Provides:	%name-devel = %version-%release

%description -n	%develname
Devel library for BMPX.

%prep
%setup -q -n %fname
%patch -p1
%patch1 -p1 -b .no-gsd-spawn
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
autoreconf -fi
%configure2_5x --enable-hal --enable-sid
%make

%install
rm -rf $RPM_BUILD_ROOT %name.lang
%makeinstall_std
mv %buildroot%_datadir/locale/th_TH %buildroot%_datadir/locale/th
%find_lang %name
desktop-file-install --vendor="" \
  --add-category="Audio" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/{bmp-2.0,bmp-2.0-offline}.desktop

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

%if %mdkversion < 200900
%post
%update_menus
%update_desktop_database
%update_icon_cache hicolor
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%clean_desktop_database
%clean_icon_cache hicolor
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %name.lang
%defattr(-,root,root)
%doc README* ChangeLog AUTHORS
%_bindir/bmp2
%_bindir/beep-media-player-2
%_bindir/bmp-play-files-2.0
%_bindir/bmp-play-uris-2.0
%_datadir/dbus-1/services/*
%_datadir/%name
%_datadir/applications/bmp-2.0.desktop
%_datadir/applications/bmp-play-2.0.desktop
%_datadir/applications/bmp-2.0-offline.desktop
%_datadir/icons/hicolor/48x48/apps/%name.png
%_mandir/man1/beep-media-player-2.1*
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%_libdir/bmpx/
%_libexecdir/beep-media-player-2-bin
%_libexecdir/beep-media-player-2-sentinel

%files -n %develname
%defattr(-,root,root)
%_includedir/bmp-2.0/
%_libdir/pkgconfig/*.pc
