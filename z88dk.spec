Summary:	Z88 Development Kit
Summary(pl.UTF-8):	Zestaw programistyczny Z88
%define snap	20101107
Name:		z88dk
Version:	1.10
Release:	0.%{snap}.1
Epoch:		1
License:	Artistic
Group:		Development/Tools
Source0:	http://nightly.z88dk.org/%{name}-%{snap}.tgz
# Source0-md5:	17725bbb3e7f945fe17627578ace6062
Patch0:		%{name}-setup.patch
URL:		http://z88dk.sourceforge.net/
BuildRequires:	rpmbuild(macros) >= 1.213
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
%patch0 -p1

%build
Z80_OZFILES=`pwd`/lib/
ZCCCFG=`pwd`/lib/config/
PATH=$PATH:`pwd`/bin
CC="%{__cc}"
CCOPT=-DUNIX
export CC CCOPT
export PATH Z80_OZFILES ZCCCFG
%{__make} CFLAGS="%{rpmcflags}" prefix=%{_prefix}
%{__make} -j1 -C libsrc
%{__make} -j1 -C libsrc install

%{__cc} %{rpmcflags} %{rpmldflags} support/zx/tapmaker.c -o tapmaker

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_prefix} \
	$RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT DEFAULT=zx prefix=%{_prefix}
install tapmaker $RPM_BUILD_ROOT%{_bindir}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.1st EXTENSIONS doc/* support LICENSE
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
