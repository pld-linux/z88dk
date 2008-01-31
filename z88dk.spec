Summary:	Z88 Development Kit
Summary(pl.UTF-8):	Zestaw programistyczny Z88
Name:		z88dk
Version:	1.7
Release:	1
Epoch:		1
License:	Artistic
Group:		Development/Tools
Source0:	http://dl.sourceforge.net/z88dk/%{name}-src-%{version}.tgz
# Source0-md5:	cbb910bcb8beb0b15b101a4420d3fb25
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
Z80, m. in. dla ZX Spectrum, Z88, MSX.

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
sed -i -e 's/$(prefix)/$(DESTDIR)\/$(prefix)/g' Makefile
sed -i -e 's/\.\/config\.sh $(DESTDIR)\//\.\/config.sh /' Makefile

%build
Z80_OZFILES=`pwd`/lib/
ZCCCFG=`pwd`/lib/config/
PATH=$PATH:`pwd`/bin
CC="%{__cc}"
CCOPT=-DUNIX
export CC CCOPT
export PATH Z80_OZFILES ZCCCFG
%{__make} CFLAGS="%{rpmcflags}" prefix=%{_prefix}
%{__make} -C `pwd`/libsrc
%{__make} -C `pwd`/libsrc install

%{__cc} %{rpmcflags} %{rpmldflags} support/zx/tapmaker.c -o tapmaker

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_prefix} \
	$RPM_BUILD_ROOT%{_examplesdir}/%{name}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT DEFAULT=zx prefix=%{_prefix}
install tapmaker $RPM_BUILD_ROOT%{_bindir}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.1st EXTENSIONS doc/* support LICENSE
%attr(755,root,root) %{_bindir}/*
%{_libdir}/%{name}

%files examples
%defattr(644,root,root,755)
%dir %{_examplesdir}/%{name}
%{_examplesdir}/%{name}/*
