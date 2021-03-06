%define		pkgname	snap-server
Summary:	A fast, iteratee-based, epoll-enabled web server for the Snap Framework
Name:		ghc-%{pkgname}
Version:	0.9.4.0
Release:	1
License:	BSD
Group:		Development/Languages
Source0:	http://hackage.haskell.org/packages/archive/%{pkgname}/%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	4ee81486fcaf568a9f6ae58a4df1e28a
URL:		http://hackage.haskell.org/package/snap-server/
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-prof
BuildRequires:	ghc-attoparsec
BuildRequires:	ghc-attoparsec-prof
BuildRequires:	ghc-attoparsec-enumerator
BuildRequires:	ghc-attoparsec-enumerator-prof
BuildRequires:	ghc-blaze-builder >= 0.2.1.4
BuildRequires:	ghc-blaze-builder-prof >= 0.2.1.4
BuildRequires:	ghc-blaze-builder-enumerator >= 0.2.0
BuildRequires:	ghc-blaze-builder-enumerator-prof >= 0.2.0
BuildRequires:	ghc-enumerator >= 0.4.15
BuildRequires:	ghc-enumerator-prof >= 0.4.15
BuildRequires:	ghc-MonadCatchIO-transformers >= 0.2.1
BuildRequires:	ghc-MonadCatchIO-transformers-prof >= 0.2.1
BuildRequires:	ghc-snap-core >= 0.9.3
BuildRequires:	ghc-snap-core-prof >= 0.9.3
BuildRequires:	ghc-unix-compat >= 0.2
BuildRequires:	ghc-unix-compat-prof >= 0.2
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires(post,postun):	/usr/bin/ghc-pkg
Requires:	ghc-attoparsec-enumerator
Requires:	ghc-blaze-builder >= 0.2.1.4
Requires:	ghc-blaze-builder-enumerator >= 0.2.0
Requires:	ghc-enumerator >= 0.4.15
Requires:	ghc-MonadCatchIO-transformers >= 0.2.1
%requires_eq ghc-snap-core
Requires:	ghc-unix-compat >= 0.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddoc files
%define		_noautocompressdoc	*.haddock

%description
Snap is a simple and fast web development framework and server written
in Haskell. For more information or to download the latest version,
you can visit the Snap project website at http://snapframework.com/.

The Snap HTTP server is a high performance, epoll-enabled,
iteratee-based web server library written in Haskell. Together with
the snap-core library upon which it depends, it provides a clean and
efficient Haskell programming interface to the HTTP protocol.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC.
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
BuildRequires:	ghc-attoparsec-prof
BuildRequires:	ghc-attoparsec-enumerator-prof
BuildRequires:	ghc-blaze-builder-prof
BuildRequires:	ghc-blaze-builder-enumerator-prof
BuildRequires:	ghc-enumerator-prof
BuildRequires:	ghc-MonadCatchIO-transformers-prof
BuildRequires:	ghc-snap-core-prof
BuildRequires:	ghc-unix-compat-prof

%description prof
Profiling %{pkgname} library for GHC.  Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 --enable-library-profiling \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT/%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc CONTRIBUTORS README*
%doc %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.o
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.hi
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a

%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Snap
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Snap/Http
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Snap/Http/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Snap/Http/Server
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Snap/Http/Server/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Snap/Internal
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Snap/Internal/Http
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Snap/Internal/Http/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Snap/Internal/Http/Server
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Snap/Internal/Http/Server/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/SendFile
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/SendFile/*.hi

%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Snap/Http/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Snap/Http/Server/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Snap/Internal/Http/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Snap/Internal/Http/Server/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/SendFile/*.p_hi
