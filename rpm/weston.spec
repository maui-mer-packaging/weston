# Build with Cairo by default
%bcond_with cairo

# Do not build for X11 or XWayland by default
%bcond_without X11
%bcond_without xwayland

# Currently X11 builds are enabled but we lack cairo-xcb, so we
# always disable the X11 compositor
#%define enable_x11 %{with X11}
#%define enable_xwayland %{with xwayland}
%define enable_x11 0
%define enable_xwayland 0

Name:       weston
Summary:    Wayland Compositor Infrastructure
Version:    1.5.93
Release:    1
Group:      System/GUI/Other
License:    MIT
URL:        http://wayland.freedesktop.org/
Source0:    %{name}-%{version}.tar.xz
Source100:  weston.yaml
Requires:   xkeyboard-config
%if %{with cairo}
BuildRequires:  pkgconfig(cairo-egl) >= 1.11.3
%endif
%if 0%{?enable_x11} || 0%{?enable_xwayland}
BuildRequires:  pkgconfig(cairo-xcb)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-xfixes)
BuildRequires:  pkgconfig(xcursor)
%endif
%ifarch %{ix86}
BuildRequires:  pkgconfig(egl) >= 7.10
BuildRequires:  pkgconfig(glesv2)
%endif
%if "%{name}" == "weston-rpi"
BuildRequires:  pkgconfig(gfx-rpi-libEGL-devel)
BuildRequires:  pkgconfig(gfx-rpi-libGLESv2-devel)
BuildRequires:  pkgconfig(gfx-rpi-libOMXIL-devel)
%endif
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(libdrm) >= 2.4.30
BuildRequires:  pkgconfig(libffi)
BuildRequires:  pkgconfig(libsystemd-login)
BuildRequires:  pkgconfig(libudev) >= 136
BuildRequires:  pkgconfig(mtdev) >= 1.1.0
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(poppler-glib)
BuildRequires:  pkgconfig(wayland-client) >= 1.5.0
BuildRequires:  pkgconfig(wayland-egl) >= 1.5.0
BuildRequires:  pkgconfig(wayland-server) >= 1.5.0
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(libunwind)
BuildRequires:  pkgconfig(xkbcommon) >= 0.0.578
BuildRequires:  pkgconfig(expat)
BuildRequires:  pkgconfig(libinput)
BuildRequires:  gcc-c++
BuildRequires:  libjpeg-devel
BuildRequires:  pam-devel
BuildRequires:  pkgconfig
BuildRequires:  xkeyboard-config

%if "%{name}" == "weston-rpi"
Provides:  weston
%endif

%description
Weston is the reference implementation of a Wayland compositor, and a
useful compositor in its own right. Weston has various backends that
lets it run on Linux kernel modesetting and evdev input as well as
under X11. Weston ships with a few example clients, from simple
clients that demonstrate certain aspects of the protocol to more
complete clients and a simplistic toolkit. There is also a quite
capable terminal emulator (weston-terminal) and an toy/example
desktop shell. Finally, weston also provides integration with the
Xorg server and can pull X clients into the Wayland desktop and act
as a X window manager.


%package devel
Summary:    Development files for %{name}
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
%if "%{name}" == "weston-rpi"
Provides:   weston-devel
%endif

%description devel
This package contains the files necessary to develop applications
that use %{name}.


%prep
%setup -q -n %{name}-%{version}/upstream


%build
%if "%{name}" == "weston-rpi"
export WESTON_NATIVE_BACKEND=rpi-backend.so
%endif

NOCONFIGURE=1 ./autogen.sh

%configure --disable-static \
%if 0%{?enable_x11}
    --enable-x11-compositor \
%else
    --disable-x11-compositor \
%endif
%if 0%{?enable_xwayland}
    --enable-xwayland \
%else
    --disable-xwayland \
%endif
    --disable-xwayland-test \
%if %{with cairo} && "%{name}" == "weston"
    --with-cairo-glesv2 \
%endif
%if %{with cairo} && "%{name}" == "weston-rpi"
    --with-cairo=image \
%endif
    --enable-tablet-shell \
    --enable-drm-compositor \
    --enable-wayland-compositor \
    --enable-fbdev-compositor \
    --disable-rdp-compositor \
    --enable-weston-launch \
    --enable-simple-clients \
    --enable-simple-egl-clients \
    --enable-clients \
    --enable-demo-clients=yes \
    --disable-colord \
    --disable-setuid-install

make %{?_smp_mflags}


%install
rm -rf %{buildroot}
%make_install
rm -f "%buildroot/%_libdir"/*.la "%buildroot/%_libdir/weston"/*.la;


%files
%defattr(-,root,root,-)
%{_bindir}/wcap-*
%{_bindir}/weston*
%{_libexecdir}/weston-*
%{_libdir}/weston
%{_datadir}/weston
%{_mandir}/man1/weston.1*
%{_mandir}/man7/weston*7*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/pkgconfig/weston.pc
