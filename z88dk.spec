# TODO:
# - rename conflicting manpages
Summary:	Z88 Development Kit
Summary(pl.UTF-8):	Zestaw programistyczny Z88
Name:		z88dk
Version:	1.10.1
Release:	1
Epoch:		1
License:	Artistic
Group:		Development/Tools
Source0:	http://downloads.sourceforge.net/z88dk/%{name}-%{version}.tgz
# Source0-md5:	7898bc04f9e5275845d6117cafa74096
Patch0:		%{name}-setup.patch
URL:		http://z88dk.sourceforge.net/
BuildRequires:	rpmbuild(macros) >= 1.213
ExcludeArch:	%{x8664} alpha ia64 ppc64 s390x sparc64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define Werror_cflags -Wformat

%description
z88dk contains C compiler (zcc) for Z80, assembler (z80asm) and
libraries for various Z80 based machines (such as ZX Spectrum, Z88,
MSX).

%description -l pl.UTF-8
z88dk zawiera kompilator C (zcc) generujący kod dla procesora Z80,
asembler (z80asm) i biblioteki dla różnych komputerów z procesorem
Z80, m.in. dla ZX Spectrum, Z88, MSX.

%package examples
Summary:	Examples for Z88 Development Kit
Summary(pl.UTF-8):	Przykłady dla zestawu programistycznego Z88
Group:		Development/Tools
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description examples
Some sample programs for Z88.

%description examples -l pl.UTF-8
Kilka przykładowych programów dla Z88.

%prep
%setup -q -n %{name}
%patch0 -p1


rm doc/netman/.sock_open.man.swp
find -name CVS | xargs rm -rf

mv doc/netman .

%build
PWD=$(pwd)
export Z80_OZFILES=$PWD/lib/
export ZCCCFG=$PWD/lib/config/
export PATH=$PATH:$PWD/bin
export CC="%{__cc}"
export CCOPT=-DUNIX
%{__make} \
	CFLAGS="%{rpmcflags}" \
	prefix=%{_prefix}

%{__make} -j1 -C libsrc
%{__make} -j1 -C libsrc install

%{__cc} %{rpmcflags} %{rpmldflags} support/zx/tapmaker.c -o tapmaker

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_mandir}/man3,%{_examplesdir}/%{name}-%{version}}

%{__make} install \
	prefix=%{_prefix} \
	DEFAULT=zx \
	DESTDIR=$RPM_BUILD_ROOT

install -p tapmaker $RPM_BUILD_ROOT%{_bindir}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

cp -a netman/man3z/* $RPM_BUILD_ROOT%{_mandir}/man3

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.1st EXTENSIONS doc/* support LICENSE
%attr(755,root,root) %{_bindir}/appmake
%attr(755,root,root) %{_bindir}/copt
%attr(755,root,root) %{_bindir}/sccz80
%attr(755,root,root) %{_bindir}/tapmaker
%attr(755,root,root) %{_bindir}/z80asm
%attr(755,root,root) %{_bindir}/zcc
%attr(755,root,root) %{_bindir}/zcpp
%{_datadir}/%{name}
%{_mandir}/man3/DeviceOffline.3*
%{_mandir}/man3/DeviceOnline.3*
%{_mandir}/man3/QueryPackage.3*
%{_mandir}/man3/byteorder.3*
%{_mandir}/man3/get*by*.3*
%{_mandir}/man3/[hn]to[hn][ls].3*
%{_mandir}/man3/pktdrive.3*
%{_mandir}/man3/resolve.3*
%{_mandir}/man3/reverse_addr_lookup.3*
%{_mandir}/man3/sock_*.3*
%{_mandir}/man3/tcp_*.3*

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
