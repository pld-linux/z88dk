Summary:	Z88 Development Kit
Summary(pl):	Zestaw developerski Z88
Name:		z88dk
Version:	1.33
Release:	2
License:	Artistic
Group:		Development/Tools
Source0:	http://prdownloads.sourceforge.net/z88dk/z88dkv%{version}-src.tar.gz
Patch0:		z88dk-make-clean.patch
Patch1:		z88dk-make-config.patch
URL:		http://z88dk.sourceforge.net/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	_z88dkdir	%{_var}/lib/z88dk

%description
z88dk contains C compiler (zcc) for Z80, assembler (z80asm)
and libraries for various Z80 based machines (such as ZX Spectrum,
Z88, MSX).

%description -l pl
z88dk zawiera kompilator C (zcc) generuj±cy kod dla procesora Z80,
asembler (z80asm) i biblioteki dla ró¿nych komputerów
z procesorem Z80, m. in. dla ZX Spectrum, Z88, MSX.

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1

%build
make clean
mv src/z80asm/config.h src/z80asm/config.h.orig
mv src/zcc/zcc.h src/zcc/zcc.h.orig

# build for the first time to build libraries
sed "s?/usr/local/z88dk?`pwd`?" < src/z80asm/config.h.orig \
> src/z80asm/config.h
sed "s?/usr/local/z88dk?`pwd`?" < src/zcc/zcc.h.orig \
> src/zcc/zcc.h
make CC=%{__cc} CFLAGS="%{rpmcflags}" prefix=`pwd`
PATH=`pwd`/bin:$PATH ; export PATH
ZCCCFG=`pwd`/lib/config/ ; export ZCCCFG
cd libsrc
make
make install
cd ..

# setting default paths and build again
sed "s?/usr/local/z88dk?%{_z88dkdir}?" < src/z80asm/config.h.orig \
> src/z80asm/config.h
sed "s?/usr/local/z88dk?%{_z88dkdir}?" < src/zcc/zcc.h.orig \
> src/zcc/zcc.h
make CC=%{__cc} CFLAGS="%{rpmcflags}" prefix=%{_z88dkdir}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir} \
	$RPM_BUILD_ROOT%{_z88dkdir}/{bin,lib/{clibs,config}} \
	$RPM_BUILD_ROOT%{_z88dkdir}/include/{net,oz,sys} \
	$RPM_BUILD_ROOT%{_examplesdir}/%{name}

install \
	bin/{appmake,copt,sccz80,z80asm,zcc,zcpp} $RPM_BUILD_ROOT%{_bindir}

install lib/config/*.cfg $RPM_BUILD_ROOT%{_z88dkdir}/lib/config
install lib/clibs/*.lib $RPM_BUILD_ROOT%{_z88dkdir}/lib/clibs
install lib/clibs/README $RPM_BUILD_ROOT%{_z88dkdir}/lib/clibs
install lib/[ad-z]* $RPM_BUILD_ROOT%{_z88dkdir}/lib
install lib/README $RPM_BUILD_ROOT%{_z88dkdir}/lib
install lib/{bas_crt0.asm,bastoken.def,char.def,cpm_crt0.asm,\
cpm_crt0.opt,ctrlchar.def} $RPM_BUILD_ROOT%{_z88dkdir}/lib

install include/*.h $RPM_BUILD_ROOT%{_z88dkdir}/include
install include/net/*.h $RPM_BUILD_ROOT%{_z88dkdir}/include/net
install include/oz/*.h $RPM_BUILD_ROOT%{_z88dkdir}/include/oz
install include/sys/*.h $RPM_BUILD_ROOT%{_z88dkdir}/include/sys
cp -ar examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}

gzip -9nf README.1st EXTENSIONS doc/*.txt doc/netman/cat3z/*.3

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz doc/* support
%dir %{_examplesdir}/%{name}
%dir %{_z88dkdir}
%dir %{_z88dkdir}/lib
%dir %{_z88dkdir}/include
%attr(755,root,root) %{_bindir}/*
%{_examplesdir}/%{name}/*
%{_z88dkdir}/include/*
%{_z88dkdir}/lib/*
