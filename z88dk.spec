%define		snap	20140121
Summary:	Z88 Development Kit
Summary(pl.UTF-8):	Zestaw programistyczny Z88
Name:		z88dk
Version:	1.10.2
Release:	0.%{snap}.1
Epoch:		1
License:	Artistic
Group:		Development/Tools
Source0:	http://nightly.z88dk.org/%{name}-%{snap}.tgz
# Source0-md5:	9c960065cae6fda242737743328cb655
Patch0:		%{name}-setup.patch
Patch1:		override.patch
URL:		http://z88dk.sourceforge.net/
BuildRequires:	rpmbuild(macros) >= 1.213
BuildRequires:	sed >= 4.0
ExcludeArch:	%{x8664} alpha ia64 ppc64 s390x sparc64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
%patch -P0 -p1
%patch -P1 -p1

rm doc/netman/.sock_open.man.swp
find -name CVS | xargs rm -rf

mv doc/netman .

%build
PWD=$(pwd)
export Z80_OZFILES=$PWD/lib/
export ZCCCFG=$PWD/lib/config/
export PATH=$PWD/bin:$PATH
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

cd netman/man3z
for m in *;
do
	sed -i -e 's|^\.so man3z/|.so man3/z88dk_|' $m
	cp -a $m $RPM_BUILD_ROOT%{_mandir}/man3/z88dk_$m;
done
cd -

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
%{_mandir}/man3/z88dk_DeviceOffline.3*
%{_mandir}/man3/z88dk_DeviceOnline.3*
%{_mandir}/man3/z88dk_QueryPackage.3*
%{_mandir}/man3/z88dk_byteorder.3*
%{_mandir}/man3/z88dk_get*by*.3*
%{_mandir}/man3/z88dk_[hn]to[hn][ls].3*
%{_mandir}/man3/z88dk_pktdrive.3*
%{_mandir}/man3/z88dk_resolve.3*
%{_mandir}/man3/z88dk_reverse_addr_lookup.3*
%{_mandir}/man3/z88dk_sock_*.3*
%{_mandir}/man3/z88dk_tcp_*.3*

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
