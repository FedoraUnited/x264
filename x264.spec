# globals for x264-0.148-20160912-3f5ed56.tar.xz
%global api 148
%global gitdate 20160912
%global gitversion 3f5ed56
%global snapshot %{gitdate}-%{gitversion}
%global gver .%{gitdate}git%{gitversion}
%global branch master

Name:           x264
Version: 	0.%{api}
Release: 	6%{?gver}%{?dist}
Epoch:		1
Summary:        A free h264/avc encoder - encoder binary
License:        GPLv2
Group:          Applications/Multimedia
Url:            http://developers.videolan.org/x264.html
Source0: 	%{name}-0.%{api}-%{snapshot}.tar.xz
Source1: 	x264-snapshot.sh
BuildRequires:  nasm
BuildRequires:  pkgconfig
BuildRequires:  yasm-devel >= 1.2.0
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Provides:	%{name} = %{epoch}:%{version}-%{release}
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}


%description
x264 is a free library for encoding next-generation H264/AVC video
streams. The code is written from scratch by Laurent Aimar, Loren
Merritt, Eric Petit (OS X), Min Chen (vfw/asm), Justin Clay (vfw), Mans
Rullgard, Radek Czyz, Christian Heine (asm), Alex Izvorski (asm), and
Alex Wright. It is released under the terms of the GPL license. This
package contains a shared library and a commandline tool for encoding
H264 streams. This library is needed for mplayer/mencoder for H264
encoding support.

Encoder features:
- CAVLC/CABAC
- Multi-references
- Intra: all macroblock types (16x16, 8x8, and 4x4 with all predictions)
- Inter P: all partitions (from 16x16 down to 4x4)
- Inter B: partitions from 16x16 down to 8x8 (including skip/direct)
- Ratecontrol: constant quantizer, single or multipass ABR, optional VBV
- Scene cut detection
- Adaptive B-frame placement
- B-frames as references / arbitrary frame order
- 8x8 and 4x4 adaptive spatial transform
- Lossless mode
- Custom quantization matrices
- Parallel encoding of multiple slices (currently disabled)

Be aware that the x264 library is still in early development stage. The
command line tool x264 can handle only raw YUV 4:2:0 streams at the
moment so please use mencoder or another tool that supports x264 library
for all other file types.

%package libs
Summary: Library for encoding H264/AVC video streams
Group: Development/Libraries
Provides:	%{name}-libs = %{epoch}:%{version}-%{release}

%description libs
x264 is a free library for encoding H264/AVC video streams, written from
scratch.

%package devel
Summary:        Libraries and include file for the %{name} encoder
Group:          Development/Libraries
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Requires: 	pkgconfig
Provides:       x264-devel = %{version}
Provides:	x264-devel = %{epoch}:%{version}-%{release}
Obsoletes:      x264-devel < %{version}

%description devel
x264 is a free library for encoding next-generation H264/AVC video
streams. The code is written from scratch by Laurent Aimar, Loren
Merritt, Eric Petit (OS X), Min Chen (vfw/asm), Justin Clay (vfw), Mans
Rullgard, Radek Czyz, Christian Heine (asm), Alex Izvorski (asm), and
Alex Wright. It is released under the terms of the GPL license. This
package contains a static library and a header needed for the
development with libx264. This library is needed to build
mplayer/mencoder with H264 encoding support.

%prep
%setup -n x264 


%build

cp -r %{_builddir}/%{name} %{_builddir}/%{name}-10bit

  pushd %{_builddir}/%{name}

%configure --enable-shared \
    --enable-pic

make %{?_smp_mflags}


pushd %{_builddir}/%{name}-10bit

%configure --enable-shared \
    --enable-pic \
    --bit-depth=10

make %{?_smp_mflags}

%install

  make -C %{_builddir}/%{name} DESTDIR=%{buildroot} install-cli
  install -m 755 %{_builddir}/%{name}-10bit/x264 %{buildroot}/%{_bindir}/x264-10bit

  install -dm 755 %{buildroot}/%{_libdir}
  make -C %{_builddir}/%{name} DESTDIR=%{buildroot} install-lib-shared %{?_smp_mflags}

  make -C %{_builddir}/%{name}-10bit DESTDIR=%{buildroot} install-lib-shared %{?_smp_mflags}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_bindir}/x264
%{_bindir}/x264-10bit

%files libs
%{_libdir}/libx264.so.%{api}

%files devel
%defattr(0644,root,root)
%{_includedir}/x264.h
%{_includedir}/x264_config.h
%{_libdir}/pkgconfig/x264.pc
%{_libdir}/libx264.so


%changelog

* Mon Sep 12 2016 David Vásquez <davidjeremias82 AT gmail DOT com> 0.148-6-20160906git3f5ed56
- Added epoch for sub-packages libs and devel

* Tue Sep 06 2016 David Vásquez <davidjeremias82 AT gmail DOT com> 0.148-4-20160906git3f5ed56
- Epoch tag

* Thu Jul 07 2016 David Vásquez <davidjeremias82 AT gmail DOT com> 0.148-3-20160707git3f5ed56
- Updated to 0.148-20160707git3f5ed56

* Wed Apr 20 2016 David Vásquez <davidjeremias82 AT gmail DOT com> 0.148-2-20160420git3b70645
- Updated to x264-0.148-20160420-3b70645
- Built x264-10bit

* Sat Feb 20 2016 David Vasquez <davidjeremias82 at gmail dot com> - 0.148-1-20160220gita01e339
- Updated to 0.148-20160220-a01e339

* Mon Jul 13 2015 David Vasquez <davidjeremias82 at gmail dot com> - 0.146-1-20150713git121396c
- Upstream
- Updated to 0.146-20150713git121396c
- Added git tag in x264-snapshot.sh

* Tue Nov 19 2013 obs@botter.cc
- add -fno-aggressive-loop-optimizations to extra-cflags in
  configure for >= 13.1 (specfile), see also
  https://bugs.launchpad.net/ubuntu/+source/x264/+bug/1241772
  MAY BE REMOVED on upstream fix
