Summary:	Z88 Development Kit
Summary(pl):	Zestaw programistyczny Z88
Name:		z88dk
Version:	1.5
Epoch:		1
Release:	2
License:	Artistic
Group:		Development/Tools
Source0:	http://dl.sourceforge.net/%{name}/%{name}-src-%{version}.tar.gz
# Source0-md5:	07c122c40c66093ede4ba3047e8f6128
Patch0:		%{name}-typo.patch
Patch1:		%{name}-DESTDIR.patch
URL:		http://z88dk.sourceforge.net/
ExcludeArch:	amd64 alpha ia64 ppc64 sparc64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
z88dk contains C compiler (zcc) for Z80, assembler (z80asm) and
libraries for various Z80 based machines (such as ZX Spectrum, Z88,
MSX).

%description -l pl
z88dk zawiera kompilator C (zcc) generuj±cy kod dla procesora Z80,
asembler (z80asm) i biblioteki dla ró¿nych komputerów z procesorem
Z80, m. in. dla ZX Spectrum, Z88, MSX.

%package examples
Summary:	Examples for Z88 Development Kit
Summary(pl):	Przyk³ady dla zestawu programistycznego Z88
Group:		Development/Tools
Requires:	%{name} = %{epoch}:%{version}

%description examples
Some sample programs for Z88.

%description examples -l pl
Kilka przyk³adowych programów dla Z88.

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1

find www -name CVS -exec rm -rf {} \; ||:

%build
Z80_OZFILES=`pwd`/lib/
ZCCCFG=`pwd`/lib/config/
PATH=$PATH:`pwd`/bin
CC="%{__cc}"
CFLAGS="%{rpmcflags}"
CCOPT=-DUNIX
export CC CFLAGS CCOPT
export PATH Z80_OZFILES ZCCCFG
%{__make} prefix=%{_prefix}
%{__make} -C `pwd`/libsrc
%{__make} -C `pwd`/libsrc install

cp support/zx/bin2tap.c .
%{__cc} %{rpmcflags} %{rpmldflags} bin2tap.c -o bin2tap

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_prefix} \
	$RPM_BUILD_ROOT%{_examplesdir}/%{name}

%{__make} install DESTDIR=$RPM_BUILD_ROOT prefix=%{_prefix}
install bin2tap $RPM_BUILD_ROOT%{_bindir}
cp -ar examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.1st EXTENSIONS doc/* support www LICENSE
%attr(755,root,root) %{_bindir}/*
%{_libdir}/%{name}

%files examples
%defattr(644,root,root,755)
%dir %{_examplesdir}/%{name}
%{_examplesdir}/%{name}/*
